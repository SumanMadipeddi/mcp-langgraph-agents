from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent, openai
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    load_dotenv()
    client=MultiServerMCPClient(
    {
        "math":{
            "command":"uv",
            "args":[
                "run",
                "math_server.py"
            ],
            "transport":"stdio",
        },

        "weather":{
            "url":"http://127.0.0.1:8000/mcp",
            "transport":"streamable_http"
        }

    })

    tools=await client.get_tools()
    llm=ChatGroq(
        model="llama-3.3-70b-versatile", 
        model_kwargs={
            "tool_choice": "auto"
        }
    )
    agent=create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a JARVIS in IronMan solve like a human emotional intelligence and Artificial General Intelligence and give me step by steps in detail"
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 10)*20?"}]}
    )
    print("Math Agent Response:",math_response["messages"][-1].content)

    weather_response= await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's the weather in Arizona?"}]}
    )

    print("Weather Agent Response:",weather_response["messages"][-1].content)

asyncio.run(main())






