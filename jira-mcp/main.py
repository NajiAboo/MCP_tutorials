import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

app = FastAPI()

# global variables
client = None
tools = []
agent = None

@app.on_event("startup")
async def startup_event():
    global client, tools, agent
    try:
        client = MultiServerMCPClient(
            {
                "math": {
                    "command": "python",
                    "args": ["math-server.py"],
                    "transport": "stdio"
                },
                "weather": {
                    'url': "http://localhost:8000/mcp",
                    "transport": "streamable_http"
                },
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
                
            }
        )

        tools = await client.get_tools()
        agent = create_react_agent('gpt-4o', tools=tools)
        print(f"Successfully initialized with {len(tools)} tools")
    except Exception as ex:
        print(ex)


class ChatInput(BaseModel):
    message: str

class ChatOutput(BaseModel):
    response: str

@app.post("/chat", response_model=ChatOutput)
async def chat_endpoint(chat_input: ChatInput):
    try:
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=chat_input.message)]}
        )
        ai_response_message = response["messages"][-1].content
        print(f"AI message {ai_response_message}")

        return ChatOutput(response=ai_response_message)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)