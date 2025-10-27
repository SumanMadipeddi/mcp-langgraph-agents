import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import SystemMessage
from langchain.messages import ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage
from langchain.messages import AnyMessage
from typing import TypedDict, Annotated
from IPython.display import Image, display
from typing import Literal
import operator
load_dotenv()

async def main():
    client = MultiServerMCPClient({
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
            "transport": "stdio",
        },
        "duckduckgo-search": {
            "command": "npx",
            "args": ["-y", "duckduckgo-mcp-server"],
            "transport": "stdio",
        },
    })
    
    llm = init_chat_model("google_genai:gemini-2.0-flash")
    tools = await client.get_tools()
    for tool in tools:
        print(f"{tool.name}: {tool.description}")
    print(f"\n Loaded {len(tools)} tools total\n")
    
    tools_by_name = {tool.name: tool for tool in tools}
    model_with_tools=llm.bind_tools(tools)

    return model_with_tools, tools, tools_by_name
model_with_tools, tools, tools_by_name=asyncio.run(main())

class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls:int

def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages":[model_with_tools.invoke(
                [
                    SystemMessage(
                            content="You are a helpful assistant")
                ]
                + state["messages"]
            )],
        "llm_calls":state.get('llm_calls',0)+1
    }

async def tool_node(state: dict):
    """Performs the tool call"""
    import asyncio

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = await tool.ainvoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessageState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    return END


agent_builder=StateGraph(MessageState)

agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("tool_node",tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node","llm_call")

agent=agent_builder.compile()

# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

messages=[HumanMessage(content="go to google and open the facebook add library and search for the nike and wait which will show the drop down and then see teh compay name and search and get the id from url")]
messages=asyncio.run(agent.ainvoke({"messages":messages}))

for m in messages["messages"]:
    m.pretty_print()
