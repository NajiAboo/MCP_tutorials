from langchain_community.utilities import SerpAPIWrapper
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["SERPAPI_API_KEY"] = "7461a367eb89fd44fc0f2697077620b9c9937dfd4498cf1f245f422af186beb5"

mcp = FastMCP("Flipkart", port="8081")

@mcp.tool()
def search_flipkart(product: str) -> str:
    """
        Searches flipkart for a product and return the result
    """
    search = SerpAPIWrapper()
    query=f"site: flipkart.com {product}"
    return search.run(query=query)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")