from mcp.server.fastmcp import FastMCP
import nhm_api
import json

# Create an MCP server
mcp = FastMCP("Natural History Museum Data API")

@mcp.tool()
def search_specimens(query: str, limit: int) -> str:
    nhm_api_result = nhm_api.get_by_query(query, limit)

    return json.dumps(nhm_api_result)


def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()
