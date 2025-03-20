import asyncio
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import aiofiles
import aiofiles.os as aiofiles_os
import httpx
import validators

from pleach.base.curl.parse import parse_context
from pleach.custom import Component
from pleach.io import (
    BoolInput,
    DataInput,
    DropdownInput,
    FloatInput,
    IntInput,
    MessageTextInput,
    MultilineInput,
    Output,
    StrInput,
    TableInput,
)
from pleach.schema import Data
from pleach.schema.message import Message
from pleach.schema.dotdict import dotdict

class APIExecutor(Component):
    display_name = "API Request Executor"
    description = "Make HTTP requests with JSON mapping and table inputs"
    icon = "Globe"
    name = "APIRequestExecutor"

    default_keys = ["urls", "method", "query_params"]

    inputs = [
        MessageTextInput(
            name="urls",
            display_name="URLs",
            list=True,
            info="Enter one or more URLs, separated by commas.",
            advanced=False,
            tool_mode=True,
        ),
        MessageTextInput(
            name="json_input",
            display_name="JSON Input (Optional)",
            info="Provide JSON as a string. If given, it will be stored in 'temp' and used for mapping.",
            value="",
            tool_mode=True,
            advanced=False,
        ),
        MessageTextInput(
            name="mapping_expression",
            display_name="Mapping Expression",
            info="Define how to transform the JSON using 'temp'. Optional if using Body table. Example: {'firstName': temp['employee']['name']}",
            value="",
            tool_mode=True,
            advanced=False,
        ),
        MultilineInput(
            name="curl",
            display_name="cURL",
            info=(
                "Paste a curl command to populate the fields. "
                "This will fill in the dictionary fields for headers and body."
            ),
            advanced=True,
            real_time_refresh=True,
            tool_mode=True,
        ),
        DropdownInput(
            name="method",
            display_name="Method",
            options=["GET", "POST", "PATCH", "PUT", "DELETE"],
            info="The HTTP method to use.",
            real_time_refresh=True,
        ),
        BoolInput(
            name="use_curl",
            display_name="Use cURL",
            value=False,
            info="Enable cURL mode to populate fields from a cURL command.",
            real_time_refresh=True,
        ),
        DataInput(
            name="query_params",
            display_name="Query Parameters",
            info="The query parameters to append to the URL.",
            advanced=True,
        ),
        TableInput(
            name="body",
            display_name="Body",
            info="The body to send with the request (for POST, PATCH, PUT). Optional if using Mapping Expression. Can reference temp['key'] for dynamic values.",
            table_schema=[
                {
                    "name": "key",
                    "display_name": "Key",
                    "type": "str",
                    "description": "Parameter name",
                },
                {
                    "name": "value",
                    "display_name": "Value",
                    "description": "Parameter value (can reference temp['key'])",
                },
            ],
            value=[],
            input_types=["Data"],
            advanced=True,
        ),
        TableInput(
            name="headers",
            display_name="Headers",
            info="The headers to send with the request. Can reference temp['key'] for dynamic values.",
            table_schema=[
                {
                    "name": "key",
                    "display_name": "Header",
                    "type": "str",
                    "description": "Header name",
                },
                {
                    "name": "value",
                    "display_name": "Value",
                    "type": "str",
                    "description": "Header value (can reference temp['key'])",
                },
            ],
            value=[],
            advanced=True,
            input_types=["Data"],
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            value=5,
            info="The timeout to use for the request.",
            advanced=True,
        ),
        BoolInput(
            name="follow_redirects",
            display_name="Follow Redirects",
            value=True,
            info="Whether to follow http redirects.",
            advanced=True,
        ),
        BoolInput(
            name="save_to_file",
            display_name="Save to File",
            value=False,
            info="Save the API response to a temporary file",
            advanced=True,
        ),
        BoolInput(
            name="include_httpx_metadata",
            display_name="Include HTTPx Metadata",
            value=False,
            info=(
                "Include properties such as headers, status_code, response_headers, "
                "and redirection_history in the output."
            ),
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Message", name="message", method="response_message"),
        Output(display_name="Data", name="data", method="make_requests"),
    ]

    def parse_json_input(self):
        """Parses JSON input if provided and returns a dictionary."""
        if self.json_input:
            try:
                return json.loads(self.json_input)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format in input")
        return {}

    def evaluate_mapping(self, temp):
        """Evaluates the user-defined mapping expression."""
        if self.mapping_expression:
            try:
                return eval(self.mapping_expression, {"temp": temp})
            except Exception as e:
                raise ValueError(f"Mapping error: {str(e)}")
        return temp

    async def response_message(self) -> Message:
        """Processes the request and returns the API response as a message."""
        try:
            responses = await self.make_requests()
            
            # Get the first response since we typically expect one
            response = responses[0] if responses else None
            if not response:
                raise ValueError("No response received")

            data = response.data
            if "error" in data:
                return await Message.create(
                    text=json.dumps({"error": data["error"]}),
                    sender="EnhancedAPIRequest",
                    sender_name="API Response",
                    session_id=None,
                    properties={"type": "json"},
                )

            # Extract the result from the response
            result = data.get("result", "")
            
            # If result is already a dict, use it directly
            if isinstance(result, dict):
                response_json = result
            # If result is a string that looks like JSON, parse it
            elif isinstance(result, str):
                try:
                    response_json = json.loads(result)
                except json.JSONDecodeError:
                    response_json = {"result": result}
            else:
                response_json = {"result": result}

            # Create message with the response
            message = await Message.create(
                text=json.dumps(response_json),
                sender="EnhancedAPIRequest",
                sender_name="API Response",
                session_id=None,
                properties={"type": "json"},
            )
            self.status = message
            return message

        except Exception as e:
            return await Message.create(
                text=json.dumps({"error": str(e)}),
                sender="EnhancedAPIRequest",
                sender_name="API Response",
                session_id=None,
                properties={"type": "json"},
            )

    def _is_valid_key_value_item(self, item: Any) -> bool:
        """Check if an item is a valid key-value dictionary."""
        return isinstance(item, dict) and "key" in item and "value" in item

    def parse_curl(self, curl: str, build_config: dotdict) -> dotdict:
        """Parse a cURL command and update build configuration."""
        try:
            parsed = parse_context(curl)

            # Update basic configuration
            build_config["urls"]["value"] = [parsed.url]
            build_config["method"]["value"] = parsed.method.upper()
            build_config["headers"]["advanced"] = True
            build_config["body"]["advanced"] = True

            # Process headers
            headers_list = [{"key": k, "value": v} for k, v in parsed.headers.items()]
            build_config["headers"]["value"] = headers_list

            if headers_list:
                build_config["headers"]["advanced"] = False

            # Process body data
            if not parsed.data:
                build_config["body"]["value"] = []
            elif parsed.data:
                try:
                    json_data = json.loads(parsed.data)
                    if isinstance(json_data, dict):
                        body_list = [
                            {"key": k, "value": json.dumps(v) if isinstance(v, (dict, list)) else str(v)}
                            for k, v in json_data.items()
                        ]
                        build_config["body"]["value"] = body_list
                        build_config["body"]["advanced"] = False
                    else:
                        build_config["body"]["value"] = [{"key": "data", "value": json.dumps(json_data)}]
                        build_config["body"]["advanced"] = False
                except json.JSONDecodeError:
                    build_config["body"]["value"] = [{"key": "data", "value": parsed.data}]
                    build_config["body"]["advanced"] = False

        except Exception as exc:
            msg = f"Error parsing curl: {exc}"
            self.log(msg)
            raise ValueError(msg) from exc

        return build_config

    def _process_body(self, body: Any, temp: dict) -> dict:
        """Process the body input into a valid dictionary with temp variable support."""
        if body is None:
            return {}
        
        if isinstance(body, dict):
            return {k: eval(str(v), {"temp": temp}) if isinstance(v, str) and "temp" in v else v 
                   for k, v in body.items()}
        
        if isinstance(body, list):
            processed_dict = {}
            for item in body:
                if not self._is_valid_key_value_item(item):
                    continue
                key = item["key"]
                value = item["value"]
                try:
                    # Evaluate if value references temp
                    processed_value = eval(str(value), {"temp": temp}) if isinstance(value, str) and "temp" in value else value
                    processed_dict[key] = processed_value
                except Exception as e:
                    self.log(f"Failed to process value for key {key}: {e}")
                    processed_dict[key] = value
            return processed_dict

        return {}

    def _process_headers(self, headers: Any, temp: dict) -> dict:
        """Process headers with temp variable support."""
        if headers is None:
            return {}
            
        if isinstance(headers, list):
            processed_headers = {}
            for item in headers:
                if not self._is_valid_key_value_item(item):
                    continue
                key = item["key"]
                value = item["value"]
                try:
                    # Evaluate if value references temp
                    processed_value = eval(str(value), {"temp": temp}) if isinstance(value, str) and "temp" in value else value
                    processed_headers[key] = processed_value
                except Exception as e:
                    self.log(f"Failed to process header value for key {key}: {e}")
                    processed_headers[key] = value
            return processed_headers
            
        return headers if isinstance(headers, dict) else {}

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "use_curl":
            build_config = self._update_curl_mode(build_config, use_curl=field_value)
            ### RESET LOGIC I NEED TO CHECK AGAIN ###
            # # Fields that should not be reset
            # preserve_fields = {"timeout", "follow_redirects", "save_to_file", "include_httpx_metadata", "use_curl"}

            # # Mapping between input types and their reset values
            # type_reset_mapping = {
            #     TableInput: [],
            #     BoolInput: False,
            #     IntInput: 0,
            #     FloatInput: 0.0,
            #     MessageTextInput: "",
            #     StrInput: "",
            #     MultilineInput: "",
            #     DropdownInput: "GET",
            #     DataInput: {},
            # }

            # for input_field in self.inputs:
            #     # Only reset if field is not in preserve list
            #     if input_field.name not in preserve_fields:
            #         reset_value = type_reset_mapping.get(type(input_field), None)
            #         build_config[input_field.name]["value"] = reset_value
        elif field_name == "method" and not self.use_curl:
            build_config = self._update_method_fields(build_config, field_value)
        elif field_name == "curl" and self.use_curl and field_value:
            build_config = self.parse_curl(field_value, build_config)
        return build_config

    def _update_curl_mode(self, build_config: dotdict, *, use_curl: bool) -> dotdict:
        always_visible = ["method", "use_curl"]

        for field in self.inputs:
            field_name = field.name
            field_config = build_config.get(field_name)
            if isinstance(field_config, dict):
                if field_name in always_visible:
                    field_config["advanced"] = False
                elif field_name == "urls":
                    field_config["advanced"] = use_curl
                elif field_name == "curl":
                    field_config["advanced"] = not use_curl
                    field_config["real_time_refresh"] = use_curl
                elif field_name in ["body", "headers"]:
                    field_config["advanced"] = True
                else:
                    field_config["advanced"] = use_curl
            else:
                self.log(f"Expected dict for build_config[{field_name}], got {type(field_config).__name__}")

        if not use_curl:
            current_method = build_config.get("method", {}).get("value", "GET")
            build_config = self._update_method_fields(build_config, current_method)

        return build_config

    def _update_method_fields(self, build_config: dotdict, method: str) -> dotdict:
        # Fields that are always visible
        common_fields = ["urls", "method", "use_curl", "json_input", "mapping_expression"]
        
        # Fields visible for POST/PUT/PATCH methods
        request_body_fields = ["body"]
        
        # Headers should be visible for all methods
        header_fields = ["headers"]
        
        # Advanced fields
        always_advanced_fields = [
            "timeout",
            "follow_redirects",
            "save_to_file",
            "include_httpx_metadata",
        ]

        for field in self.inputs:
            field_name = field.name
            field_config = build_config.get(field_name)
            if isinstance(field_config, dict):
                if field_name in common_fields:
                    # Always visible fields
                    field_config["advanced"] = False
                elif field_name in header_fields:
                    # Headers always visible but in advanced
                    field_config["advanced"] = False
                elif field_name in request_body_fields:
                    # Show for POST/PUT/PATCH, hide for others
                    field_config["advanced"] = method not in ["POST", "PUT", "PATCH"]
                elif field_name in always_advanced_fields:
                    field_config["advanced"] = True
                else:
                    field_config["advanced"] = True
            else:
                self.log(f"Expected dict for build_config[{field_name}], got {type(field_config).__name__}")

        return build_config

    async def make_request(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        headers: dict | None = None,
        body: Any = None,
        timeout: int = 5,
        *,
        follow_redirects: bool = True,
        save_to_file: bool = False,
        include_httpx_metadata: bool = False,
    ) -> Data:
        """Handle an individual API request.

        Args:
            client: The HTTP client to use
            method: HTTP method
            url: Request URL
            headers: Request headers
            body: Request body
            timeout: Request timeout
            follow_redirects: Whether to follow redirects
            save_to_file: Whether to save response to file
            include_httpx_metadata: Whether to include extra metadata
        Returns:
            Data object containing response or error
        """
        method = method.upper()
        if method not in {"GET", "POST", "PATCH", "PUT", "DELETE"}:
            msg = f"Unsupported method: {method}"
            raise ValueError(msg)

        try:
            if query_params := self.process_query_params():
                from urllib.parse import urlencode
                query_string = urlencode(query_params)
                url = f"{url}?{query_string}"

            request_args = {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "follow_redirects": follow_redirects,
            }

            # Only send body if method requires it
            if body and method in {"POST", "PUT", "PATCH"}:
                request_args["json"] = body

            response = await client.request(method, **request_args)
            
            redirection_history = [
                {
                    "url": redirect.headers.get("Location", str(redirect.url)),
                    "status_code": redirect.status_code,
                }
                for redirect in response.history
            ]

            is_binary, file_path = await self._response_info(response, with_file_path=save_to_file)
            response_headers = self._headers_to_dict(response.headers)

            metadata: dict[str, Any] = {
                "source": url,
            }

            if save_to_file:
                mode = "wb" if is_binary else "w"
                encoding = response.encoding if mode == "w" else None
                if file_path:
                    await aiofiles_os.makedirs(file_path.parent, exist_ok=True)
                    if is_binary:
                        async with aiofiles.open(file_path, "wb") as f:
                            await f.write(response.content)
                            await f.flush()
                    else:
                        async with aiofiles.open(file_path, "w", encoding=encoding) as f:
                            await f.write(response.text)
                            await f.flush()
                    metadata["file_path"] = str(file_path)

                if include_httpx_metadata:
                    metadata.update(
                        {
                            "headers": headers,
                            "status_code": response.status_code,
                            "response_headers": response_headers,
                            **({"redirection_history": redirection_history} if redirection_history else {}),
                        }
                    )
                return Data(data=metadata)

            if is_binary:
                result = response.content
            else:
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    self.log("Failed to decode JSON response")
                    result = response.text

            metadata.update({"result": result})

            if include_httpx_metadata:
                metadata.update(
                    {
                        "headers": headers,
                        "status_code": response.status_code,
                        "response_headers": response_headers,
                        **({"redirection_history": redirection_history} if redirection_history else {}),
                    }
                )
            return Data(data=metadata)
        except httpx.TimeoutException:
            return Data(
                data={
                    "source": url,
                    "headers": headers,
                    "status_code": 408,
                    "error": "Request timed out",
                },
            )
        except Exception as exc:
            self.log(f"Error making request to {url}: {exc}")
            return Data(
                data={
                    "source": url,
                    "headers": headers,
                    "status_code": 500,
                    "error": str(exc),
                },
            )

    def add_query_params(self, url: str, params: dict) -> str:
        """Add query parameters to URL.
        
        Args:
            url: Base URL
            params: Query parameters to add
        Returns:
            URL with query parameters
        """
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    def process_query_params(self):
        """Process query parameters from input."""
        if isinstance(self.query_params, str):
            try:
                return json.loads(self.query_params)
            except json.JSONDecodeError:
                return {}
        return self.query_params if self.query_params else {}

    async def _response_info(
        self, response: httpx.Response, *, with_file_path: bool = False
    ) -> tuple[bool, Path | None]:
        """Determine if response is binary and generate file path if needed."""
        content_type = response.headers.get("Content-Type", "")
        is_binary = "application/octet-stream" in content_type or "application/binary" in content_type

        if not with_file_path:
            return is_binary, None

        component_temp_dir = Path(tempfile.gettempdir()) / self.__class__.__name__
        await aiofiles_os.makedirs(component_temp_dir, exist_ok=True)

        filename = None
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            filename_match = re.search(r'filename="(.+?)"', content_disposition)
            if filename_match:
                filename = filename_match.group(1)

        if not filename:
            url_path = urlparse(str(response.request.url) if response.request else "").path
            base_name = Path(url_path).name
            if not base_name:
                base_name = "response"

            content_type_to_extension = {
                "text/plain": ".txt",
                "application/json": ".json",
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "application/octet-stream": ".bin",
            }
            extension = content_type_to_extension.get(content_type, ".bin" if is_binary else ".txt")
            filename = f"{base_name}{extension}"

        file_path = component_temp_dir / filename

        try:
            async with aiofiles.open(file_path, "x"):
                pass
        except FileExistsError:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
            file_path = component_temp_dir / f"{timestamp}-{filename}"

        return is_binary, file_path

    def _headers_to_dict(self, headers: httpx.Headers) -> dict[str, str]:
        """Convert HTTP headers to dictionary."""
        return {k.lower(): v for k, v in headers.items()}

    async def make_requests(self) -> list[Data]:
        """Process and make all API requests."""
        method = self.method
        urls = [url.strip() for url in self.urls if url.strip()]
        timeout = self.timeout
        follow_redirects = self.follow_redirects
        save_to_file = self.save_to_file
        include_httpx_metadata = self.include_httpx_metadata

        # For POST/PUT/PATCH, verify at least one of mapping_expression or body table is provided
        if method in ["POST", "PUT", "PATCH"]:
            has_mapping = bool(self.mapping_expression and self.mapping_expression.strip())
            has_body = bool(self.body and len(self.body) > 0)
            if not has_mapping and not has_body:
                raise ValueError("For POST/PUT/PATCH requests, either Mapping Expression or Body table must be provided")

        # Parse JSON input and apply mapping
        temp = self.parse_json_input()
        mapped_data = self.evaluate_mapping(temp)

        # Process headers and body with temp support
        headers = self._process_headers(self.headers, temp)
        body = self._process_body(self.body, temp)

        if self.use_curl and self.curl:
            self._build_config = self.parse_curl(self.curl, dotdict())

        invalid_urls = [url for url in urls if not validators.url(url)]
        if invalid_urls:
            msg = f"Invalid URLs provided: {invalid_urls}"
            raise ValueError(msg)

        # Process query parameters
        if isinstance(self.query_params, str):
            query_params = dict(parse_qsl(self.query_params))
        else:
            query_params = self.query_params.data if self.query_params else {}

        bodies = [body] * len(urls)
        urls = [self.add_query_params(url, query_params) for url in urls]

        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                *[
                    self.make_request(
                        client,
                        method,
                        u,
                        headers,
                        rec,
                        timeout,
                        follow_redirects=follow_redirects,
                        save_to_file=save_to_file,
                        include_httpx_metadata=include_httpx_metadata,
                    )
                    for u, rec in zip(urls, bodies, strict=False)
                ]
            )
        self.status = results
        return results