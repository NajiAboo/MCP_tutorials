import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


from dotenv import load_dotenv
load_dotenv()

async def test_youtube_summarizer():
    print("Testing Youtube Summarizer")

    client = MultiServerMCPClient(
        {
            "youtube-video-summarizer": {
                "command": "npx",
                "args": ["-y", "youtube-video-summarizer-mcp"],
                "transport": "stdio"
            }

        }
    )

    try:
        tools = await client.get_tools()
        print(f" AValiable tools {tools}")

        agent = create_react_agent("gpt-4o", tools= tools)
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": "Can you summarize this YouTube video for me? https://youtu.be/fv7EfD-Xs5Y"}]
        })
        print(response["messages"][-1].content)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    asyncio.run(test_youtube_summarizer())