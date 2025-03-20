from pleach.custom import Component
from pleach.io import MessageTextInput, Output
from pleach.schema import Data
import json
from typing import Dict, List
from datetime import datetime

class FlowCreator(Component):
    display_name = "Flow Creator"
    description = "Creates Langflow flows from workflow definitions"
    documentation = "http://docs.pleach.org/components/flow-creator"
    icon = "flow"
    name = "FlowCreator"

    inputs = [
        MessageTextInput(
            name="workflow_plan",
            display_name="Workflow Plan",
            info="The analyzed workflow plan from API Processor",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="langflow_api_url",
            display_name="Langflow API URL",
            info="URL for the Langflow API",
            required=False,
            value="http://localhost:7860/api/v1",
            tool_mode=True,
        )
    ]

    outputs = [
        Output(
            name="flow_info",
            display_name="Flow Information",
            method="process_flow"
        )
    ]

    def process_flow(self) -> Data:
        """Process flow and return response"""
        try:
            workflow_plan = json.loads(self.workflow_plan if isinstance(self.workflow_plan, str) else self.workflow_plan.value)
            
            # Generate preview
            preview = self._format_preview(workflow_plan)
            
            # Create response with preview and buttons
            response = {
                "content": preview,
                "additional_kwargs": {
                    "buttons": [
                        {
                            "label": "Create Flow",
                            "value": "create",
                            "action": {
                                "workflow_plan": workflow_plan
                            }
                        },
                        {
                            "label": "Cancel",
                            "value": "cancel"
                        }
                    ]
                }
            }
            
            data = Data(value=json.dumps(response))
            self.status = data
            return data
            
        except Exception as e:
            error_response = {
                "content": f"Error processing flow: {str(e)}",
                "additional_kwargs": {}
            }
            data = Data(value=json.dumps(error_response))
            self.status = data
            return data

    def _format_preview(self, workflow_plan: Dict) -> str:
        """Format workflow preview for chat"""
        workflow = workflow_plan["workflow"]
        
        preview_lines = [
            f"I can create a flow for: {workflow['name']}",
            f"\nDescription: {workflow['description']}",
            "\nRequired Inputs:"
        ]
        
        for req in workflow_plan.get("initial_requirements", []):
            preview_lines.append(
                f"- {req['field']}: {req['type']} "
                f"({'Required' if req.get('required') else 'Optional'})"
            )
        
        preview_lines.append("\nSteps:")
        for step in workflow["steps"].get("sequential", []):
            preview_lines.append(
                f"- {step['name']}: {step['method']} {step['endpoint']}"
            )
            
        if workflow["steps"].get("parallel", []):
            preview_lines.append("\nParallel Steps:")
            for step in workflow["steps"]["parallel"]:
                preview_lines.append(
                    f"- {step['name']}: {step['method']} {step['endpoint']}"
                )
                
        preview_lines.append("\nWould you like me to create this flow?")
        
        return "\n".join(preview_lines)

    def _generate_flow_structure(self, workflow_plan: Dict) -> Dict:
        """Generates Langflow-compatible flow structure"""
        workflow = workflow_plan["workflow"]
        nodes = []
        edges = []
        
        # Track node positions for layout
        position = {"x": 100, "y": 100}
        
        # Create input nodes
        input_nodes = self._create_input_nodes(workflow_plan.get("initial_requirements", []), position)
        nodes.extend(input_nodes["nodes"])
        
        # Create API nodes for sequential steps
        sequential_nodes = self._create_sequential_nodes(
            workflow["steps"].get("sequential", []),
            input_nodes["node_map"],
            position
        )
        nodes.extend(sequential_nodes["nodes"])
        edges.extend(sequential_nodes["edges"])
        
        # Create parallel nodes if any
        if workflow["steps"].get("parallel", []):
            parallel_nodes = self._create_parallel_nodes(
                workflow["steps"]["parallel"],
                sequential_nodes["node_map"],
                position
            )
            nodes.extend(parallel_nodes["nodes"])
            edges.extend(parallel_nodes["edges"])
        
        return {
            "name": workflow["name"],
            "description": workflow["description"],
            "data": {
                "nodes": nodes,
                "edges": edges
            }
        }

    def _create_input_nodes(self, requirements: List[Dict], position: Dict) -> Dict:
        """Creates input nodes for initial requirements"""
        nodes = []
        node_map = {}
        
        for req in requirements:
            node_id = f"input_{req['field']}"
            nodes.append({
                "id": node_id,
                "type": "InputNode",
                "position": position.copy(),
                "data": {
                    "name": req["field"],
                    "type": req["type"],
                    "required": req["required"],
                    "description": req["description"],
                    "default": req.get("extracted_value", ""),
                    "customField": True
                }
            })
            node_map[req["field"]] = node_id
            position["y"] += 150
            
        return {"nodes": nodes, "node_map": node_map}

    def _create_sequential_nodes(self, steps: List[Dict], input_map: Dict, position: Dict) -> Dict:
        """Creates nodes for sequential API steps"""
        nodes = []
        edges = []
        node_map = {}
        position["x"] += 300
        position["y"] = 100
        
        for step in steps:
            node_id = f"api_{step['step_id']}"
            
            # Create API node
            nodes.append({
                "id": node_id,
                "type": "APINode",
                "position": position.copy(),
                "data": {
                    "name": step["name"],
                    "endpoint": step["endpoint"],
                    "method": step["method"],
                    "parameters": step["parameters"],
                    "error_handling": step["error_handling"],
                    "operation_id": step.get("operation_id", ""),
                    "description": step.get("description", "")
                }
            })
            
            # Create edges from inputs and previous steps
            self._create_parameter_edges(
                step["parameters"],
                input_map,
                node_map,
                node_id,
                edges
            )
            
            # Create dependency edge if specified
            if step.get("depends_on"):
                edges.append({
                    "source": node_map[step["depends_on"]],
                    "target": node_id,
                    "type": "dependency"
                })
            
            node_map[step["step_id"]] = node_id
            position["y"] += 200
            
        return {"nodes": nodes, "edges": edges, "node_map": node_map}

    def _create_parallel_nodes(self, steps: List[Dict], sequential_map: Dict, position: Dict) -> Dict:
        """Creates nodes for parallel API steps"""
        nodes = []
        edges = []
        position["x"] += 300
        
        for step in steps:
            node_id = f"api_{step['step_id']}"
            
            # Create API node
            nodes.append({
                "id": node_id,
                "type": "APINode",
                "position": position.copy(),
                "data": {
                    "name": step["name"],
                    "endpoint": step["endpoint"],
                    "method": step["method"],
                    "parameters": step["parameters"],
                    "error_handling": step["error_handling"],
                    "operation_id": step.get("operation_id", ""),
                    "description": step.get("description", "")
                }
            })
            
            # Create dependency edge
            if step.get("depends_on"):
                edges.append({
                    "source": sequential_map[step["depends_on"]],
                    "target": node_id,
                    "type": "dependency"
                })
            
            position["y"] += 200
            
        return {"nodes": nodes, "edges": edges}

    def _create_parameter_edges(self, parameters: Dict, input_map: Dict, node_map: Dict, target_node: str, edges: List):
        """Creates edges for parameter connections"""
        for param_type, params in parameters.items():
            for key, value in params.items():
                if isinstance(value, str):
                    if value.startswith("{response."):
                        # Connect from previous step
                        source_step = value[10:-1].split(".")[0]
                        if source_step in node_map:
                            edges.append({
                                "source": node_map[source_step],
                                "target": target_node,
                                "type": "data",
                                "data": {
                                    "parameter": key,
                                    "param_type": param_type
                                }
                            })
                    elif key in input_map:
                        # Connect from input node
                        edges.append({
                            "source": input_map[key],
                            "target": target_node,
                            "type": "data",
                            "data": {
                                "parameter": key,
                                "param_type": param_type
                            }
                        })

    def _create_langflow(self, flow_data: Dict) -> Dict:
        """Creates flow in Langflow via API"""
        try:
            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Create flow via API
            response = requests.post(
                f"{self.langflow_api_url}/flows/",
                json=flow_data,
                headers=headers
            )
            response.raise_for_status()
            
            # Get created flow details
            flow_response = response.json()
            
            return {
                "status": "success",
                "flow_id": flow_response.get("id"),
                "flow_data": flow_response,
                "created_at": datetime.now().isoformat(),
                "message": "Flow created successfully"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": f"Failed to create flow: {str(e)}",
                "flow_data": flow_data
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error creating flow: {str(e)}",
                "flow_data": flow_data
            }