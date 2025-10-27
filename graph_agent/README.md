# LangGraph Agent with MCP Integration

This notebook demonstrates how to integrate MCP (Model Context Protocol) servers with LangChain/LangGraph.

## Features

- **Math Server**: Perform arithmetic operations (add, multiply)
- **Weather Server**: Get weather alerts for US states
- **LangChain Agent**: Conversational AI agent with tool access
- **Groq LLM**: Fast inference with Llama models

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the Weather MCP Server

In a separate terminal:

```bash
cd mcpserver
python server.py
```

Or use the convenience script:

```bash
python mcpserver/start_weather_server.py
```

The weather server will be available at `http://127.0.0.1:8000`

### 4. Run the Notebook

Open `main.ipynb` in Jupyter or your preferred notebook environment and run all cells.

## Usage

### Basic Examples

1. **Math Operations**:
   ```python
   response = await agent_executor.ainvoke({
       "input": "What's 15 multiplied by 20?"
   })
   ```

2. **Weather Alerts**:
   ```python
   response = await agent_executor.ainvoke({
       "input": "What are the weather alerts for Texas?"
   })
   ```

3. **Complex Calculations**:
   ```python
   response = await agent_executor.ainvoke({
       "input": "Calculate (100 + 50) * 3 - 25"
   })
   ```

## Architecture

```
┌─────────────────┐
│  Jupyter        │
│  Notebook       │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
    ┌────▼────┐    ┌────▼────┐
    │  Math   │    │ Weather │
    │ Server  │    │ Server  │
    │ (stdio) │    │ (HTTP)  │
    └─────────┘    └─────────┘
         │              │
         └──────┬───────┘
                │
         ┌──────▼──────┐
         │ MCP Client  │
         │             │
         │  ┌──────────▼───┐
         │  │ LangChain      │
         │  │ Agent          │
         │  │ (Groq LLM)     │
         └──┴────────────────┘
```

## Troubleshooting

### Weather Server Not Connecting

Make sure the weather server is running:
```bash
curl http://127.0.0.1:8000/sse
```

### Math Server Issues

The math server starts automatically via stdio. If there are issues, check that `uv` is installed:
```bash
uv --version
```

### Import Errors

Install missing dependencies:
```bash
pip install langchain langchain-groq langchain-mcp-adapters
```

