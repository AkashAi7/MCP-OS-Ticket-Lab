# MCP Development Cheat Sheet

> Quick reference for building MCP servers

---

## 🚀 Project Setup

```powershell
# Create project
mkdir my-mcp-server && cd my-mcp-server
python -m venv venv
.\venv\Scripts\Activate
pip install mcp httpx
```

---

## 📄 Minimal Server Template

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="What it does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Param desc"}
                },
                "required": ["param"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        return [TextContent(type="text", text=f"Result: {arguments['param']}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔧 JSON Schema Types

| Type | Schema | Example |
|------|--------|---------|
| String | `{"type": "string"}` | `"hello"` |
| Integer | `{"type": "integer"}` | `42` |
| Number | `{"type": "number"}` | `3.14` |
| Boolean | `{"type": "boolean"}` | `true` |
| Array | `{"type": "array", "items": {"type": "string"}}` | `["a", "b"]` |
| Object | `{"type": "object", "properties": {...}}` | `{"key": "value"}` |
| Enum | `{"type": "string", "enum": ["a", "b", "c"]}` | `"a"` |

### Constraints

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100,
  "pattern": "^[a-z]+$"
}
```

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100
}
```

```json
{
  "type": "array",
  "items": {"type": "string"},
  "minItems": 1,
  "maxItems": 10
}
```

---

## 📚 Resources

```python
from mcp.types import Resource, TextResourceContents

@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="myapp://data",
            name="My Data",
            description="Description",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    if uri == "myapp://data":
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text='{"key": "value"}'
        )
    raise ValueError(f"Unknown resource: {uri}")
```

---

## 💬 Prompts

```python
from mcp.types import Prompt, PromptMessage, PromptArgument

@app.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="my_prompt",
            description="Description",
            arguments=[
                PromptArgument(
                    name="topic",
                    description="Topic description",
                    required=True
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None):
    if name == "my_prompt":
        topic = arguments.get("topic", "default")
        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=f"Discuss {topic}")
            )
        ]
    raise ValueError(f"Unknown prompt: {name}")
```

---

## 🌐 HTTP Client Pattern

```python
import httpx

async def fetch_data(url: str, api_key: str = None):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
```

---

## 🐳 Docker Execution Pattern

```python
import subprocess
import json

def execute_in_docker(container: str, command: list) -> dict:
    cmd = ["docker", "exec", container] + command
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        return {"error": result.stderr}
    
    return json.loads(result.stdout)
```

---

## ⚠️ Error Handling

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Your logic here
        result = await do_something(arguments)
        return [TextContent(type="text", text=f"Success: {result}")]
    
    except ValueError as e:
        return [TextContent(type="text", text=f"❌ Validation Error: {e}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]
```

---

## 🧪 Test Template

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Tools: {[t.name for t in tools.tools]}")
            
            # Call tool
            result = await session.call_tool("my_tool", {"param": "test"})
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

---

## ⚙️ VS Code Configuration

`.vscode/settings.json`:

```json
{
    "mcp": {
        "servers": {
            "my-server": {
                "command": "python",
                "args": ["${workspaceFolder}/server.py"],
                "env": {
                    "API_KEY": "your-key",
                    "DEBUG": "true"
                }
            }
        }
    }
}
```

---

## 🔍 Environment Variables

```python
import os

# Get with default
API_KEY = os.environ.get("API_KEY", "")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
TIMEOUT = int(os.environ.get("TIMEOUT", "30"))
```

---

## 📁 Project Structure

```
my-mcp-server/
├── server.py           # Main MCP server
├── test.py             # Test suite
├── requirements.txt    # Dependencies
├── README.md           # Documentation
├── .vscode/
│   └── settings.json   # VS Code MCP config
└── src/
    ├── __init__.py
    ├── client.py       # API client
    └── utils.py        # Helper functions
```

---

## 📦 requirements.txt

```
mcp>=1.0.0
httpx>=0.27.0
```

---

## 🏃 Quick Commands

```powershell
# Run server
python server.py

# Test server
python test.py

# Install deps
pip install -r requirements.txt

# Check syntax
python -m py_compile server.py
```
