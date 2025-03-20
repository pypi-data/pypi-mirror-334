from pleach.custom import Component
from pleach.inputs import MessageTextInput
from pleach.template import Output
from pleach.schema.message import Message
import json
import requests
from typing import Dict

class APINodeExecutor(Component):
    """Executes individual API nodes with proper request handling"""
    display_name = "API Node Executor"
    description = "Executes individual API nodes with retry and error handling"
    
    inputs = [
        MessageTextInput(
            name="node_config",
            display_name="Node Configuration",
            info="API node configuration with endpoint and parameters",
            required=True
        ),
        MessageTextInput(
            name="input_data",
            display_name="Input Data",
            info="Input data for the API call",
            required=True
        )
    ]

    outputs = [
        Output(
            name="result",
            display_name="API Result",
            method="execute_node"
        )
    ]

    def execute_node(self) -> Message:
        try:
            config = json.loads(self.node_config.text if isinstance(self.node_config, Message) else self.node_config)
            input_data = json.loads(self.input_data.text if isinstance(self.input_data, Message) else self.input_data)
            
            # Process parameters
            processed_params = self._process_parameters(config["parameters"], input_data)
            
            # Execute request with retry logic
            result = self._execute_request(
                config["method"],
                config["endpoint"],
                processed_params,
                config.get("error_handling", {})
            )
            
            return Message(text=json.dumps(result))
            
        except Exception as e:
            return Message(text=json.dumps({
                "status": "error",
                "error": str(e)
            }))

    def _process_parameters(self, parameters: Dict, input_data: Dict) -> Dict:
        """Processes and validates node parameters"""
        processed = {
            "body": {},
            "query": {},
            "path": {}
        }
        
        for param_type, params in parameters.items():
            for key, value in params.items():
                if isinstance(value, str) and value in input_data:
                    processed[param_type][key] = input_data[value]
                else:
                    processed[param_type][key] = value
                    
        return processed

    def _execute_request(self, method: str, endpoint: str, params: Dict, error_config: Dict) -> Dict:
        """Executes API request with retry logic"""
        max_retries = error_config.get("max_retries", 0)
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                response = self._make_request(method, endpoint, params)
                return {
                    "status": "success",
                    "data": response,
                    "retries": retry_count
                }
            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    raise
                
        return {
            "status": "error",
            "error": "Max retries exceeded"
        }

    def _make_request(self, method: str, endpoint: str, params: Dict) -> Dict:
        """Makes the actual API request"""
        headers = {"Content-Type": "application/json"}
        
        if method == "GET":
            response = requests.get(endpoint, params=params["query"], headers=headers)
        elif method == "POST":
            response = requests.post(endpoint, json=params["body"], params=params["query"], headers=headers)
        elif method == "PUT":
            response = requests.put(endpoint, json=params["body"], params=params["query"], headers=headers)
        elif method == "DELETE":
            response = requests.delete(endpoint, params=params["query"], headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()
        return response.json()