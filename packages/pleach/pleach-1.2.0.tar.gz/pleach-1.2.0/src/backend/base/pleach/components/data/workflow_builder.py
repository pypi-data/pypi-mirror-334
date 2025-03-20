from pleach.custom import Component
from pleach.io import MessageTextInput, Output, IntInput, StrInput
from pleach.schema import Data
import json
import httpx
from typing import Dict, Any, Optional

class WorkflowBuilder(Component):
    display_name = "Workflow Builder"
    description = "Creates workflow nodes from LLM response"
    icon = "workflow"
    name = "WorkflowBuilder"

    inputs = [
        MessageTextInput(
            name="workflow_spec",
            display_name="Workflow Specification",
            info="LLM response containing workflow specification",
            value="",
        )
    ]

    outputs = [
        Output(
            name="workflow",
            display_name="Generated Workflow",
            method="build_workflow",
        )
    ]

    def build_workflow(self) -> Data:
        try:
            # Parse workflow specification
            spec = json.loads(self.workflow_spec)
            
            nodes = []
            edges = []
            position = {"x": 100, "y": 100}
            
            # Process sequential steps
            for step in spec["workflow"]["steps"]["sequential"]:
                node = self._create_node(step, position, spec["workflow"]["swagger_analysis"])
                nodes.append(node)
                position["x"] += 250
                
                # Add edge if not first node
                if len(nodes) > 1:
                    edges.append({
                        "source": nodes[-2]["id"],
                        "target": node["id"],
                        "sourceHandle": "api_result",
                        "targetHandle": "input_data",
                    })
            
            # Process parallel steps
            position["y"] += 200
            position["x"] = 100
            
            for step in spec["workflow"]["steps"]["parallel"]:
                node = self._create_node(step, position, spec["workflow"]["swagger_analysis"])
                nodes.append(node)
                position["x"] += 250
                
                # Add edge from dependency
                if "depends_on" in step:
                    for prev_node in nodes:
                        if prev_node["id"] == step["depends_on"]:
                            edges.append({
                                "source": prev_node["id"],
                                "target": node["id"],
                                "sourceHandle": "api_result",
                                "targetHandle": "input_data",
                            })
            
            workflow = {
                "nodes": nodes,
                "edges": edges
            }
            
            return Data(value=workflow)
            
        except Exception as e:
            return Data(value={"error": str(e)})

    def _create_node(self, step: Dict, position: Dict, swagger_info: Dict) -> Dict:
        """Create a node configuration"""
        endpoint = f"{swagger_info['base_url']}{swagger_info['base_path']}{step['endpoint']}"
        
        return {
            "id": step["step_id"],
            "type": "APICallNode",
            "position": position.copy(),
            "data": {
                "endpoint": endpoint,
                "method": step["method"],
                "input_data": json.dumps(step["parameters"]),
                "retry_count": step.get("error_handling", {}).get("max_retries", 3),
                "name": step["name"],
            }
        }