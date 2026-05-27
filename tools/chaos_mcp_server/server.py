"""Chaos Engineering MCP Server entry point."""
from mcp.server.fastmcp import FastMCP

from tools.chaos_mcp_server.tools import register_tools
from tools.chaos_mcp_server.prompts import register_prompts

mcp = FastMCP(
    "chaos-engineering-server",
    version="0.1.0",
    description="MCP server for LitmusChaos and Harness Chaos Engineering operations",
)

register_tools(mcp)
register_prompts(mcp)


def main():
    """Run the MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
