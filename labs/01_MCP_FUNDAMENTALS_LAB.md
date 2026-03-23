# Lab 1: MCP Fundamentals - From Beginner to Advanced

> **Model Context Protocol (MCP)** - A Complete Hands-On Learning Path

---

## 🎯 Learning Objectives

By completing this lab, you will be able to:
- Understand what MCP is and why it matters
- Build MCP servers from scratch
- Define custom tools with proper JSON schemas
- Handle resources and prompts
- Integrate MCP servers with VS Code Copilot
- Debug and test MCP implementations
- **Deploy MCP servers to Azure Container Apps**
- **Create VS Code `.prompt.md` skills and `.instructions.md` files**
- Build production-ready MCP solutions

---

## 📋 Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| VS Code | Latest | `code --version` |
| Git | Any | `git --version` |

---

# Module 1: Understanding MCP (Beginner)

## 1.1 What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how AI assistants connect to external data sources and tools. Think of it as a "USB for AI" - a universal connector.

### Key Concepts

```
┌─────────────────┐     MCP Protocol     ┌──────────────────┐
│   AI Assistant  │ ◄──────────────────► │   MCP Server     │
│   (VS Code,     │                      │   (Your App)     │
│    Claude, etc) │                      │                  │
└─────────────────┘                      └──────────────────┘
        │                                         │
        │ Requests tools, resources               │ Exposes tools,
        │ Calls functions                         │ resources, prompts
        │                                         │
        ▼                                         ▼
   "Create a ticket"                    create_ticket(title, body)
```

### MCP Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Functions the AI can call | `create_ticket()`, `search_database()` |
| **Resources** | Data the AI can read | Files, database records, API responses |
| **Prompts** | Pre-defined conversation templates | "Analyze this ticket" template |

---

## Exercise 1.1: Your First MCP Server (Hello World)

**Goal**: Create a minimal MCP server that responds with "Hello, MCP!"

### Step 1: Create Project Structure

```powershell
# Create project folder
mkdir mcp-hello-world
cd mcp-hello-world

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install MCP SDK
pip install mcp
```

### Step 2: Create the Server

Create `server.py`:

```python
"""
Exercise 1.1: Hello World MCP Server
=====================================
This is the simplest possible MCP server.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

# Create server instance
app = Server("hello-world")

# Define available tools
@app.list_tools()
async def list_tools():
    """Return list of available tools."""
    return [
        Tool(
            name="say_hello",
            description="Says hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet"
                    }
                },
                "required": ["name"]
            }
        )
    ]

# Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute tool calls."""
    if name == "say_hello":
        person_name = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {person_name}! Welcome to MCP!")]
    raise ValueError(f"Unknown tool: {name}")

# Main entry point
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 3: Test Your Server

Create `test_hello.py`:

```python
"""Test the Hello World server."""
import subprocess
import json

def test_server():
    # Start server process
    process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_request) + "\n")
    process.stdin.flush()
    
    response = process.stdout.readline()
    print(f"Initialize response: {response}")
    
    process.terminate()
    print("✅ Server responds correctly!")

if __name__ == "__main__":
    test_server()
