from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("python-ai-course-mcp-server")

@mcp.tool()
async def get_info() -> str:
    """Get information about this MCP server.
    
    Returns information about the purpose and capabilities of this demo MCP server.
    """
    return (
        "This is a demo MCP server created using the MCP SDK.\n\n"
        "It demonstrates how to create a simple MCP server with tools "
        "that can be used by MCP clients like Claude Desktop and VSCode."
    )

@mcp.tool()
async def get_greetings(name: str) -> str:
    """Get a personalized greeting.
    
    Args:
        name: The name of the person to greet
    
    Returns a friendly greeting that includes the provided name.
    """
    return f"Hello, {name}! This is a demo MCP server."

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
