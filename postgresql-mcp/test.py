import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
load_dotenv()

async def test_postsql():
    print("Testing Postsql mcp")

    client = MultiServerMCPClient({
        "postgres-mcp-server": {
      "command": "npx",
      "args": [
        "@ahmedmustahid/postgres-mcp-server",
        "stdio"
      ],
      "env": {
        "POSTGRES_URL" : "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

      },
      "transport": "stdio"
    }

    })


    try:
        tools =  await client.get_tools()
        print(f"Available tools {tools}")

        agent = create_react_agent('gpt-4o', tools=tools)

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": "list tables in the database"}]
        })

        print(result["messages"][-1].content)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    asyncio.run(test_postsql())