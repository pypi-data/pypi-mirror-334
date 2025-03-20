from pleach.custom import Component
from pleach.inputs import MessageTextInput
from pleach.template import Output
from pleach.schema.message import Message
import json
import requests
from typing import Dict, Any, List
from datetime import datetime

class APIWorkflowExecutor(Component):
    display_name = "API Workflow Executor"
    description = "Executes API workflows with proper orchestration"
    
    inputs = [
        MessageTextInput(
            name="workflow_plan",
            display_name="Workflow Plan",
            info="The workflow execution plan from the API Processor",
            required=True
        ),
        MessageTextInput(
            name="user_inputs",
            display_name="User Inputs",
            info="Additional user inputs if required",
            required=False
        )
    ]

    outputs = [
        Output(
            name="result",
            display_name="Execution Result",
            method="execute_workflow"
        )
    ]

    def execute_workflow(self) -> Message:
        try:
            # Parse workflow plan
            if isinstance(self.workflow_plan, Message):
                workflow_plan = json.loads(self.workflow_plan.text)
            else:
                workflow_plan = json.loads(self.workflow_plan)
            
            workflow = workflow_plan.get("workflow", {})
            
            # Initialize execution results
            execution_results = {
                "workflow_execution": {
                    "name": workflow.get("name", "unnamed_workflow"),
                    "start_time": datetime.now().isoformat(),
                    "status": "running",
                    "steps_total": 0,
                    "steps_completed": 0,
                    "steps_failed": 0
                },
                "step_results": {},
                "execution_graph": {
                    "sequential": [],
                    "parallel": []
                }
            }

            # Check for missing fields
            missing_fields = workflow_plan.get("missing_fields", [])
            if missing_fields:
                execution_results["workflow_execution"].update({
                    "status": "failed",
                    "error": "Missing required fields",
                    "missing_fields": missing_fields
                })
                return Message(text=json.dumps(execution_results, indent=2))

            # Execute sequential steps
            step_results = {}
            sequential_steps = workflow["steps"].get("sequential", [])
            execution_results["workflow_execution"]["steps_total"] = len(sequential_steps)
            
            for step in sequential_steps:
                try:
                    # Process step parameters
                    processed_params = self._process_parameters(
                        step.get("parameters", {}),
                        step_results,
                        workflow_plan.get("initial_requirements", [])
                    )
                    
                    # Add to execution graph
                    execution_results["execution_graph"]["sequential"].append({
                        "step_id": step["step_id"],
                        "name": step["name"],
                        "status": "running",
                        "start_time": datetime.now().isoformat()
                    })
                    
                    # Execute step
                    step_result = self._execute_single_step(
                        step,
                        processed_params,
                        workflow_plan
                    )
                    
                    # Store result
                    step_results[step["step_id"]] = step_result
                    execution_results["step_results"][step["step_id"]] = {
                        "status": step_result["status"],
                        "start_time": datetime.now().isoformat(),
                        "end_time": datetime.now().isoformat(),
                        "produces": step.get("produces", []),
                        "consumes": step.get("consumes", []),
                        "response": step_result.get("response", {}),
                        "error": step_result.get("error")
                    }
                    
                    if step_result["status"] == "success":
                        execution_results["workflow_execution"]["steps_completed"] += 1
                    else:
                        execution_results["workflow_execution"]["steps_failed"] += 1
                        if not step.get("error_handling", {}).get("continue_on_error", False):
                            break
                        
                except Exception as e:
                    execution_results["step_results"][step["step_id"]] = {
                        "status": "error",
                        "error": str(e)
                    }
                    execution_results["workflow_execution"]["steps_failed"] += 1
                    if not step.get("error_handling", {}).get("continue_on_error", False):
                        break

            # Execute parallel steps if sequential steps succeeded
            parallel_steps = workflow["steps"].get("parallel", [])
            if (execution_results["workflow_execution"]["steps_failed"] == 0 
                and parallel_steps):
                
                execution_results["workflow_execution"]["steps_total"] += len(parallel_steps)
                
                for step in parallel_steps:
                    try:
                        # Process step parameters
                        processed_params = self._process_parameters(
                            step.get("parameters", {}),
                            step_results,
                            workflow_plan.get("initial_requirements", [])
                        )
                        
                        # Add to execution graph
                        execution_results["execution_graph"]["parallel"].append({
                            "step_id": step["step_id"],
                            "name": step["name"],
                            "status": "running",
                            "start_time": datetime.now().isoformat(),
                            "depends_on": step.get("depends_on")
                        })
                        
                        # Execute step
                        step_result = self._execute_single_step(
                            step,
                            processed_params,
                            workflow_plan
                        )
                        
                        # Store result
                        step_results[step["step_id"]] = step_result
                        execution_results["step_results"][step["step_id"]] = {
                            "status": step_result["status"],
                            "start_time": datetime.now().isoformat(),
                            "end_time": datetime.now().isoformat(),
                            "produces": step.get("produces", []),
                            "consumes": step.get("consumes", []),
                            "response": step_result.get("response", {}),
                            "error": step_result.get("error")
                        }
                        
                        if step_result["status"] == "success":
                            execution_results["workflow_execution"]["steps_completed"] += 1
                        else:
                            execution_results["workflow_execution"]["steps_failed"] += 1
                            
                    except Exception as e:
                        execution_results["step_results"][step["step_id"]] = {
                            "status": "error",
                            "error": str(e)
                        }
                        execution_results["workflow_execution"]["steps_failed"] += 1

            # Update final workflow status
            execution_results["workflow_execution"].update({
                "end_time": datetime.now().isoformat(),
                "status": "completed" if execution_results["workflow_execution"]["steps_failed"] == 0 else "failed",
                "success_rate": (
                    execution_results["workflow_execution"]["steps_completed"] /
                    execution_results["workflow_execution"]["steps_total"]
                ) * 100 if execution_results["workflow_execution"]["steps_total"] > 0 else 0
            })
            
            return Message(text=json.dumps(execution_results, indent=2))

        except Exception as e:
            return Message(text=json.dumps({
                "workflow_execution": {
                    "status": "error",
                    "error": f"Workflow execution failed: {str(e)}",
                    "error_type": str(type(e))
                },
                "step_results": {},
                "execution_graph": {
                    "sequential": [],
                    "parallel": []
                }
            }, indent=2))

    def _process_parameters(self, parameters: dict, step_results: dict, initial_requirements: List[Dict]) -> dict:
        processed_params = {}
        
        # Create lookup for initial requirements
        initial_values = {
            req["field"]: req["extracted_value"]
            for req in initial_requirements
        }
        
        for param_type, params in parameters.items():
            processed_params[param_type] = {}
            for key, value in params.items():
                if isinstance(value, str) and value.startswith("{response."):
                    try:
                        parts = value[10:-1].split(".")
                        step_id = parts[0]
                        field = parts[1]
                        processed_params[param_type][key] = step_results[step_id]["response"][field]
                    except (KeyError, IndexError) as e:
                        raise ValueError(f"Failed to map step parameter: {value}. Error: {str(e)}")
                elif key in initial_values:
                    processed_params[param_type][key] = initial_values[key]
                else:
                    processed_params[param_type][key] = value
                    
        return processed_params

    def _execute_single_step(self, step: Dict[str, Any], processed_params: Dict[str, Any], workflow_plan: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Get base URL from workflow plan
            swagger_analysis = workflow_plan["workflow"].get("swagger_analysis", {})
            base_url = swagger_analysis.get("base_url", "").strip('/')
            base_path = swagger_analysis.get("base_path", "").strip('/')
            endpoint = step["endpoint"].strip('/')
            method = step["method"]
            
            if not base_url:
                raise ValueError("Missing base_url in workflow swagger_analysis")
                
            # Construct URL parts ensuring no double slashes
            url_parts = [
                "https:/",
                base_url,
                base_path if base_path else None,
                endpoint
            ]
            
            # Filter out None values and join with single slash
            full_url = '/'.join(filter(None, url_parts))
            
            # Extract parameters by type
            body_params = processed_params.get("body", {})
            query_params = processed_params.get("query", {})
            path_params = processed_params.get("path", {})
            
            # Replace path parameters in URL
            try:
                for param_name, param_value in path_params.items():
                    placeholder = f"{{{param_name}}}"
                    if placeholder in full_url:
                        full_url = full_url.replace(placeholder, str(param_value))
                        
                if '{' in full_url or '}' in full_url:
                    unreplaced_params = re.findall(r'{([^}]+)}', full_url)
                    raise ValueError(f"Unresolved path parameters in URL: {unreplaced_params}")
            except Exception as e:
                raise ValueError(f"Error replacing path parameters: {str(e)}")

            # Make the request with retry logic if specified
            max_retries = step.get("error_handling", {}).get("max_retries", 0)
            retry_count = 0
            
            while retry_count <= max_retries:
                try:
                    headers = {"Content-Type": "application/json"}
                    response = self._make_request(
                        method, 
                        full_url, 
                        body_params, 
                        query_params, 
                        headers
                    )
                    
                    return {
                        "status": "success",
                        "url": full_url,
                        "method": method,
                        "response": response,
                        "retries": retry_count
                    }
                
                except Exception as e:
                    retry_count += 1
                    if retry_count > max_retries:
                        raise
                    
        except Exception as e:
            return {
                "status": "error",
                "url": full_url if 'full_url' in locals() else "URL construction failed",
                "method": method if 'method' in locals() else "unknown",
                "error": str(e),
                "retries": retry_count if 'retry_count' in locals() else 0,
                "debug_info": {
                    "base_url": base_url if 'base_url' in locals() else None,
                    "base_path": base_path if 'base_path' in locals() else None,
                    "endpoint": endpoint if 'endpoint' in locals() else None,
                    "path_params": path_params if 'path_params' in locals() else None,
                    "constructed_url_parts": url_parts if 'url_parts' in locals() else None
                }
            }

    def _make_request(self, method: str, url: str, body_params: dict, query_params: dict, headers: dict) -> dict:
        """Make HTTP request with appropriate method and parameters"""
        if method == "GET":
            response = requests.get(url, params=query_params, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=body_params, params=query_params, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=body_params, params=query_params, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, params=query_params, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()