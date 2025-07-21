from langchain_community.utilities import SerpAPIWrapper
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["SERPAPI_API_KEY"]= "7461a367eb89fd44fc0f2697077620b9c9937dfd4498cf1f245f422af186beb5"


mcp = FastMCP("Amazon", port="8082")

@mcp.tool()
def search_amazon(product: str) -> str:
    """
        Searches amazon for a product and return the result
    """
    try:
        search = SerpAPIWrapper()
        query=f"site: amazon.in {product}"
        print(query)
        result = search.run(query)
        print(result)
        return result
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")