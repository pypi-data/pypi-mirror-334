from pleach.custom import Component
from pleach.inputs import MessageTextInput
from pleach.template import Output
from pleach.schema.message import Message
import json
import requests
from typing import Dict

class APIProcessor(Component):
    display_name = "API Workflow Processor"
    description = "Processes API specifications into executable workflows"
    
    inputs = [
        MessageTextInput(
            name="spec_url",
            display_name="Specification URL",
            info="URL to fetch the Swagger/OpenAPI specification",
            required=True
        ),
        MessageTextInput(
            name="chat_input",
            display_name="Chat Input",
            info="User's workflow request",
            required=True
        )
    ]

    outputs = [
        Output(
            name="workflow_plan",
            display_name="Workflow Plan",
            method="process_and_generate"
        )
    ]

    def parse_swagger(self, url: str) -> Dict:
        try:
            if not url.strip():
                raise ValueError("URL cannot be empty")

            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
                
            response = requests.get(url)
            response.raise_for_status()
            swagger_spec = response.json()

            base_info = {
                "base_url": swagger_spec.get("host", ""),
                "base_path": swagger_spec.get("basePath", ""),
                "endpoints": []
            }

            definitions = swagger_spec.get("definitions", {})
            
            for path, methods in swagger_spec.get("paths", {}).items():
                for method, details in methods.items():
                    if method.lower() == "parameters":
                        continue
                    
                    endpoint_info = {
                        "path": path,
                        "method": method.upper(),
                        "responses": details.get("responses", {}),
                        "requires_auth": bool(details.get("security", [])),
                        "summary": details.get("summary", ""),
                        "operation_id": details.get("operationId", ""),
                        "description": details.get("description", ""),
                        "produces": details.get("produces", []),
                        "consumes": details.get("consumes", [])
                    }

                    required_params = []
                    request_body_schema = None
                    
                    for param in details.get("parameters", []):
                        if param.get("in") == "body" and param.get("schema", {}).get("$ref"):
                            schema_ref = param["schema"]["$ref"].split("/")[-1]
                            schema = definitions.get(schema_ref, {})
                            required_fields = schema.get("required", [])
                            properties = schema.get("properties", {})
                            
                            request_body_schema = {
                                "type": "object",
                                "required": required_fields,
                                "properties": properties
                            }
                            
                            for field in required_fields:
                                prop = properties.get(field, {})
                                param_info = {
                                    "field": field,
                                    "type": prop.get("type", "string"),
                                    "description": prop.get("description", f"Required field: {field}"),
                                    "format": prop.get("format", ""),
                                    "in": "body"
                                }
                                
                                if prop.get("type") == "array":
                                    param_info["items"] = prop.get("items", {})
                                
                                required_params.append(param_info)
                        else:
                            if param.get("required", False):
                                param_info = {
                                    "field": param["name"],
                                    "type": param.get("type", "string"),
                                    "description": param.get("description", f"Required parameter: {param['name']}"),
                                    "in": param.get("in", "query"),
                                    "format": param.get("format", "")
                                }
                                
                                if param.get("type") == "array":
                                    param_info["items"] = param.get("items", {})
                                
                                required_params.append(param_info)

                    endpoint_info["required_parameters"] = required_params
                    endpoint_info["request_body_schema"] = request_body_schema
                    base_info["endpoints"].append(endpoint_info)

            return {"swagger_analysis": base_info}
                
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to fetch Swagger spec: {str(e)}",
                "swagger_analysis": {
                    "base_url": "",
                    "base_path": "",
                    "endpoints": []
                }
            }
        except Exception as e:
            return {
                "error": f"Failed to parse Swagger: {str(e)}",
                "swagger_analysis": {
                    "base_url": "",
                    "base_path": "",
                    "endpoints": []
                }
            }

    def process_and_generate(self) -> Message:
        try:
            analysis_data = self.parse_swagger(self.spec_url)
            
            template = """Based on the following API specification and user request, generate a workflow-style execution plan. Think of this as an API orchestration workflow where each step must be clearly defined with its data requirements and dependencies.

API Specification:
{swagger_analysis}

User Request: {user_query}

Generate a workflow plan following these rules:


1. Data Requirements:
{{
  "initial_requirements": [
     // Get all the required and optional fields needed to execute the workflow
    {{
      "field": "data_field_name",
      "type": "data_type",
      "description": "Clear description of the data needed",
      "extracted_value": "actual_value_from_request"
      "required":"true|false"
    }}
  ],
  "missing_fields": [
    // Only fields that couldn't be extracted from the request
  ]
}}

2. Workflow Definition:
{{
  "workflow": {{
    "name": "generated_from_user_request",
    "description": "Detailed description of what this workflow does",
    "type": "sequential|parallel|mixed",
    "version": "1.0",
    "swagger_analysis": {{  // MUST include this
      "base_url": "from_swagger_spec", // Must come from swagger spec
      "base_path": "from_swagger_spec" // Must get from swagger spec
    }},
    "steps": {{
      "sequential": [
        {{
          "step_id": "unique_step_identifier",
          "name": "human_readable_name",
          "endpoint": "/api/path",
          "method": "HTTP_METHOD",
          "operation_id": "unique_operation_name",
          "parameters": {{
            "body": {{
              "field": "direct_value_no_templates"
            }},
            "path": {{
              "param": "value_or_step_reference"
            }},
            "query": {{
              "param": "value_or_step_reference"
            }}
          }},
          "depends_on": null,
          "produces": ["output_fields"],
          "consumes": ["input_fields"],
          "error_handling": {{
            "retry": boolean,
            "max_retries": number,
            "fallback": "step_id_or_null"
          }}
        }}
      ],
      "parallel": [
        {{
          // Same structure as sequential steps
          "step_id": "parallel_step_id",
          "depends_on": "sequential_step_id"
        }}
      ]
    }}
  }}
}}

Rules for Workflow Construction:

1. Step Identification:
   - Each step must have unique step_id
   - Clear, descriptive names for human readability
   - Proper endpoint and method mapping

2. Data Flow:
   - Parameters must be properly categorized (body, path, query)
   - Use actual values extracted from user request
   - Use step references in format: {{response.step_id.field}}
   - No template placeholders like {{field_name}}

3. Dependencies:
   - Sequential steps can depend on previous sequential steps
   - Parallel steps can only depend on sequential steps
   - No circular dependencies
   - No dependencies between parallel steps

4. Error Handling:
   - Each step should specify retry behavior
   - Can define fallback steps
   - Must handle required vs optional dependencies
  
Example Response Structure:
{{
  "initial_requirements": [],
  "missing_fields": [],
  "workflow": {{
    "name": "create_and_verify_pet",
    "description": "Creates a pet and verifies its creation",
    "type": "sequential",
    "swagger_analysis": {{  // MUST include this
        "base_url": "petstore.swagger.io",
        "base_path": "/v2"
    }},
    "steps": {{
      "sequential": [
        {{
          "step_id": "create_pet",
          "name": "Create New Pet",
          "endpoint": "/pet",
          "method": "POST",
          "parameters": {{
            "body": {{
              "name": "actual_name_from_request",
              "status": "available"
            }}
          }},
          {{
        "step_id": "update_pet",
        "parameters": {{
          "path": {{
            "petId": "{{response.create_pet.id}}"  // Reference previous step
          }}
        }},
        "depends_on": "create_pet"
      }},
          "produces": ["id", "name", "status"],
          "error_handling": {{
            "retry": true,
            "max_retries": 3
          }}
        }}
      ],
      "parallel": []
    }}
  }}
}}

IMPORTANT:
1. Return ONLY the JSON object, no explanations or descriptions
2. Use actual values from user request, not reference templates
3. Map values directly into parameters where needed
4. Make sure there is not single explanation or words other then a json object

CRITICAL: Return ONLY the JSON object. No explanations, descriptions, markdown formatting, or any other text.
"""

            formatted_prompt = template.format(
                swagger_analysis=json.dumps(analysis_data["swagger_analysis"], indent=2),
                user_query=self.chat_input
            )
            
            return Message(text=formatted_prompt)

        except Exception as e:
            return Message(text=f"Error processing workflow request: {str(e)}")