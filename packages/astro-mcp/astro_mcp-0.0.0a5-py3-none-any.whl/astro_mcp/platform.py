"""
MCP server for Astro APIs

This module implements an MCP server that provides access to Astro Platform API.
"""

import json
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Iterable

from mcp.types import Tool, TextContent
from mcp.server.fastmcp import FastMCP



class AstroServer(FastMCP):
    """MCP server for interacting with Astro API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the server with API credentials.

        Args:
            api_key: API key for authentication. Defaults to ASTRO_API_KEY env var.
        """
        super().__init__(
            name="astro-mcp",
            version="0.1.0", 
            instructions="Astronomer Platform API client using Model Context Protocol",
        )
        
        # Set up API credentials
        self.base_url = "https://api.astronomer.io/platform/v1beta1"
        self.api_key = api_key or os.environ.get("ASTRO_API_KEY")

        if not self.api_key:
            raise ValueError("API key is required. Please set ASTRO_API_KEY environment variable or provide an API key.")
        
        # Try to load bundled API spec from installed package first
        try:
            import importlib.resources as pkg_resources
            from importlib.abc import Traversable
            
            # Handle both Python 3.9+ and older versions
            try:
                # For Python 3.9+
                spec_resource: Traversable = pkg_resources.files("astro_mcp").joinpath("specs/platform_api_spec.yaml")
                with spec_resource.open("r") as f:
                    self.spec = yaml.safe_load(f)
            except (ImportError, AttributeError):
                # For older Python versions or different package structure
                raise FileNotFoundError("Could not load spec from package resources")
        except (ImportError, FileNotFoundError):
            # Fall back to loading from local file system
            root_dir = Path(__file__).parent.parent
            spec_path = root_dir / "astro_mcp" / "specs" / "platform_api_spec.yaml"
            
            if not spec_path.exists():
                raise FileNotFoundError(
                    f"API spec not found at {spec_path}. "
                    "Run 'python scripts/download_specs.py' to download it."
                )
            
            with open(spec_path, "r") as f:
                self.spec = yaml.safe_load(f)

    async def list_tools(self) -> list[Tool]:
        """List all available Astro API tools."""
        print("Listing tools")
        tools = []
        for path, path_item in self.spec.get("paths", {}).items():
            for method, operation in path_item.items():
                if method.lower() not in ("get", "post", "put", "delete", "patch"):
                    continue
                
                operation_id = operation.get("operationId")
                if not operation_id:
                    continue
                
                tool_name = f"astro_{operation_id}"
                description = operation.get("summary", "") or operation.get("description", "")

                parameters_schema = {
                    "type": "object",
                    "properties": {},
                    "required": []
                }

                for param in operation.get("parameters", []):
                    if param.get("in") == "path":
                        param_name = param.get("name")
                        param_schema = param.get("schema", {})
                        parameters_schema["properties"][param_name] = param_schema
                        if param.get("required", False):
                            parameters_schema["required"].append(param_name)

                for param in operation.get("parameters", []):
                    if param.get("in") == "query":
                        param_name = param.get("name")
                        param_schema = param.get("schema", {})
                        parameters_schema["properties"][param_name] = param_schema
                        if param.get("required", False):
                            parameters_schema["required"].append(param_name)

                if "requestBody" in operation:
                    content = operation["requestBody"].get("content", {})
                    if "application/json" in content:
                        body_schema = content["application/json"].get("schema", {})
                        parameters_schema["properties"]["body"] = body_schema
                        if operation["requestBody"].get("required", False):
                            parameters_schema["required"].append("body")

                tools.append(Tool(
                    name=tool_name,
                    description=description,
                    inputSchema=parameters_schema
                ))

        return tools
    
    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Iterable[TextContent]:
        """Handle tool calls."""
        print(f"Calling tool: {tool_name} with args: {args}")
        # Special case for listing available tools
        if tool_name == "list_tools":
            tools_list = await self.list_tools()
            tools_info = [
                {
                    "name": tool.name,
                    "description": tool.description
                }
                for tool in tools_list
            ]
            
            return [TextContent(
                type="text",
                text=json.dumps({"tools": tools_info}, indent=2)
            )]
        
        # Handle API calls
        if tool_name.startswith("astro_"):
            response_data = await self._handle_api_call(tool_name, args)
            return [TextContent(
                type="text",
                text=json.dumps(response_data, indent=2)
            )]
        
        # Unknown tool
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {tool_name}"}, indent=2)
        )]
    
    async def _handle_api_call(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an API call.
        
        Args:
            tool_name: The name of the tool to call
            args: The parameters for the call
            
        Returns:
            Response data from the API call
        """
        import aiohttp
        
        # Check API key at call time
        if not self.api_key:
            return {
                "error": "API key required. Please set ASTRO_API_KEY environment variable or provide an API key."
            }
            
        # Extract the operation ID from the tool name
        operation_id = tool_name.replace("astro_", "")
        
        # Find the operation in the spec
        operation_info = None
        operation_path = None
        operation_method = None
        
        for path, path_item in self.spec.get("paths", {}).items():
            for method, operation in path_item.items():
                if method.lower() not in ("get", "post", "put", "delete", "patch"):
                    continue
                
                if operation.get("operationId") == operation_id:
                    operation_info = operation
                    operation_path = path
                    operation_method = method
                    break
            
            if operation_info:
                break
        
        if not operation_info:
            return {"error": f"Unknown operation: {operation_id}"}
        
        # Process path parameters
        url = operation_path
        for param in operation_info.get("parameters", []):
            if param.get("in") == "path":
                param_name = param.get("name")
                if param_name in args:
                    url = url.replace(f"{{{param_name}}}", str(args[param_name]))
        
        url = f"{self.base_url}{url}"
        
        # Process query parameters
        query_params = {}
        for param in operation_info.get("parameters", []):
            if param.get("in") == "query" and param.get("name") in args:
                query_params[param.get("name")] = args[param.get("name")]
        
        # Process request body
        json_body = None
        if "body" in args:
            json_body = args["body"]
        
        # Make the API call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        print(f"Making API call to {url} with method {operation_method}")
        print(f"Headers: {headers}")
        print(f"Query params: {query_params}")
        print(f"JSON body: {json_body}")
        
        async with aiohttp.ClientSession() as session:
            method_func = getattr(session, operation_method.lower())
            
            try:
                async with method_func(
                    url, 
                    headers=headers, 
                    params=query_params, 
                    json=json_body
                ) as response:
                    if response.status >= 400:
                        error_text = await response.text()
                        return {"error": f"API error: {response.status} - {error_text}"}
                    
                    response_data = await response.json()
                    return response_data
            except Exception as e:
                return {"error": f"Request failed: {str(e)}"}
    

server = AstroServer()
