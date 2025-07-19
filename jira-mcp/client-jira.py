import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

async def test_jira_server():
    print("Testing JIRA Server...")
    client = MultiServerMCPClient({
        "mcp-atlassian": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e", "JIRA_URL",
                "-e", "JIRA_USERNAME", 
                "-e", "JIRA_API_TOKEN",
                "ghcr.io/sooperset/mcp-atlassian:latest"
            ],
            "env": {
                "JIRA_URL": "https://najiabootrain.atlassian.net/",
                "JIRA_USERNAME": "najiaboo.train@gmail.com",
                "JIRA_API_TOKEN": "ATATT3xFfGF0fP_iraiYHuFwbTrtdq8ZFBlFzBX40_ZI5-705DOgFVFEuZkGmyr0Lw5keMuOmunkasPRsg7ko-MlqcyyOxMVxxoESEV4f8F29IlIRVw_yt05K6b210_Yw2U1j6-GS0sD73KtouYesge11NLMqSuM_eEDeJydqLkawB4oy93ryAw=C32C4D5A"
            },
            "transport": "stdio",
        }
    })
    
    try:
        #await client.initialize()
        tools = await client.get_tools()
        print(f"JIRA server tools: {[tool.name for tool in tools]}")

        agent = create_react_agent("gpt-4o", tools=tools)

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Give me task assigned to naji aboo?"}]}
        )

        print(response["messages"][-1].content)

        return True
    except Exception as e:
        print(f"JIRA server error: {e}")
        return False
    finally:
        try:
            await client.close()
        except:
            pass

async def main():
    jira_ok = await test_jira_server()
    
    print(f"\nResults:")
    print(f"JIRA server: {'✓' if jira_ok else '✗'}")

if __name__ == "__main__":
    asyncio.run(main())