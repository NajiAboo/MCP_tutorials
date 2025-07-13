from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """
        Gt weather for location
    """

    return "Its always sunny in ny"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")