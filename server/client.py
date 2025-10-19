import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient


async def main():
    load_dotenv()
    config_file="server/weather.json"

    llm=ChatGroq(model="llama-3.1-8b-instant")

    client=MCPClient.from_config_file(config_file)

    agent=MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        memory_enabled=True
    )


    result=await agent.run("what is the weather in CA")
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())
    