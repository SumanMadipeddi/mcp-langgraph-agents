# MCP Server & LLM Integration Guide

A simple guide to creating MCP servers with **FastMCP** and integrating them with any LLM using **mcp-use**.

## 🔍 What is MCP?

**Model Context Protocol (MCP)** is an open protocol that lets AI assistants (LLMs) connect to external tools, databases, and services. Think of it as giving your AI superpowers! 🦸

## 📂 This Project Contains

- **Weather MCP Server** - Built with FastMCP (server/weather.py)
- **LLM Integration Example** - Using mcp-use with Groq LLM (app.py)
- **Browser Automation Example** - MCP integration with Playwright

---

## 🚀 Quick Start

### 0. Install UV (if not installed)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 1. Install Dependencies

```bash
# Install all dependencies from pyproject.toml
uv sync

# Or install specific packages
uv pip install mcp-use langchain-groq fastmcp httpx python-dotenv

# Or add packages to your project
uv add mcp-use langchain-groq fastmcp httpx python-dotenv
```

### 2. Set Up Environment Variables

Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Weather MCP Server

```bash
# STDIO mode (for direct client connection)
uv run python server/weather.py

# SSE mode (HTTP server on port 8000)
uv run python mcpserver/server.py
```

### 4. Run the LLM Agent

```bash
uv run python app.py
```

---

## 🛠️ Creating MCP Servers with FastMCP

FastMCP makes it super easy to create MCP servers in Python!

### Example: Simple Weather Server

```python
from mcp.server.fastmcp import FastMCP
import httpx

# Create server
mcp = FastMCP("weather")

# Add a tool
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"https://api.weather.gov/alerts/active/area/{state}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return data

# Run the server
if __name__ == "__main__":
    mcp.run()
```

That's it! You now have a working MCP server. ✨

---

## 🤝 Integrating MCP with LLMs using mcp-use

**mcp-use** lets you connect ANY LLM (OpenAI, Anthropic, Groq, Ollama, etc.) with MCP servers.

### Example: Connect Groq LLM to MCP Server

```python
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

# 1. Initialize your LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 2. Connect to MCP server(s)
client = MCPClient.from_config_file("browser_mcp.json")

# 3. Create an agent
agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=30,
    memory_enabled=True
)

# 4. Run tasks!
result = await agent.run("What's the weather in CA?")
print(result)
```

### Works with ANY LLM Framework:

- ✅ LangChain (OpenAI, Anthropic, Groq, etc.)
- ✅ Ollama (local models)
- ✅ Bedrock, Azure OpenAI
- ✅ Any custom LLM

---

## 📋 MCP Configuration File

Create a `browser_mcp.json` or any config file to define your MCP servers:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "python", "server/weather.py"],
      "type": "stdio"
    },
    "browser": {
      "url": "http://localhost:8000/sse",
      "type": "sse"
    }
  }
}
```

---

## 📚 Key Concepts

### MCP Server Types

1. **STDIO** - Standard input/output (local process)
2. **SSE** - Server-Sent Events (HTTP endpoint)

### MCP Components

- **Tools** - Functions the LLM can call (e.g., `get_weather`, `search_web`)
- **Resources** - Data the LLM can access (e.g., files, databases)
- **Prompts** - Pre-defined prompts for common tasks

---

## 🔗 Useful Links

### UV (Package Manager)
- **UV Docs**: https://docs.astral.sh/uv/
- **UV GitHub**: https://github.com/astral-sh/uv
- **UV Installation**: https://docs.astral.sh/uv/getting-started/installation/

### Official MCP Resources
- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **MCP GitHub**: https://github.com/modelcontextprotocol
- **MCP Servers List**: https://github.com/modelcontextprotocol/servers

### FastMCP
- **FastMCP Docs**: https://github.com/jlowin/fastmcp
- **FastMCP PyPI**: https://pypi.org/project/fastmcp/

### mcp-use (LLM Integration)
- **mcp-use GitHub**: https://github.com/ergut/mcp-use
- **mcp-use PyPI**: https://pypi.org/project/mcp-use/

### LLM Providers
- **Groq (Fast Inference)**: https://console.groq.com/
- **LangChain**: https://python.langchain.com/
- **Anthropic Claude**: https://www.anthropic.com/
- **OpenAI**: https://platform.openai.com/

---

## 💡 Examples in This Repo

### 1. Weather Server (`server/weather.py`)
- Simple MCP server using FastMCP
- Fetches real-time weather alerts from NOAA API
- STDIO transport

### 2. SSE Server (`mcpserver/server.py`)
- Same weather server but with HTTP/SSE transport
- Runs on port 8000
- Can be accessed remotely

### 3. LLM Agent (`app.py`)
- Uses Groq LLM (fast and free!)
- Integrates with browser automation MCP server
- Shows memory-enabled multi-step tasks

---

## 🎯 Use Cases

**What can you build with MCP?**

- 🌦️ Weather assistants
- 🌐 Web scraping agents
- 💾 Database query tools
- 📧 Email automation
- 🔍 Search engines
- 📊 Data analysis tools
- 🤖 Multi-tool AI agents

---

## 📝 Project Structure

```
mcp_server/
├── app.py                    # LLM agent example
├── browser_mcp.json          # MCP configuration
├── pyproject.toml            # UV project configuration
├── uv.lock                   # UV lock file
├── server/
│   └── weather.py           # Weather MCP server (STDIO)
├── mcpserver/
│   ├── server.py            # Weather MCP server (SSE)
│   ├── client-stdio.py      # STDIO client example
│   └── client-sse.py        # SSE client example
└── README.md                # This file
```

---

## 🚦 Common UV Commands

### Package Management

```bash
# Install UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh             # macOS/Linux

