from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    __Summary:__ Adds two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    __Summary:__ Multiplies two numbers together."""
    return a * b

# the transport="stdio" arg tells the server to:
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls



if __name__ == "__main__":
    mcp.run(transport="stdio")