"""
Astro MCP package for interacting with the Astro API.
"""

from astro_mcp.server import get_server, main

# Create a server instance for MCP CLI
server = get_server()

__all__ = ["get_server", "main", "server"]