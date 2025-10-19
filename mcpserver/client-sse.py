import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()

async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            result = await session.call_tool("get_alerts", arguments={"state":"CA"})
            print(f"The weather alerts are = {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())