```

### ✅ Checkpoint 1.1
- [ ] Server starts without errors
- [ ] Server responds to initialize request
- [ ] You understand the basic MCP server structure

---

## Exercise 1.2: Adding Multiple Tools

**Goal**: Extend your server with multiple tools.

### Step 1: Create Calculator Server

Create `calculator_server.py`:

```python
"""
Exercise 1.2: Multi-Tool Calculator Server
==========================================
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import math

app = Server("calculator")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="sqrt",
            description="Calculate square root",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {"type": "number", "description": "Number to get square root of"}
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="factorial",
            description="Calculate factorial of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "description": "Number (0-20)"}
                },
                "required": ["n"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [TextContent(type="text", text=f"Result: {result}")]
    
    elif name == "multiply":
        result = arguments["a"] * arguments["b"]
        return [TextContent(type="text", text=f"Result: {result}")]
    
    elif name == "sqrt":
        num = arguments["number"]
        if num < 0:
            return [TextContent(type="text", text="Error: Cannot calculate square root of negative number")]
        result = math.sqrt(num)
        return [TextContent(type="text", text=f"√{num} = {result}")]
    
    elif name == "factorial":
        n = arguments["n"]
        if n < 0 or n > 20:
            return [TextContent(type="text", text="Error: n must be between 0 and 20")]
        result = math.factorial(n)
        return [TextContent(type="text", text=f"{n}! = {result}")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 🏆 Challenge 1.2
Add these additional tools to your calculator:
1. `power(base, exponent)` - Calculate power
2. `percentage(value, percent)` - Calculate percentage
3. `average(numbers)` - Calculate average of a list of numbers

<details>
<summary>💡 Hint for average tool</summary>

```python
Tool(
    name="average",
    description="Calculate average of numbers",
    inputSchema={
        "type": "object",
        "properties": {
            "numbers": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers"
            }
        },
        "required": ["numbers"]
    }
)
```
</details>

---

# Module 2: Tool Design Patterns (Intermediate)

## 2.1 JSON Schema Best Practices

### Input Validation Patterns

```python
# Good: Descriptive, constrained schema
Tool(
    name="create_user",
    description="Create a new user account",
    inputSchema={
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email",
                "description": "User's email address"
            },
            "username": {
                "type": "string",
                "minLength": 3,
                "maxLength": 20,
                "pattern": "^[a-zA-Z0-9_]+$",
                "description": "Username (3-20 chars, alphanumeric with underscores)"
            },
            "role": {
                "type": "string",
                "enum": ["admin", "user", "guest"],
                "default": "user",
                "description": "User role"
            }
        },
        "required": ["email", "username"]
    }
)
```

### Complex Input Types

```python
# Object within object
Tool(
    name="create_ticket",
    description="Create a support ticket",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
            "customer": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "phone": {"type": "string"}
                },
                "required": ["name", "email"]
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 5
            }
        },
        "required": ["title", "customer"]
    }
)
```

---

## Exercise 2.1: Building a Task Manager MCP Server

**Goal**: Create a practical task management MCP server with proper data persistence.

Create `task_manager_server.py`:

```python
"""
Exercise 2.1: Task Manager MCP Server
=====================================
A practical example with file-based persistence.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

app = Server("task-manager")

# Data file path
DATA_FILE = Path("tasks.json")

