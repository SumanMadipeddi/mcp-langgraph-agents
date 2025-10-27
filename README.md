# MCP Server & LLM Integration

A practical guide to building MCP servers with **FastMCP** and integrating them with any LLM using **mcp-use**.

## Project Structure

- **`server/`** - Basic weather MCP server using STDIO transport
- **`mcpserver/`** - Weather MCP server with SSE/HTTP transport, includes client examples and Streamlit UI
- **`mcpagent/`** - Simple MCP servers (math and weather) for agent integration examples
- **`graph_agent/`** - LangGraph integration examples
  - `main.ipynb` - Weather tool agent with LangSmith monitoring
  - `main.py` - Competitor ads flow analysis using Playwright and DuckDuckGo search MCP servers
- **`app.py`** - Browser automation example using mcp-use with Groq LLM

## Quick Start

```bash
# Install UV (if needed)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "GEMINI_API_KEY=your_key_here" >> .env

# Run the weather MCP server
uv run python server/weather.py

# Run the LLM agent (in another terminal)
uv run python app.py
```

## Resources

- **MCP Spec**: https://spec.modelcontextprotocol.io/
- **FastMCP**: https://github.com/jlowin/fastmcp
- **mcp-use**: https://github.com/ergut/mcp-use
- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://docs.langchain.com/oss/python/langgraph/overview
- **UV Docs**: https://docs.astral.sh/uv/
