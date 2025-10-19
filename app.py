import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient


async def main():
    load_dotenv()

    config_file = "browser_mcp.json"
    print(f"Using config file: {config_file}")

    llm = ChatGroq(model="llama-3.3-70b-versatile")
    print(f"Using model: {llm}")

    client = MCPClient.from_config_file(config_file)

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        memory_enabled=True)

    result=await agent.run("Open google and search for AI startups in SFO and give me the top 5 companies and what problem they are solving ")

    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())