def load_tasks():
    """Load tasks from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": [], "next_id": 1}

def save_tasks(data):
    """Save tasks to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task to the list",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "default": "medium",
                        "description": "Task priority"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in YYYY-MM-DD format (optional)"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "default": "all",
                        "description": "Filter by status"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["all", "low", "medium", "high"],
                        "default": "all",
                        "description": "Filter by priority"
                    }
                }
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="get_task",
            description="Get details of a specific task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task"
                    }
                },
                "required": ["task_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    data = load_tasks()
    
    if name == "add_task":
        task = {
            "id": data["next_id"],
            "title": arguments["title"],
            "description": arguments.get("description", ""),
            "priority": arguments.get("priority", "medium"),
            "due_date": arguments.get("due_date"),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        data["tasks"].append(task)
        data["next_id"] += 1
        save_tasks(data)
        return [TextContent(type="text", text=f"✅ Task #{task['id']} created: {task['title']}")]
    
    elif name == "list_tasks":
        tasks = data["tasks"]
        status_filter = arguments.get("status", "all")
        priority_filter = arguments.get("priority", "all")
        
        if status_filter != "all":
            tasks = [t for t in tasks if t["status"] == status_filter]
        if priority_filter != "all":
            tasks = [t for t in tasks if t["priority"] == priority_filter]
        
        if not tasks:
            return [TextContent(type="text", text="No tasks found.")]
        
        output = "📋 **Tasks:**\n\n"
        for task in tasks:
            status_icon = "✅" if task["status"] == "completed" else "⏳"
            priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}[task["priority"]]
            output += f"{status_icon} #{task['id']} [{priority_icon}] {task['title']}\n"
            if task.get("due_date"):
                output += f"   Due: {task['due_date']}\n"
        
        return [TextContent(type="text", text=output)]
    
    elif name == "complete_task":
        task_id = arguments["task_id"]
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                save_tasks(data)
                return [TextContent(type="text", text=f"✅ Task #{task_id} marked as completed!")]
        return [TextContent(type="text", text=f"❌ Task #{task_id} not found.")]
    
    elif name == "delete_task":
        task_id = arguments["task_id"]
        original_count = len(data["tasks"])
        data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
        if len(data["tasks"]) < original_count:
            save_tasks(data)
            return [TextContent(type="text", text=f"🗑️ Task #{task_id} deleted.")]
        return [TextContent(type="text", text=f"❌ Task #{task_id} not found.")]
    
    elif name == "get_task":
        task_id = arguments["task_id"]
        for task in data["tasks"]:
            if task["id"] == task_id:
                output = f"""
**Task #{task['id']}**
- Title: {task['title']}
- Description: {task.get('description', 'N/A')}
- Priority: {task['priority']}
- Status: {task['status']}
- Due Date: {task.get('due_date', 'Not set')}
- Created: {task['created_at']}
"""
                return [TextContent(type="text", text=output.strip())]
        return [TextContent(type="text", text=f"❌ Task #{task_id} not found.")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 🏆 Challenge 2.1
Extend the task manager with:
1. `update_task` - Update task title, description, or priority
2. `search_tasks` - Search tasks by keyword
3. `get_statistics` - Return task statistics (total, completed, pending by priority)

---

## Exercise 2.2: Integrating with VS Code

**Goal**: Register your MCP server with VS Code Copilot.

### Step 1: Update VS Code Settings

Add to `.vscode/settings.json`:

```json
{
    "mcp": {
        "servers": {
            "task-manager": {
                "command": "python",
                "args": ["${workspaceFolder}/task_manager_server.py"],
                "env": {}
            }
        }
    }
}
```

### Step 2: Test in VS Code

1. Open VS Code in your project folder
2. Open Copilot Chat (Ctrl+Shift+I)
3. Type: `@mcp add a new high priority task titled "Review pull requests"`
4. Verify the task is created

### ✅ Checkpoint 2.2
- [ ] MCP server registered in VS Code
- [ ] Copilot can call your tools
- [ ] Tasks persist between sessions

---

# Module 3: Resources and Prompts (Intermediate-Advanced)

## 3.1 Understanding Resources

Resources in MCP provide read access to data that the AI can use as context.

```python
from mcp.types import Resource, TextResourceContents

@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="tasks://all",
            name="All Tasks",
            description="Complete list of all tasks",
            mimeType="application/json"
        ),
        Resource(
            uri="tasks://statistics",
            name="Task Statistics",
            description="Task completion statistics",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    data = load_tasks()
    
    if uri == "tasks://all":
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(data["tasks"], indent=2)
        )
    
    elif uri == "tasks://statistics":
        tasks = data["tasks"]
        stats = {
            "total": len(tasks),
            "completed": len([t for t in tasks if t["status"] == "completed"]),
            "pending": len([t for t in tasks if t["status"] == "pending"]),
            "by_priority": {
                "high": len([t for t in tasks if t["priority"] == "high"]),
                "medium": len([t for t in tasks if t["priority"] == "medium"]),
                "low": len([t for t in tasks if t["priority"] == "low"])
            }
        }
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(stats, indent=2)
        )
    
    raise ValueError(f"Unknown resource: {uri}")
```

---

## 3.2 Understanding Prompts

Prompts provide pre-defined conversation templates.

```python
from mcp.types import Prompt, PromptMessage, TextContent, PromptArgument

@app.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="daily_standup",
            description="Generate a daily standup report for tasks",
            arguments=[
                PromptArgument(
                    name="date",
                    description="Date for the report (YYYY-MM-DD)",
                    required=False
                )
            ]
        ),
        Prompt(
            name="task_analysis",
            description="Analyze a specific task in detail",
            arguments=[
                PromptArgument(
                    name="task_id",
                    description="ID of the task to analyze",
                    required=True
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None):
    data = load_tasks()
    
    if name == "daily_standup":
        tasks = data["tasks"]
        pending = [t for t in tasks if t["status"] == "pending"]
        completed_today = [t for t in tasks if t["status"] == "completed"]
        
        report = f"""
# Daily Standup Report

## Pending Tasks ({len(pending)})
{chr(10).join(f"- [{t['priority'].upper()}] {t['title']}" for t in pending)}

## Completed Tasks ({len(completed_today)})
{chr(10).join(f"- {t['title']}" for t in completed_today)}

Please summarize this in standup format (What I did, What I'm doing, Blockers).
"""
        return [PromptMessage(role="user", content=TextContent(type="text", text=report.strip()))]
    
    raise ValueError(f"Unknown prompt: {name}")
```

---

## Exercise 3.1: Full-Featured MCP Server

**Goal**: Create a complete MCP server with tools, resources, and prompts.

Create `complete_server.py` combining all concepts:

```python
"""
Exercise 3.1: Complete MCP Server
=================================
Demonstrates tools, resources, and prompts together.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, TextContent,
    Resource, TextResourceContents,
    Prompt, PromptMessage, PromptArgument
)
import asyncio
import json
from pathlib import Path
from datetime import datetime

app = Server("complete-demo")
DATA_FILE = Path("demo_data.json")

# ... (Include all tools, resources, and prompts from above)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

---

# Module 4: External API Integration (Advanced)

## 4.1 HTTP Client Pattern

```python
import httpx

class APIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def get(self, endpoint: str, params: dict = None):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
```

---

## Exercise 4.1: Weather API MCP Server

**Goal**: Create an MCP server that integrates with a weather API.

```python
"""
Exercise 4.1: Weather API MCP Server
====================================
Integrates with OpenWeatherMap API.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import httpx
import os

app = Server("weather")

# Get API key from environment
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "demo")
BASE_URL = "https://api.openweathermap.org/data/2.5"

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'London', 'New York')"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "default": "metric",
                        "description": "Temperature units"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_forecast",
            description="Get 5-day weather forecast for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "default": "metric"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    city = arguments["city"]
    units = arguments.get("units", "metric")
    unit_symbol = "°C" if units == "metric" else "°F"
    
    try:
        async with httpx.AsyncClient() as client:
            if name == "get_weather":
                response = await client.get(
                    f"{BASE_URL}/weather",
                    params={"q": city, "units": units, "appid": API_KEY},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                weather = f"""
🌍 **Weather in {data['name']}, {data['sys']['country']}**

🌡️ Temperature: {data['main']['temp']}{unit_symbol}
🤒 Feels like: {data['main']['feels_like']}{unit_symbol}
💧 Humidity: {data['main']['humidity']}%
🌤️ Conditions: {data['weather'][0]['description'].title()}
💨 Wind: {data['wind']['speed']} {'m/s' if units == 'metric' else 'mph'}
"""
                return [TextContent(type="text", text=weather.strip())]
            
            elif name == "get_forecast":
                response = await client.get(
                    f"{BASE_URL}/forecast",
                    params={"q": city, "units": units, "appid": API_KEY, "cnt": 8},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                forecast = f"📅 **5-Day Forecast for {data['city']['name']}**\n\n"
                for item in data["list"]:
                    dt = item["dt_txt"]
                    temp = item["main"]["temp"]
                    desc = item["weather"][0]["description"]
                    forecast += f"• {dt}: {temp}{unit_symbol} - {desc}\n"
                
                return [TextContent(type="text", text=forecast)]
    
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"❌ Error: {e.response.status_code} - {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

---

# Module 5: Error Handling & Production Patterns (Advanced)

## 5.1 Robust Error Handling

```python
from mcp.types import TextContent
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='mcp_server.log'
)
logger = logging.getLogger(__name__)

class MCPError(Exception):
    """Base exception for MCP errors."""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(MCPError):
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")

class NotFoundError(MCPError):
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} '{identifier}' not found", "NOT_FOUND")

def handle_tool_error(func):
    """Decorator for consistent error handling."""
    async def wrapper(name: str, arguments: dict):
        try:
            logger.info(f"Tool called: {name} with args: {arguments}")
            result = await func(name, arguments)
            logger.info(f"Tool {name} completed successfully")
            return result
        except MCPError as e:
            logger.warning(f"Tool {name} error: {e.code} - {e.message}")
            return [TextContent(type="text", text=f"❌ [{e.code}] {e.message}")]
        except Exception as e:
            logger.error(f"Tool {name} unexpected error: {traceback.format_exc()}")
            return [TextContent(type="text", text=f"❌ Unexpected error: {str(e)}")]
    return wrapper

@app.call_tool()
@handle_tool_error
async def call_tool(name: str, arguments: dict):
    # Your tool logic here
    pass
```

## 5.2 Configuration Management

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """MCP Server Configuration"""
    
    # API Settings
    api_base_url: str
    api_key: Optional[str]
    api_timeout: int
    
    # Storage Settings
    data_directory: str
    
    # Feature Flags
    enable_caching: bool
    debug_mode: bool
    
    @classmethod
    def from_environment(cls) -> "Config":
        return cls(
            api_base_url=os.environ.get("API_BASE_URL", "http://localhost:8080"),
            api_key=os.environ.get("API_KEY"),
            api_timeout=int(os.environ.get("API_TIMEOUT", "30")),
            data_directory=os.environ.get("DATA_DIR", "./data"),
            enable_caching=os.environ.get("ENABLE_CACHE", "true").lower() == "true",
            debug_mode=os.environ.get("DEBUG", "false").lower() == "true"
        )

# Usage
config = Config.from_environment()
```

---

# Module 6: Testing MCP Servers (Advanced)

## 6.1 Unit Testing Pattern

```python
"""
test_mcp_server.py - MCP Server Unit Tests
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from mcp.types import TextContent

# Import your server
from task_manager_server import call_tool, load_tasks, save_tasks

@pytest.fixture
def sample_data():
    return {
        "tasks": [
            {"id": 1, "title": "Test Task", "status": "pending", "priority": "high"}
        ],
        "next_id": 2
    }

@pytest.fixture
def mock_save(tmp_path):
    data_file = tmp_path / "tasks.json"
    with patch("task_manager_server.DATA_FILE", data_file):
        yield data_file

class TestTaskManager:
    
    @pytest.mark.asyncio
    async def test_add_task(self, mock_save):
        result = await call_tool("add_task", {"title": "New Task", "priority": "high"})
        assert isinstance(result, list)
        assert "created" in result[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_list_empty_tasks(self, mock_save):
        result = await call_tool("list_tasks", {})
        assert "No tasks" in result[0].text or "Tasks:" in result[0].text
    
    @pytest.mark.asyncio
    async def test_complete_nonexistent_task(self, mock_save):
        result = await call_tool("complete_task", {"task_id": 999})
        assert "not found" in result[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self, mock_save):
        with pytest.raises(ValueError, match="Unknown tool"):
            await call_tool("nonexistent_tool", {})

# Run tests with: pytest test_mcp_server.py -v
```

## 6.2 Integration Testing

```python
"""
test_integration.py - MCP Server Integration Tests
"""

import subprocess
import json
import time

class MCPTestClient:
    def __init__(self, command: list):
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.request_id = 0
    
    def send_request(self, method: str, params: dict = None) -> dict:
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        return json.loads(response_line)
    
    def initialize(self):
        return self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        })
    
    def list_tools(self):
        return self.send_request("tools/list")
    
    def call_tool(self, name: str, arguments: dict):
        return self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
    
    def close(self):
        self.process.terminate()

def test_full_workflow():
    client = MCPTestClient(["python", "task_manager_server.py"])
    
    try:
        # Initialize
        init_response = client.initialize()
        assert "result" in init_response
        
        # List tools
        tools_response = client.list_tools()
        tool_names = [t["name"] for t in tools_response["result"]["tools"]]
        assert "add_task" in tool_names
        
        # Create task
        create_response = client.call_tool("add_task", {
            "title": "Integration Test Task",
            "priority": "high"
        })
        assert "created" in create_response["result"]["content"][0]["text"].lower()
        
        print("✅ All integration tests passed!")
        
    finally:
        client.close()

if __name__ == "__main__":
    test_full_workflow()
```

---

# Module 7: Deploying Your MCP Server to Azure (Simple)

## 7.1 Why Deploy to Azure?

A locally running MCP server only works on your machine over `stdio`. When you deploy to Azure, you expose it over HTTP + SSE (Server-Sent Events), so any Copilot client or teammate can reach it.

```
┌──────────────┐  HTTPS/SSE  ┌────────────────────────────┐
│  VS Code /   │ ──────────► │  Azure Container Apps       │
│  Any Client  │             │  (your MCP server)          │
└──────────────┘             └────────────────────────────┘
```

---

## Exercise 7.1: Switch from stdio → HTTP (SSE) Transport

**Goal**: Make your MCP server reachable over HTTP so it can be deployed anywhere.

### Step 1: Install extra dependencies

```powershell
pip install mcp[sse] uvicorn
```

### Step 2: Create `cloud_server.py`

```python
"""
Exercise 7.1: HTTP/SSE MCP Server (cloud-ready)
================================================
Identical tools to the task manager, but served over HTTP
so it can be deployed to Azure Container Apps.
"""

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn

app = Server("task-manager-cloud")
DATA_FILE = Path(os.environ.get("DATA_FILE", "tasks.json"))

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"tasks": [], "next_id": 1}

