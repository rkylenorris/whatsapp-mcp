from mcp.server.fastmcp import FastMCP

mcp = FastMCP("whatsapp-helper", json_response=True)


@mcp.tool()
def ping(name: str = "world") -> str:
    """Simple sanity check tool."""
    return f"Hello, {name}! MCP is alive."


if __name__ == "__main__":
    # For quick dev/testing use HTTP; later you can do stdio if needed.
    mcp.run()
