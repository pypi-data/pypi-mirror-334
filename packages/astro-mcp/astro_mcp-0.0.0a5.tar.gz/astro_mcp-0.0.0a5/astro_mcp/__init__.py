"""
Runs the MCP server for the Astro API.
"""

def start_astro_mcp():
    print("Running MCP server for Astro API")

    from astro_mcp.platform import server

    server.run()


if __name__ == "__main__":
    start_astro_mcp()