def save_tasks(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "title":    {"type": "string", "description": "Task title"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["task_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    data = load_tasks()

    if name == "add_task":
        task = {
            "id": data["next_id"],
            "title": arguments["title"],
            "priority": arguments.get("priority", "medium"),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        data["tasks"].append(task)
        data["next_id"] += 1
        save_tasks(data)
        return [TextContent(type="text", text=f"✅ Task #{task['id']} created: {task['title']}")]

    elif name == "list_tasks":
        tasks = data["tasks"]
        if not tasks:
            return [TextContent(type="text", text="No tasks yet.")]
        lines = [f"{'✅' if t['status']=='completed' else '⏳'} #{t['id']} [{t['priority']}] {t['title']}" for t in tasks]
        return [TextContent(type="text", text="📋 Tasks:\n" + "\n".join(lines))]

    elif name == "complete_task":
        for task in data["tasks"]:
            if task["id"] == arguments["task_id"]:
                task["status"] = "completed"
                save_tasks(data)
                return [TextContent(type="text", text=f"✅ Task #{task['id']} completed!")]
        return [TextContent(type="text", text=f"❌ Task #{arguments['task_id']} not found.")]

    raise ValueError(f"Unknown tool: {name}")

# ── SSE transport wiring ──────────────────────────────────────────────────────
sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

async def health(request):
    return JSONResponse({"status": "ok", "server": "task-manager-cloud"})

starlette_app = Starlette(
    routes=[
        Route("/health", health),
        Route("/sse",    handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
```

### Step 3: Test locally first

```powershell
python cloud_server.py
# Server starts on http://localhost:8000

# In another terminal, verify health endpoint:
curl http://localhost:8000/health
# {"status": "ok", "server": "task-manager-cloud"}
```

### ✅ Checkpoint 7.1
- [ ] Server starts with `uvicorn`
- [ ] `/health` returns `{"status": "ok"}`
- [ ] `/sse` endpoint is reachable

---

## Exercise 7.2: Containerize with Docker

### Step 1: Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY cloud_server.py .

# Data directory (mounted as a volume in production)
RUN mkdir -p /app/data
ENV DATA_FILE=/app/data/tasks.json

EXPOSE 8000

CMD ["python", "cloud_server.py"]
```

### Step 2: Create `requirements.txt`

```
mcp[sse]>=1.0.0
uvicorn>=0.30.0
starlette>=0.37.0
```

### Step 3: Build and test the container

```powershell
# Build image
docker build -t mcp-task-manager .

# Run locally with a data volume
docker run -p 8000:8000 -v ${PWD}/data:/app/data mcp-task-manager

# Verify
curl http://localhost:8000/health
```

### ✅ Checkpoint 7.2
- [ ] Docker image builds without errors
- [ ] Container runs and serves on port 8000
- [ ] Data persists across container restarts via volume

---

## Exercise 7.3: Deploy to Azure Container Apps

**Goal**: Push the container to Azure and get a public HTTPS endpoint in ~5 minutes.

### Prerequisites
```powershell
# Install Azure CLI if needed
winget install Microsoft.AzureCLI

# Log in
az login

# Install Container Apps extension
az extension add --name containerapp --upgrade
```

### Step 1: Create Azure resources

```powershell
# Set variables (change these to your own values)
$RESOURCE_GROUP = "rg-mcp-demo"
$LOCATION       = "eastus"
$ACR_NAME       = "acrmcpdemo$(Get-Random -Maximum 9999)"   # must be globally unique
$APP_NAME       = "mcp-task-manager"
$ENV_NAME       = "mcp-env"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create `
  --resource-group $RESOURCE_GROUP `
  --name $ACR_NAME `
  --sku Basic `
  --admin-enabled true
```

### Step 2: Push your image to ACR

```powershell
# Build & push directly to ACR (no local Docker daemon needed)
az acr build `
  --registry $ACR_NAME `
  --image mcp-task-manager:latest .

# Get the registry credentials
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
$ACR_SERVER   = "$ACR_NAME.azurecr.io"
```

### Step 3: Create Container Apps environment and deploy

```powershell
# Create the Container Apps environment
az containerapp env create `
  --name $ENV_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION

# Deploy the app
az containerapp create `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENV_NAME `
  --image "$ACR_SERVER/mcp-task-manager:latest" `
  --registry-server $ACR_SERVER `
  --registry-username $ACR_NAME `
  --registry-password $ACR_PASSWORD `
  --target-port 8000 `
  --ingress external `
  --min-replicas 0 `
  --max-replicas 3 `
  --env-vars DATA_FILE="/tmp/tasks.json"

# Get the public URL
$APP_URL = az containerapp show `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "✅ MCP Server deployed at: https://$APP_URL"
```

### Step 4: Verify deployment

```powershell
# Health check
curl "https://$APP_URL/health"

# View live logs
az containerapp logs show `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --follow
```

### Step 5: Connect VS Code to your deployed server

Add to `.vscode/settings.json`:

```json
{
    "mcp": {
        "servers": {
            "task-manager-cloud": {
                "url": "https://<YOUR_APP_URL>/sse"
            }
        }
    }
}
```

> **Note**: Replace `<YOUR_APP_URL>` with the FQDN printed in Step 3.  
> The `url` key (instead of `command`) tells VS Code to connect to a remote SSE endpoint.

### ✅ Checkpoint 7.3
- [ ] Image pushed to ACR successfully
- [ ] Container App shows `Running` state
- [ ] `curl https://<APP_URL>/health` returns `{"status":"ok"}`
- [ ] VS Code Copilot calls tools on the deployed server

### 🧹 Cleanup (optional)

```powershell
# Remove all resources when done
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

### 🏆 Challenge 7
- Add an Azure Storage Blob backend so tasks persist across container restarts
- Enable Azure Managed Identity so no credentials are stored in environment variables
- Add a GitHub Actions workflow that automatically rebuilds and redeploys on every `git push`

---

# Module 8: Custom Prompts & Skills for Your MCP Server

## 8.1 What Are Prompts and Skills?

| Concept | Where it lives | Purpose |
|---------|---------------|---------|
| **MCP Prompt** | Inside your MCP server | Pre-built conversation templates the AI invokes |
| **VS Code `.prompt.md`** | `.github/prompts/` | Reusable slash-commands for Copilot Chat |
| **VS Code `.instructions.md`** | `.github/instructions/` | Always-on rules that shape how Copilot behaves |

This module covers all three so you can pick the right tool for the job.

---

## Exercise 8.1: Add a Prompt to Your MCP Server

**Goal**: Expose a `task_review` prompt that primes the AI to analyse your task list.

Add this block to `cloud_server.py` (after the `call_tool` handler):

```python
from mcp.types import Prompt, PromptArgument, PromptMessage

@app.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="task_review",
            description="Review all tasks and suggest what to tackle next",
            arguments=[]           # no arguments needed – loads live data
        ),
        Prompt(
            name="task_standup",
            description="Generate a daily standup summary from the task list",
            arguments=[
                PromptArgument(
                    name="your_name",
                    description="Your name for the standup report",
                    required=False
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None):
    data = load_tasks()
    tasks = data["tasks"]

    if name == "task_review":
        pending   = [t for t in tasks if t["status"] == "pending"]
        completed = [t for t in tasks if t["status"] == "completed"]
        task_list = "\n".join(
            f"- #{t['id']} [{t['priority'].upper()}] {t['title']}" for t in pending
        ) or "No pending tasks."

        prompt_text = f"""
You are a productivity coach reviewing my task list.

## Pending Tasks ({len(pending)})
{task_list}

## Completed Tasks: {len(completed)}

Please:
1. Identify the highest-impact task to tackle first.
2. Flag any tasks that look blocked or need more info.
3. Suggest if any tasks can be batched or delegated.
"""
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text.strip()))]

    elif name == "task_standup":
        name_str  = (arguments or {}).get("your_name", "Team Member")
        pending   = [t for t in tasks if t["status"] == "pending"]
        completed = [t for t in tasks if t["status"] == "completed"]

        prompt_text = f"""
Generate a concise daily standup update for {name_str}.

Completed:
{chr(10).join(f"  ✅ {t['title']}" for t in completed) or "  (nothing yet)"}

In Progress / Pending:
{chr(10).join(f"  ⏳ [{t['priority']}] {t['title']}" for t in pending) or "  (nothing pending)"}

Format it as: Yesterday | Today | Blockers
Keep it under 5 bullet points total.
"""
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text.strip()))]

    raise ValueError(f"Unknown prompt: {name}")
```

### Test the prompts in VS Code

After restarting your MCP server, type in Copilot Chat:

```
Run the task_review prompt
```

or

```
Run the task_standup prompt with your_name = "Alice"
```

### ✅ Checkpoint 8.1
- [ ] `list_prompts` returns `task_review` and `task_standup`
- [ ] Copilot Chat invokes the prompts and returns useful output
- [ ] Prompts reference live task data

---

## Exercise 8.2: Create a Reusable VS Code `.prompt.md` Skill

**Goal**: Create a reusable slash-command in VS Code that automatically invokes your MCP tools.

### Step 1: Create the prompts directory

```powershell
mkdir .github\prompts
```

### Step 2: Create `.github/prompts/manage-tasks.prompt.md`

```markdown
---
mode: agent
description: Manage my task list using the MCP task manager server
tools:
  - mcp_task_manager_add_task
  - mcp_task_manager_list_tasks
  - mcp_task_manager_complete_task
---

You are a focused task management assistant. You have access to these MCP tools:
- `add_task` – create a new task (requires `title`, optional `priority`: low/medium/high)
- `list_tasks` – list all tasks
- `complete_task` – mark a task done by `task_id`

## Rules
- Always call `list_tasks` first so you know the current state before acting.
- Confirm with the user before marking tasks as complete.
- When adding multiple tasks from a list, add them one at a time and report each ID.
- Keep responses short: one sentence per action taken.

## User request
{{input}}
```

### Step 3: Use the prompt

In VS Code Copilot Chat:

```
/manage-tasks Add three tasks: write tests, update README, deploy to staging
```

Copilot will invoke the MCP `add_task` tool three times and report back.

---

## Exercise 8.3: Create a VS Code `.instructions.md` to Always Load MCP Context

**Goal**: Create an always-on instruction file so Copilot automatically understands your MCP server without you repeating yourself.

### Create `.github/instructions/mcp-task-manager.instructions.md`

```markdown
---
applyTo: "**"
---

# Task Manager MCP – Context for GitHub Copilot

This workspace includes a running MCP server called **task-manager** (or **task-manager-cloud** when deployed).

## Available MCP Tools

| Tool | Description | Required params |
|------|-------------|-----------------|
| `add_task` | Create a task | `title` (string) |
| `list_tasks` | Show all tasks | none |
| `complete_task` | Mark done | `task_id` (int) |

## Available MCP Prompts

| Prompt | Description |
|--------|-------------|
| `task_review` | AI-powered task prioritisation |
| `task_standup` | Daily standup generator |

## Conventions
- Priority levels: `low` | `medium` | `high`  
- Task IDs are sequential integers starting at 1.
- Always call `list_tasks` to get current state before making changes.

## Deployment
- Local: `python cloud_server.py` → `http://localhost:8000/sse`
- Azure: `https://<APP_URL>/sse` (set in `.vscode/settings.json`)
```

With `applyTo: "**"`, this instruction is included in every Copilot Chat session — no need to re-explain your MCP server each time.

### ✅ Checkpoint 8.3
- [ ] `.instructions.md` created with correct frontmatter
- [ ] Copilot uses MCP tools without you explaining the schema
- [ ] VS Code shows the instruction file in the Copilot context pane

---

## 8.4 Quick Reference: Choosing the Right Mechanism

```
Need the AI to run a canned workflow?
  └─► MCP Prompt  (server-side, data-aware, returned via get_prompt)

Need a slash-command that chains multiple tool calls?
  └─► .prompt.md  (client-side, lives in .github/prompts/)

Need Copilot to always know about your tools/conventions?
  └─► .instructions.md  (always-on, lives in .github/instructions/)
```

---

# Final Challenges

## 🏆 Challenge: Build a Complete Project Management MCP Server

Create an MCP server for project management with:

### Requirements:
1. **Projects** - Create, list, update, delete projects
2. **Tasks** - Create tasks within projects, assign to users
3. **Users** - Create users, assign roles
4. **Time Tracking** - Log time against tasks
5. **Reports** - Generate project reports via prompts
6. **Resources** - Expose project data as resources

### Deliverables:
- [ ] Full MCP server with 10+ tools
- [ ] At least 3 resources
- [ ] At least 2 prompts
- [ ] Unit tests with 80%+ coverage
- [ ] VS Code integration
- [ ] Documentation

### Grading Rubric:
| Criteria | Points |
|----------|--------|
| Tool implementation | 30 |
| Error handling | 20 |
| Resource/Prompt implementation | 20 |
| Testing | 15 |
| Code quality | 10 |
| Documentation | 5 |
| **Total** | **100** |

---

## 📚 Additional Resources

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [VS Code MCP Integration](https://code.visualstudio.com/docs)
- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/)

---

## ✅ Lab Completion Checklist

- [ ] Module 1: Created Hello World MCP server
- [ ] Module 1: Built Calculator with multiple tools
- [ ] Module 2: Created Task Manager with persistence
- [ ] Module 2: Integrated with VS Code
- [ ] Module 3: Implemented Resources
- [ ] Module 3: Implemented Prompts
- [ ] Module 4: Built Weather API integration
- [ ] Module 5: Applied error handling patterns
- [ ] Module 6: Wrote unit tests
- [ ] Module 7: Switched server to HTTP/SSE transport
- [ ] Module 7: Containerized server with Docker
- [ ] Module 7: Deployed to Azure Container Apps
- [ ] Module 7: Connected VS Code to remote MCP endpoint
- [ ] Module 8: Added MCP Prompts (task_review, task_standup)
- [ ] Module 8: Created `.prompt.md` slash-command skill
- [ ] Module 8: Created `.instructions.md` always-on context
- [ ] Final Challenge: Completed project management server

**Congratulations on completing the MCP Fundamentals Lab!** 🎉
