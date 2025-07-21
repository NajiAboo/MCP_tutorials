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
                "amazon": {
                    "url": "http://localhost:8082/mcp/",
                    "transport": "streamable_http"
                },
                "flipkart": {
                    "url": "http://localhost:8081/mcp/",
                    "transport": "streamable_http"
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