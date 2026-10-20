
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pathlib import Path
import os
import sys
import asyncio

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY is missing from your .env file")

llm = init_chat_model(
    "claude-sonnet-4-6",
    model_provider="anthropic",
    api_key=api_key,
)

async def main():
    math_server = Path(__file__).parent / "mathserver.py"

    if not math_server.exists():
        raise FileNotFoundError(
            f"Math server not found: {math_server}"
        )

    mcp_client = MultiServerMCPClient({
        "math": {
            "command": sys.executable,
            "args": [str(math_server)],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http",
        },
    })

    tools = await mcp_client.get_tools()
    print("Available tools:", [tool.name for tool in tools])

    agent = create_react_agent(llm, tools)

    result = await agent.ainvoke({
        "messages": [
            ("user", "What is the multiplication of 5 and 3?")
        ]
    })

    print("Agent response:", result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