# Initialize a new project
uv init

# Install dependencies from pyproject.toml
uv sync

# Add a package
uv add fastmcp
uv add mcp-use langchain-groq

# Add a development dependency
uv add --dev pytest black ruff

# Remove a package
uv remove package-name

# Install a package globally as a tool
uv tool install mcp-cli
uv tool install ruff

# List installed tools
uv tool list

# Uninstall a tool
uv tool uninstall mcp-cli

# Update a package
uv lock --upgrade-package fastmcp

# Update all packages
uv lock --upgrade

# Run a Python script with UV
uv run python app.py
uv run python server/weather.py

# Run a command in the virtual environment
uv run pytest
uv run black .

# Create a virtual environment
uv venv

# Activate the virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install packages with pip interface
uv pip install httpx
uv pip list
uv pip uninstall httpx

# Clean cache
uv cache clean

# Check UV version
uv --version
```

### Running MCP Servers with UV

```bash
# Run weather server (STDIO)
uv run python server/weather.py

# Run weather server (SSE on port 8000)
uv run python mcpserver/server.py

# Run LLM agent
uv run python app.py

# Test MCP server with inspector (using uvx)
uvx @modelcontextprotocol/inspector python server/weather.py

# Or install inspector as a tool
uv tool install @modelcontextprotocol/inspector
```

### Project Setup from Scratch

```bash
# Create new project directory
mkdir my-mcp-project
cd my-mcp-project

# Initialize UV project
uv init

# Add dependencies
uv add fastmcp mcp-use langchain-groq httpx python-dotenv

# Create your server file
# (write your code)

# Run it
uv run python server.py

# Lock dependencies
uv lock

# Share your project (others can run)
# Just share the directory with pyproject.toml and uv.lock
# Others run: uv sync && uv run python server.py
```

---

## 🤔 Troubleshooting

### Issue: "Module not found: mcp"
```bash
# Install FastMCP
uv add fastmcp
# or
uv pip install fastmcp
```

### Issue: "No API key found"
Add your API key to `.env` file:
```env
GROQ_API_KEY=your_key_here
```

### Issue: "Connection refused"
Make sure the MCP server is running before starting the client.

### Issue: "UV command not found"
```bash
# Reinstall UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh             # macOS/Linux

# Add to PATH if needed (Windows)
# UV is typically installed to: %USERPROFILE%\.cargo\bin
```

### Issue: "Package version conflict"
```bash
# Update lock file
uv lock --upgrade

# Or sync with fresh lock
rm uv.lock
uv sync
```

---

## 🎓 Learn More

1. **Start Simple**: Create a basic MCP server with one tool
2. **Test It**: Use the MCP inspector to test your server
   ```bash
   uvx @modelcontextprotocol/inspector python server/weather.py
   ```
3. **Connect an LLM**: Use mcp-use to integrate with your favorite LLM
4. **Build Complex Agents**: Combine multiple MCP servers for powerful agents
5. **Use UV Tools**: Install CLI tools globally with `uv tool install`

---

## 🔧 UV Best Practices

1. **Use `uv sync`** - Always sync dependencies before running
2. **Lock your dependencies** - Commit `uv.lock` to git
3. **Use `uv run`** - Run scripts in the project's environment
4. **Install tools globally** - Use `uv tool install` for CLI tools
5. **Keep UV updated** - Run `uv self update` periodically

---

## 📦 Complete Installation Script

```bash
# 1. Install UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone/navigate to project
cd mcp_server

# 3. Install all dependencies
uv sync

# 4. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Run the server
uv run python server/weather.py

# 6. In another terminal, run the agent
uv run python app.py
```

---

## 🧹 Cleanup Commands

```bash
# Remove virtual environment
rm -rf .venv

# Remove UV cache
uv cache clean

# Uninstall UV completely (Windows)
Remove-Item -Recurse -Force "$env:USERPROFILE\.cargo\bin\uv.exe"
Remove-Item -Recurse -Force "$env:USERPROFILE\.uv"
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\uv"

# Uninstall all UV tools
uv tool uninstall mcp-cli
uv tool list  # Check what's installed
```

---

## 📄 License

This project is open source and available for learning purposes.

---

## 🙏 Credits

- **UV** by Astral
- **FastMCP** by James Lowin
- **mcp-use** by ergut
- **Model Context Protocol** by Anthropic

---

**Happy Building! 🚀**

*Questions? Check the links above or dive into the code examples!*

---

## 🆚 UV vs pip/npm Quick Reference

| Task | pip/npm | UV |
|------|---------|-----|
| Install package | `pip install fastmcp` | `uv add fastmcp` |
| Install from requirements | `pip install -r requirements.txt` | `uv sync` |
| Run script | `python app.py` | `uv run python app.py` |
| Global CLI tool | `npm install -g tool` | `uv tool install tool` |
| List packages | `pip list` | `uv pip list` |
| Remove package | `pip uninstall package` | `uv remove package` |
| Create venv | `python -m venv .venv` | `uv venv` |
| Update packages | `pip install --upgrade` | `uv lock --upgrade` |

**Why UV?**
- ⚡ 10-100x faster than pip
- 🔒 Automatic dependency locking
- 🎯 Built-in virtual environment management
- 🛠️ Global tool installation
- 📦 Single tool for everything (no need for pip, venv, pipx, etc.)
