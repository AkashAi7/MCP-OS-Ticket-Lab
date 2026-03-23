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

Before starting, **verify every tool is installed correctly**. Open **PowerShell** (press `Win + X` → "Windows Terminal" or search "PowerShell" in Start Menu) and run each check command.

| Requirement | Minimum Version | Check Command | Expected Output |
|-------------|----------------|---------------|-----------------|
| Python | 3.10+ | `python --version` | `Python 3.10.x` or higher |
| pip | Latest | `pip --version` | `pip 23.x ...` |
| Node.js | 18+ | `node --version` | `v18.x.x` or higher |
| VS Code | Latest | `code --version` | `1.8x.x` or higher |
| Git | Any | `git --version` | `git version 2.x.x` |

### Step-by-step prerequisite verification

**1. Open PowerShell as your working terminal**

Press `Win + X` on your keyboard and click **"Terminal"** (or **"Windows PowerShell"**).
You should see a blue/dark prompt like:
```
PS C:\Users\YourName>
```

**2. Check Python**
```powershell
python --version
```
Expected output:
```
Python 3.11.4
```
If you see `Python 2.x` or `'python' is not recognized`, download Python 3.11+ from [python.org](https://www.python.org/downloads/). During installation, **tick "Add Python to PATH"**.

**3. Check pip (Python package manager)**
```powershell
pip --version
```
Expected output:
```
pip 23.3.1 from C:\Python311\Lib\site-packages\pip (python 3.11)
```

**4. Check Node.js**
```powershell
node --version
```
Expected output:
```
v20.10.0
```
If missing, download from [nodejs.org](https://nodejs.org/) and install the LTS version.

**5. Check VS Code is installed and in PATH**
```powershell
code --version
```
Expected output:
```
1.87.0
...
```
If missing, download from [code.visualstudio.com](https://code.visualstudio.com/) and install it.

**6. Confirm VS Code has the GitHub Copilot extension**

Inside VS Code (`code .` to open it), press `Ctrl + Shift + X` to open Extensions. Search for "GitHub Copilot" and verify it shows as **installed and enabled** (green checkmark). If not, click **Install**.

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

**Goal**: Create a minimal MCP server with one tool (`say_hello`) and verify it works end to end.

**Estimated time**: 15–20 minutes

---

### Step 1: Decide where to work

> **Rule of thumb for this entire lab**: keep everything inside one dedicated folder on your Desktop so paths are short and easy to type.

In PowerShell, create that folder now:

```powershell
# Navigate to your Desktop first
cd "$env:USERPROFILE\Desktop"

# Create a lab root folder (all exercises live here)
mkdir mcp-lab
cd mcp-lab
```

You should now see:
```
PS C:\Users\YourName\Desktop\mcp-lab>
```

> **Keep this PowerShell window open for the rest of Exercise 1.1.** Every command below is run here unless the step says to switch to VS Code.

---

### Step 2: Create the Exercise 1.1 project folder

Still inside `mcp-lab`, run:

```powershell
# Create a subfolder for this exercise
mkdir ex1-hello-world
cd ex1-hello-world
```

Your prompt should now read:
```
PS C:\Users\YourName\Desktop\mcp-lab\ex1-hello-world>
```

---

### Step 3: Create and activate a Python virtual environment

A virtual environment keeps this exercise's packages isolated from your system Python. Run these commands **one at a time**:

```powershell
# Create the virtual environment (creates a folder called 'venv')
python -m venv venv
```

Expected output: silent (no output means success).

```powershell
# Activate the virtual environment
.\venv\Scripts\Activate
```

Expected output — your prompt now shows `(venv)` at the front:
```
(venv) PS C:\Users\YourName\Desktop\mcp-lab\ex1-hello-world>
```

> **Important**: You must see `(venv)` before running any `pip install` or `python` command. If you close and reopen PowerShell, run `.\venv\Scripts\Activate` again.

---

### Step 4: Install the MCP SDK

```powershell
pip install "mcp[cli]"
```

Watch the output scroll by. The last lines should look like:
```
Successfully installed mcp-1.x.x ... (several packages)
```

Verify the install worked:
```powershell
python -c "import importlib.metadata; print('MCP version:', importlib.metadata.version('mcp'))"
```

Expected output:
```
MCP version: 1.x.x
```

If you see `ModuleNotFoundError`, your virtual environment is not activated — re-run `.\venv\Scripts\Activate`.

---

### Step 5: Open this folder in VS Code

> **First time opening VS Code in this exercise.**

In the same PowerShell window, run:

```powershell
code .
```

VS Code will open with `ex1-hello-world` as the workspace root. You should see:
- A file explorer on the left showing only the `venv/` folder so far.
- The title bar showing `ex1-hello-world`.

> **Leave VS Code open.** You will create all files in it. Keep the PowerShell window open in the background for running commands.

---

### Step 6: Create `server.py`

In VS Code:
1. Click the **New File** icon in the Explorer panel (hover over the `ex1-hello-world` heading to see it), **or** press `Ctrl + N` then `Ctrl + S` to save.
2. Name the file **`server.py`** (save it directly inside `ex1-hello-world`, NOT inside the `venv` folder).
3. Paste the following code:

```python
"""
Exercise 1.1: Hello World MCP Server
=====================================
This is the simplest possible MCP server.
It exposes one tool: say_hello(name) -> "Hello, {name}! Welcome to MCP!"
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

# Create server instance — the string is the server's display name
app = Server("hello-world")

# ── Tool declaration ──────────────────────────────────────────────────────────
# list_tools() returns the catalogue of tools this server offers.
# The AI reads this catalogue to know what it can call.
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
                "required": ["name"]   # 'name' must be provided
            }
        )
    ]

# ── Tool execution ────────────────────────────────────────────────────────────
# call_tool() is invoked when the AI decides to use a tool.
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute tool calls."""
    if name == "say_hello":
        person_name = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {person_name}! Welcome to MCP!")]
    raise ValueError(f"Unknown tool: {name}")

# ── Server startup ────────────────────────────────────────────────────────────
# stdio_server wires the server to standard input/output (how VS Code talks to it).
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

4. Save the file: `Ctrl + S`.

Your `ex1-hello-world` folder should now contain:
```
ex1-hello-world/
├── venv/           ← created by python -m venv (do not edit)
└── server.py       ← the file you just created ✓
```

---

### Step 7: Verify the server starts cleanly

Switch back to PowerShell (click it in the taskbar). Make sure `(venv)` is still showing, then run:

```powershell
python server.py
```

The server will appear to **hang** (no output, blinking cursor). This is **correct** — it is waiting for a client to connect over stdio. Press `Ctrl + C` to stop it.

You should see output like:
```
^CTraceback (most recent call last):
  ...
KeyboardInterrupt
```

That `KeyboardInterrupt` is normal. The key point: **no Python errors appeared before you pressed Ctrl+C**. If you see a red error message (e.g., `ImportError`), check Step 4.

---

### Step 8: Create `test_hello.py` and run it

Now you will send a real MCP message to the server and read the response.

In **VS Code**, create a new file called **`test_hello.py`** in the same folder as `server.py`:

```python
"""
test_hello.py
=============
Sends an MCP 'initialize' request to server.py and prints the response.
Run this in PowerShell: python test_hello.py
"""
import subprocess
import json
import sys

def test_server():
    print("Starting server.py as a subprocess...")

    # Launch server.py — it listens on stdin, writes to stdout
    process = subprocess.Popen(
        [sys.executable, "server.py"],   # sys.executable = the current python
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # --- 1. Send the MCP 'initialize' handshake ---
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }
    print(f"Sending: initialize")
    process.stdin.write(json.dumps(init_request) + "\n")
    process.stdin.flush()

    init_response_raw = process.stdout.readline()
    init_response = json.loads(init_response_raw)
    server_name = init_response["result"]["serverInfo"]["name"]
    print(f"✅ Server responded. Server name: '{server_name}'")

    # --- 2. Ask for the list of tools ---
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    print("Sending: tools/list")
    process.stdin.write(json.dumps(list_tools_request) + "\n")
    process.stdin.flush()

    tools_response_raw = process.stdout.readline()
    tools_response = json.loads(tools_response_raw)
    tools = tools_response["result"]["tools"]
    print(f"✅ Server has {len(tools)} tool(s): {[t['name'] for t in tools]}")

    # --- 3. Call the say_hello tool ---
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "say_hello",
            "arguments": {"name": "MCP Student"}
        }
    }
    print("Sending: tools/call say_hello(name='MCP Student')")
    process.stdin.write(json.dumps(call_request) + "\n")
    process.stdin.flush()

    call_response_raw = process.stdout.readline()
    call_response = json.loads(call_response_raw)
    result_text = call_response["result"]["content"][0]["text"]
    print(f"✅ Tool response: '{result_text}'")

    process.terminate()
    print("\n🎉 All tests passed! Your MCP server is working correctly.")

if __name__ == "__main__":
    test_server()
```

Save it (`Ctrl + S`). Your folder now looks like:
```
ex1-hello-world/
├── venv/
├── server.py
└── test_hello.py   ← just created ✓
```

Switch to **PowerShell** and run:

```powershell
python test_hello.py
```

**Expected output** (exact text):
```
Starting server.py as a subprocess...
Sending: initialize
✅ Server responded. Server name: 'hello-world'
Sending: tools/list
✅ Server has 1 tool(s): ['say_hello']
Sending: tools/call say_hello(name='MCP Student')
✅ Tool response: 'Hello, MCP Student! Welcome to MCP!'

🎉 All tests passed! Your MCP server is working correctly.
```

If the output matches, your server is fully working. If it hangs or errors, see the troubleshooting note below.

> **Troubleshooting**: If `test_hello.py` hangs indefinitely, it usually means `server.py` is crashing silently. Run `python server.py` on its own first to confirm no import errors exist.

---

### ✅ Checkpoint 1.1

Tick each box only after confirming it with your own eyes:

- [ ] Running `python server.py` alone produces no error before `Ctrl+C`
- [ ] Running `python test_hello.py` prints all three ✅ lines
- [ ] The tool response text is `'Hello, MCP Student! Welcome to MCP!'`
- [ ] You understand: `list_tools()` declares what exists; `call_tool()` executes it

---

## Exercise 1.2: Adding Multiple Tools

**Goal**: Extend your server with multiple tools (calculator) and understand how to test each one.

**Estimated time**: 20 minutes

---

### Step 1: Create a new project folder for this exercise

> **Start here in PowerShell.** You should still have the `(venv)` from Exercise 1.1 active, but this exercise gets its own folder.

```powershell
# Navigate back to your lab root
cd "$env:USERPROFILE\Desktop\mcp-lab"

# Create a subfolder for this exercise
mkdir ex2-calculator
cd ex2-calculator
```

Your prompt:
```
PS C:\Users\YourName\Desktop\mcp-lab\ex2-calculator>
```

```powershell
# Create and activate a fresh virtual environment
python -m venv venv
.\venv\Scripts\Activate
```

Your prompt should now show `(venv)`:
```
(venv) PS C:\Users\YourName\Desktop\mcp-lab\ex2-calculator>
```

```powershell
# Install MCP
pip install "mcp[cli]"
```

Expected last line: `Successfully installed mcp-1.x.x ...`

---

### Step 2: Open this folder in VS Code

```powershell
code .
```

VS Code opens. The Explorer panel on the left shows only `venv/`. The title bar shows `ex2-calculator`.

> From now on, **create all files in VS Code** and **run all commands in the PowerShell window**.

---

### Step 3: Create `calculator_server.py`

In VS Code, press `Ctrl + N` (new file), then immediately `Ctrl + S` and name it **`calculator_server.py`** — save it at the root of `ex2-calculator` (not inside `venv`).

Paste this code:

```python
"""
Exercise 1.2: Multi-Tool Calculator Server
==========================================
Demonstrates exposing multiple tools from one MCP server.
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

Save with `Ctrl + S`.

Your folder structure:
```
ex2-calculator/
├── venv/
└── calculator_server.py   ← just created ✓
```

---

### Step 4: Verify the server starts

Switch to PowerShell and run:

```powershell
python calculator_server.py
```

It should hang (waiting for connections). Press `Ctrl + C`.

You should see `KeyboardInterrupt` and **no ImportError**. If you see an error, double-check the file was saved correctly.

---

### Step 5: Create `test_calculator.py` and run it

In **VS Code**, create a new file: `Ctrl + N`, save as **`test_calculator.py`** in the same `ex2-calculator` folder. Paste:

```python
"""
test_calculator.py
==================
Tests each tool in the calculator server in sequence.
Run: python test_calculator.py
"""
import subprocess
import json
import sys

def send(process, method, params=None):
    """Send one JSON-RPC request and return the parsed response."""
    request = {
        "jsonrpc": "2.0",
        "id": send.counter,
        "method": method,
        "params": params or {}
    }
    send.counter += 1
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    return json.loads(process.stdout.readline())

send.counter = 1

def call_tool(process, name, arguments):
    return send(process, "tools/call", {"name": name, "arguments": arguments})

def test_calculator():
    print("Starting calculator_server.py...")
    process = subprocess.Popen(
        [sys.executable, "calculator_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Handshake
    send(process, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    })

    # Confirm tool list
    tools_resp = send(process, "tools/list")
    names = [t["name"] for t in tools_resp["result"]["tools"]]
    print(f"Available tools: {names}")
    assert set(names) == {"add", "multiply", "sqrt", "factorial"}, "Tool list mismatch!"

    # Test add
    r = call_tool(process, "add", {"a": 10, "b": 5})
    text = r["result"]["content"][0]["text"]
    assert text == "Result: 15", f"Unexpected: {text}"
    print(f"✅ add(10, 5) = {text}")

    # Test multiply
    r = call_tool(process, "multiply", {"a": 6, "b": 7})
    text = r["result"]["content"][0]["text"]
    assert text == "Result: 42", f"Unexpected: {text}"
    print(f"✅ multiply(6, 7) = {text}")

    # Test sqrt
    r = call_tool(process, "sqrt", {"number": 144})
    text = r["result"]["content"][0]["text"]
    assert "12" in text, f"Unexpected: {text}"
    print(f"✅ sqrt(144) = {text}")

    # Test factorial
    r = call_tool(process, "factorial", {"n": 5})
    text = r["result"]["content"][0]["text"]
    assert "120" in text, f"Unexpected: {text}"
    print(f"✅ factorial(5) = {text}")

    process.terminate()
    print("\n🎉 All calculator tests passed!")

if __name__ == "__main__":
    test_calculator()
```

Save (`Ctrl + S`). Your folder:
```
ex2-calculator/
├── venv/
├── calculator_server.py
└── test_calculator.py   ← just created ✓
```

Switch to PowerShell, run:

```powershell
python test_calculator.py
```

**Expected output:**
```
Starting calculator_server.py...
Available tools: ['add', 'multiply', 'sqrt', 'factorial']
✅ add(10, 5) = Result: 15
✅ multiply(6, 7) = Result: 42
✅ sqrt(144) = √144.0 = 12.0
✅ factorial(5) = 5! = 120

🎉 All calculator tests passed!
```

---

### ✅ Checkpoint 1.2

- [ ] `calculator_server.py` is in `ex2-calculator/` (not inside `venv/`)
- [ ] `python calculator_server.py` produces no errors before `Ctrl+C`
- [ ] `python test_calculator.py` shows all four ✅ lines
- [ ] You understand why `raise ValueError(f"Unknown tool: {name}")` goes at the bottom

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

**Estimated time**: 25 minutes

---

### Step 1: Create the project folder

> **Switch to PowerShell.** Make sure your previous venv is NOT active, or open a fresh PowerShell window.

```powershell
# Navigate back to your lab root
cd "$env:USERPROFILE\Desktop\mcp-lab"

# Create a subfolder for this exercise
mkdir ex3-task-manager
cd ex3-task-manager
```

Your prompt:
```
PS C:\Users\YourName\Desktop\mcp-lab\ex3-task-manager>
```

```powershell
# Set up a fresh virtual environment
python -m venv venv
.\venv\Scripts\Activate
pip install "mcp[cli]"
```

---

### Step 2: Open the folder in VS Code

```powershell
code .
```

VS Code opens showing `ex3-task-manager` as the workspace root. You should see only `venv/` in the Explorer.

---

### Step 3: Create `task_manager_server.py`

In VS Code: press `Ctrl + N`, then `Ctrl + S`, name the file **`task_manager_server.py`** and save it at the **root** of `ex3-task-manager` (same level as `venv/`, NOT inside it).

Paste this code:

```python
"""
Exercise 2.1: Task Manager MCP Server
=====================================
A practical example with file-based persistence.
Tasks are saved to tasks.json in the same folder as this script.
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

# tasks.json will be created automatically next to this script
DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    """Load tasks from JSON file, or return empty structure if it doesn't exist yet."""
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
                output = f"""Task #{task['id']}
- Title: {task['title']}
- Description: {task.get('description', 'N/A')}
- Priority: {task['priority']}
- Status: {task['status']}
- Due Date: {task.get('due_date', 'Not set')}
- Created: {task['created_at']}"""
                return [TextContent(type="text", text=output.strip())]
        return [TextContent(type="text", text=f"❌ Task #{task_id} not found.")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

Save with `Ctrl + S`.

Your folder structure:
```
ex3-task-manager/
├── venv/
└── task_manager_server.py   ← just created ✓
```

---

### Step 4: Verify the server starts cleanly

Switch to PowerShell:

```powershell
python task_manager_server.py
```

It should hang (no output). Press `Ctrl + C`. You should see `KeyboardInterrupt` and no errors.

---

### Step 5: Create `test_task_manager.py`

In **VS Code**: `Ctrl + N`, save as **`test_task_manager.py`** in the same `ex3-task-manager` folder. Paste:

```python
"""
test_task_manager.py
====================
End-to-end test for the task manager server.
Run: python test_task_manager.py
"""
import subprocess
import json
import sys
import os

def send(process, method, params=None, _id=[1]):
    req = {"jsonrpc": "2.0", "id": _id[0], "method": method, "params": params or {}}
    _id[0] += 1
    process.stdin.write(json.dumps(req) + "\n")
    process.stdin.flush()
    return json.loads(process.stdout.readline())

def tool(process, name, args):
    return send(process, "tools/call", {"name": name, "arguments": args})

def test_tasks():
    # Clean slate — remove leftover tasks.json from a previous run
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")

    print("Starting task_manager_server.py...")
    proc = subprocess.Popen(
        [sys.executable, "task_manager_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Handshake
    send(proc, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    })

    # 1 — Add tasks
    r = tool(proc, "add_task", {"title": "Write unit tests", "priority": "high"})
    print(f"✅ {r['result']['content'][0]['text']}")

    r = tool(proc, "add_task", {"title": "Update README", "priority": "low"})
    print(f"✅ {r['result']['content'][0]['text']}")

    # 2 — List all tasks
    r = tool(proc, "list_tasks", {})
    text = r["result"]["content"][0]["text"]
    assert "Write unit tests" in text and "Update README" in text
    print("✅ list_tasks shows both tasks")

    # 3 — Get a specific task
    r = tool(proc, "get_task", {"task_id": 1})
    text = r["result"]["content"][0]["text"]
    assert "Write unit tests" in text
    print("✅ get_task(1) returns correct task")

    # 4 — Complete task #1
    r = tool(proc, "complete_task", {"task_id": 1})
    text = r["result"]["content"][0]["text"]
    assert "completed" in text.lower()
    print("✅ complete_task(1) succeeded")

    # 5 — Filter to pending only
    r = tool(proc, "list_tasks", {"status": "pending"})
    text = r["result"]["content"][0]["text"]
    assert "Update README" in text
    assert "Write unit tests" not in text
    print("✅ list_tasks(status=pending) shows only pending task")

    # 6 — Delete task #2
    r = tool(proc, "delete_task", {"task_id": 2})
    text = r["result"]["content"][0]["text"]
    assert "deleted" in text.lower()
    print("✅ delete_task(2) succeeded")

    # 7 — Try to get deleted task
    r = tool(proc, "get_task", {"task_id": 2})
    text = r["result"]["content"][0]["text"]
    assert "not found" in text.lower()
    print("✅ get_task(2) correctly says 'not found'")

    proc.terminate()
    print("\n🎉 All task manager tests passed!")
    print("   Check the tasks.json file — it should show the final state.")

if __name__ == "__main__":
    test_tasks()
```

Save (`Ctrl + S`). Your folder:
```
ex3-task-manager/
├── venv/
├── task_manager_server.py
└── test_task_manager.py   ← just created ✓
```

Switch to PowerShell, run:

```powershell
python test_task_manager.py
```

**Expected output:**
```
Starting task_manager_server.py...
✅ Task #1 created: Write unit tests
✅ Task #2 created: Update README
✅ list_tasks shows both tasks
✅ get_task(1) returns correct task
✅ complete_task(1) succeeded
✅ list_tasks(status=pending) shows only pending task
✅ delete_task(2) succeeded
✅ get_task(2) correctly says 'not found'

🎉 All task manager tests passed!
   Check the tasks.json file — it should show the final state.
```

### Step 6: Inspect the data file

In VS Code, look at the Explorer panel on the left. You should now see a new **`tasks.json`** file appear:

```
ex3-task-manager/
├── venv/
├── task_manager_server.py
├── test_task_manager.py
└── tasks.json   ← automatically created by the server ✓
```

Click **`tasks.json`** in the Explorer to open it. You should see task #1 with status `"completed"`.

> **This confirms persistence works**: even after the server process was terminated, the data survived in the JSON file.

---

### ✅ Checkpoint 2.1

- [ ] `task_manager_server.py` is saved in `ex3-task-manager/` (not inside `venv/`)
- [ ] `python test_task_manager.py` shows all seven ✅ lines
- [ ] `tasks.json` was automatically created and contains task data
- [ ] You understand: `DATA_FILE = Path(__file__).parent / "tasks.json"` places the file next to the script

### 🏆 Challenge 2.1
Extend the task manager with:
1. `update_task` - Update task title, description, or priority
2. `search_tasks` - Search tasks by keyword
3. `get_statistics` - Return task statistics (total, completed, pending by priority)

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

**Goal**: Register your MCP server with VS Code Copilot so you can talk to it using natural language.

**Estimated time**: 10 minutes

---

### Step 1: Make sure VS Code is open on `ex3-task-manager`

Check the VS Code title bar. It should say **`ex3-task-manager`**. If it shows a different folder, go to **File → Open Folder** and browse to:
```
C:\Users\YourName\Desktop\mcp-lab\ex3-task-manager
```

---

### Step 2: Create the VS Code settings file

MCP servers are registered in a `.vscode/settings.json` file inside your workspace folder.

In VS Code:
1. In the Explorer panel, hover over the `ex3-task-manager` heading.
2. Click the **New Folder** icon and name the folder **`.vscode`** (the dot prefix is important — do not accidentally name it `vscode`).
3. Click on the new `.vscode` folder to select it.
4. Click **New File** and name the file **`settings.json`**.

Your folder structure now:
```
ex3-task-manager/
├── .vscode/
│   └── settings.json   ← just created ✓
├── venv/
├── task_manager_server.py
├── test_task_manager.py
└── tasks.json
```

5. Open **`settings.json`** (click it in the Explorer) and paste this content:

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

> **What this does**: tells VS Code to launch `python task_manager_server.py` whenever it needs to talk to your MCP server. `${workspaceFolder}` expands to the absolute path of `ex3-task-manager`.

6. Save with `Ctrl + S`.

---

### Step 3: Reload VS Code to pick up the new settings

Press `Ctrl + Shift + P` to open the Command Palette, type **"Developer: Reload Window"**, and press `Enter`.

VS Code will restart in the same folder. Wait for it to finish loading (the status bar stops spinning).

---

### Step 4: Test MCP in Copilot Chat

1. Open Copilot Chat: press `Ctrl + Shift + I` (or click the Chat icon in the Activity Bar on the left).
2. Make sure **Agent mode** is selected (look for a dropdown or toggle at the top of the Chat panel that says "Ask" vs "Agent" — select **Agent**).
3. In the chat input box, type:

```
Add a new high priority task titled "Review pull requests"
```

4. Press `Enter`.

Copilot will think for a moment, then call your MCP tool. You should see it show a tool invocation like:

```
Using tool: add_task
Arguments: { "title": "Review pull requests", "priority": "high" }
```

Followed by a response like:
```
✅ Task #1 created: Review pull requests
```

5. Now ask:

```
List all my tasks
```

You should see:
```
📋 Tasks:
⏳ #1 [🔴] Review pull requests
```

6. Finally:

```
Mark task 1 as complete
```

Copilot should call `complete_task` with `task_id: 1` and confirm it's done.

> **Troubleshooting**: If Copilot says it can't find any MCP tools, check:
> - The `.vscode/settings.json` path is correct (`"command": "python"` not `"python3"`)
> - You reloaded the window after saving settings
> - The venv Python is in your PATH (`python --version` works in PowerShell)

---

### ✅ Checkpoint 2.2

- [ ] `.vscode/settings.json` file exists with the correct MCP configuration
- [ ] After reloading VS Code, Copilot shows MCP tools available
- [ ] Copilot successfully called `add_task` and created a task
- [ ] Tasks persist in `tasks.json` between Copilot sessions

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

**Goal**: Create a complete MCP server with tools, resources, and prompts — all in one file.

**Estimated time**: 30 minutes

---

### Step 1: Create the project folder

In PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab"
mkdir ex5-complete-server
cd ex5-complete-server

python -m venv venv
.\venv\Scripts\Activate
pip install "mcp[cli]"
```

---

### Step 2: Open the folder in VS Code

```powershell
code .
```

VS Code opens. Confirm the title bar says `ex5-complete-server`.

---

### Step 3: Create `complete_server.py`

In VS Code: `Ctrl + N`, save as **`complete_server.py`** at the root of `ex5-complete-server` (same level as `venv/`). Paste this complete implementation:

```python
"""
Exercise 3.1: Complete MCP Server
=================================
Demonstrates tools, resources, and prompts all working together.
Data is persisted to demo_data.json next to this script.
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
DATA_FILE = Path(__file__).parent / "demo_data.json"

# ── Persistence helpers ───────────────────────────────────────────────────────

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"tasks": [], "next_id": 1}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

# ── Tools ─────────────────────────────────────────────────────────────────────

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
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
                    "due_date": {"type": "string", "description": "Due date YYYY-MM-DD (optional)"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List tasks, optionally filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                }
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID to complete"}
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="get_statistics",
            description="Return task completion statistics",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    data = load_data()

    if name == "add_task":
        task = {
            "id": data["next_id"],
            "title": arguments["title"],
            "priority": arguments.get("priority", "medium"),
            "due_date": arguments.get("due_date"),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        data["tasks"].append(task)
        data["next_id"] += 1
        save_data(data)
        return [TextContent(type="text", text=f"✅ Task #{task['id']} created: {task['title']}")]

    elif name == "list_tasks":
        tasks = data["tasks"]
        status_filter = arguments.get("status", "all")
        if status_filter != "all":
            tasks = [t for t in tasks if t["status"] == status_filter]
        if not tasks:
            return [TextContent(type="text", text="No tasks found.")]
        lines = []
        for t in tasks:
            icon = "✅" if t["status"] == "completed" else "⏳"
            p_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}[t["priority"]]
            lines.append(f"{icon} #{t['id']} [{p_icon}] {t['title']}")
        return [TextContent(type="text", text="📋 Tasks:\n" + "\n".join(lines))]

    elif name == "complete_task":
        task_id = arguments["task_id"]
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                save_data(data)
                return [TextContent(type="text", text=f"✅ Task #{task_id} completed!")]
        return [TextContent(type="text", text=f"❌ Task #{task_id} not found.")]

    elif name == "get_statistics":
        tasks = data["tasks"]
        stats = {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
            "by_priority": {
                "high":   sum(1 for t in tasks if t["priority"] == "high"),
                "medium": sum(1 for t in tasks if t["priority"] == "medium"),
                "low":    sum(1 for t in tasks if t["priority"] == "low"),
            }
        }
        text = (
            f"📊 Statistics\n"
            f"  Total: {stats['total']}\n"
            f"  Completed: {stats['completed']}\n"
            f"  Pending: {stats['pending']}\n"
            f"  High priority: {stats['by_priority']['high']}\n"
            f"  Medium priority: {stats['by_priority']['medium']}\n"
            f"  Low priority: {stats['by_priority']['low']}"
        )
        return [TextContent(type="text", text=text)]

    raise ValueError(f"Unknown tool: {name}")

# ── Resources ─────────────────────────────────────────────────────────────────

@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="tasks://all",
            name="All Tasks",
            description="Complete JSON list of all tasks",
            mimeType="application/json"
        ),
        Resource(
            uri="tasks://statistics",
            name="Task Statistics",
            description="Task completion statistics as JSON",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    data = load_data()

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
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
            "by_priority": {
                "high":   sum(1 for t in tasks if t["priority"] == "high"),
                "medium": sum(1 for t in tasks if t["priority"] == "medium"),
                "low":    sum(1 for t in tasks if t["priority"] == "low"),
            }
        }
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(stats, indent=2)
        )

    raise ValueError(f"Unknown resource: {uri}")

# ── Prompts ───────────────────────────────────────────────────────────────────

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
            description="Analyse a specific task in detail",
            arguments=[
                PromptArgument(
                    name="task_id",
                    description="ID of the task to analyse",
                    required=True
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None):
    data = load_data()
    args = arguments or {}

    if name == "daily_standup":
        tasks = data["tasks"]
        pending = [t for t in tasks if t["status"] == "pending"]
        completed = [t for t in tasks if t["status"] == "completed"]
        report_date = args.get("date", datetime.now().strftime("%Y-%m-%d"))

        pending_lines = "\n".join(f"- [{t['priority'].upper()}] {t['title']}" for t in pending) or "None"
        completed_lines = "\n".join(f"- {t['title']}" for t in completed) or "None"

        report = f"""
# Daily Standup — {report_date}

## Pending Tasks ({len(pending)})
{pending_lines}

## Completed Tasks ({len(completed)})
{completed_lines}

Please format this as a standup update: Yesterday | Today | Blockers.
Keep it concise (3-5 bullet points).
""".strip()
        return [PromptMessage(role="user", content=TextContent(type="text", text=report))]

    elif name == "task_analysis":
        task_id = int(args.get("task_id", 0))
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)
        if not task:
            return [PromptMessage(
                role="user",
                content=TextContent(type="text", text=f"Task #{task_id} not found.")
            )]

        prompt_text = f"""
Analyse this task and provide actionable recommendations:

Task: {task['title']}
Priority: {task['priority']}
Status: {task['status']}
Due Date: {task.get('due_date', 'Not set')}
Created: {task['created_at']}

1. Is this priority appropriate?
2. What are likely sub-tasks or blockers?
3. Suggest a time estimate.
""".strip()
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text))]

    raise ValueError(f"Unknown prompt: {name}")

# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

Save (`Ctrl + S`). Your folder:
```
ex5-complete-server/
├── venv/
└── complete_server.py   ← just created ✓
```

---

### Step 4: Verify the server starts

Switch to PowerShell:

```powershell
python complete_server.py
```

Should hang — press `Ctrl + C`. No errors means it's working.

---

### Step 5: Create `test_complete.py` and run it

In **VS Code**: `Ctrl + N`, save as **`test_complete.py`** at the root of `ex5-complete-server`. Paste:

```python
"""
test_complete.py
================
Tests tools, resources, and prompts of complete_server.py.
Run: python test_complete.py
"""
import subprocess, json, sys, os

def send(proc, method, params=None, _id=[1]):
    req = {"jsonrpc": "2.0", "id": _id[0], "method": method, "params": params or {}}
    _id[0] += 1
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())

def test():
    if os.path.exists("demo_data.json"):
        os.remove("demo_data.json")

    print("Starting complete_server.py...")
    proc = subprocess.Popen(
        [sys.executable, "complete_server.py"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    send(proc, "initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}})

    # --- Tools ---
    r = send(proc, "tools/list")
    tool_names = [t["name"] for t in r["result"]["tools"]]
    assert set(tool_names) == {"add_task", "list_tasks", "complete_task", "get_statistics"}
    print(f"✅ Tools: {tool_names}")

    def tool(name, args):
        return send(proc, "tools/call", {"name": name, "arguments": args})["result"]["content"][0]["text"]

    t1 = tool("add_task", {"title": "Design database schema", "priority": "high"})
    assert "Task #1" in t1
    print(f"✅ {t1}")

    tool("add_task", {"title": "Write API docs", "priority": "low"})
    stats = tool("get_statistics", {})
    assert "Total: 2" in stats
    print(f"✅ statistics: Total=2")

    tool("complete_task", {"task_id": 1})
    stats2 = tool("get_statistics", {})
    assert "Completed: 1" in stats2
    print(f"✅ statistics after complete: Completed=1")

    # --- Resources ---
    r = send(proc, "resources/list")
    uris = [res["uri"] for res in r["result"]["resources"]]
    assert "tasks://all" in uris and "tasks://statistics" in uris
    print(f"✅ Resources: {uris}")

    r = send(proc, "resources/read", {"uri": "tasks://all"})
    tasks_json = json.loads(r["result"]["contents"][0]["text"])
    assert len(tasks_json) == 2
    print(f"✅ resources/read tasks://all returned {len(tasks_json)} tasks")

    # --- Prompts ---
    r = send(proc, "prompts/list")
    prompt_names = [p["name"] for p in r["result"]["prompts"]]
    assert "daily_standup" in prompt_names and "task_analysis" in prompt_names
    print(f"✅ Prompts: {prompt_names}")

    r = send(proc, "prompts/get", {"name": "daily_standup", "arguments": {}})
    msg_text = r["result"]["messages"][0]["content"]["text"]
    assert "Daily Standup" in msg_text
    print(f"✅ daily_standup prompt returned structured text")

    r = send(proc, "prompts/get", {"name": "task_analysis", "arguments": {"task_id": "1"}})
    msg_text = r["result"]["messages"][0]["content"]["text"]
    assert "Design database schema" in msg_text
    print(f"✅ task_analysis prompt returned task details")

    proc.terminate()
    print("\n🎉 Complete server tests passed — tools, resources, AND prompts all work!")

if __name__ == "__main__":
    test()
```

Save (`Ctrl + S`). Switch to PowerShell:

```powershell
python test_complete.py
```

**Expected output:**
```
Starting complete_server.py...
✅ Tools: ['add_task', 'list_tasks', 'complete_task', 'get_statistics']
✅ Task #1 created: Design database schema
✅ statistics: Total=2
✅ statistics after complete: Completed=1
✅ Resources: ['tasks://all', 'tasks://statistics']
✅ resources/read tasks://all returned 2 tasks
✅ Prompts: ['daily_standup', 'task_analysis']
✅ daily_standup prompt returned structured text
✅ task_analysis prompt returned task details

🎉 Complete server tests passed — tools, resources, AND prompts all work!
```

---

### ✅ Checkpoint 3.1

- [ ] `complete_server.py` is saved at the root of `ex5-complete-server/`
- [ ] `python test_complete.py` shows all nine ✅ lines
- [ ] `demo_data.json` was created automatically
- [ ] You understand the three MCP building blocks: **tools** (actions), **resources** (read-only data), **prompts** (templates)

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

**Goal**: Create an MCP server that integrates with a real external HTTP API (OpenWeatherMap).

**Estimated time**: 25 minutes

---

### Step 1: Get a free API key

1. Open your browser and go to [openweathermap.org/api](https://openweathermap.org/api).
2. Click **Sign In** → **Create an Account** (it's free).
3. After signing in, click your username in the top-right → **My API Keys**.
4. Copy the **Default** key (it looks like `abc123def456...`).
5. Keep this key — you'll need it in Step 4 below.

> **Note**: New API keys can take up to 10 minutes to activate. If you get a `401` error, wait a few minutes and retry.

---

### Step 2: Create the project folder

Switch to PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab"
mkdir ex6-weather
cd ex6-weather

python -m venv venv
.\venv\Scripts\Activate
pip install mcp httpx
```

Expected last lines:
```
Successfully installed mcp-1.x.x httpx-0.x.x ...
```

---

### Step 3: Open the folder in VS Code

```powershell
code .
```

VS Code opens with `ex6-weather` as the workspace root. Confirm the title bar shows `ex6-weather`.

---

### Step 4: Set your API key as an environment variable

> **Do this in PowerShell before running any server commands.**
> Environment variables set this way last only for the current PowerShell session.

```powershell
$env:OPENWEATHER_API_KEY = "PASTE_YOUR_KEY_HERE"
```

Replace `PASTE_YOUR_KEY_HERE` with the key you copied in Step 1. Verify it's set:

```powershell
echo $env:OPENWEATHER_API_KEY
```

You should see your key printed back.

---

### Step 5: Create `weather_server.py`

In VS Code: `Ctrl + N`, save as **`weather_server.py`** at the root of `ex6-weather` (NOT inside `venv`).

```python
"""
Exercise 4.1: Weather API MCP Server
====================================
Integrates with OpenWeatherMap API.
Set your API key: $env:OPENWEATHER_API_KEY = "your-key-here"
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
🌍 Weather in {data['name']}, {data['sys']['country']}

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
                
                forecast = f"📅 5-Day Forecast for {data['city']['name']}\n\n"
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

Save with `Ctrl + S`. Folder structure:
```
ex6-weather/
├── venv/
└── weather_server.py   ← just created ✓
```

---

### Step 6: Verify the server starts

```powershell
python weather_server.py
```

Should hang — press `Ctrl + C`. No errors means the imports work.

---

### Step 7: Create `test_weather.py` and run it

In **VS Code**: `Ctrl + N`, save as **`test_weather.py`** in `ex6-weather`. Paste:

```python
"""
test_weather.py
===============
Tests the weather server against the live OpenWeatherMap API.
Requires: $env:OPENWEATHER_API_KEY to be set.
Run: python test_weather.py
"""
import subprocess, json, sys, os

def send(proc, method, params=None, _id=[1]):
    req = {"jsonrpc": "2.0", "id": _id[0], "method": method, "params": params or {}}
    _id[0] += 1
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())

def test_weather():
    if not os.environ.get("OPENWEATHER_API_KEY"):
        print("❌ OPENWEATHER_API_KEY not set. Run: $env:OPENWEATHER_API_KEY = 'your-key'")
        return

    print("Starting weather_server.py...")
    proc = subprocess.Popen(
        [sys.executable, "weather_server.py"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        env=os.environ.copy()   # pass through environment variables including the API key
    )

    send(proc, "initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}})

    # Check tools exist
    r = send(proc, "tools/list")
    names = [t["name"] for t in r["result"]["tools"]]
    print(f"✅ Tools available: {names}")

    # Call get_weather for London
    r = send(proc, "tools/call", {"name": "get_weather", "arguments": {"city": "London", "units": "metric"}})
    text = r["result"]["content"][0]["text"]
    print(f"✅ get_weather(London):\n{text}")

    # Check response contains expected fields
    assert "Temperature" in text or "Error" in text, "Unexpected response format"
    if "Error" in text:
        print("   ⚠️  API returned an error — check your key and wait a moment if it's new.")
    else:
        print("✅ Weather data received successfully!")

    proc.terminate()
    print("\n🎉 Weather server test complete!")

if __name__ == "__main__":
    test_weather()
```

Save (`Ctrl + S`). Switch to PowerShell (make sure `OPENWEATHER_API_KEY` is still set):

```powershell
python test_weather.py
```

**Expected output** (actual temperatures will differ):
```
Starting weather_server.py...
✅ Tools available: ['get_weather', 'get_forecast']
✅ get_weather(London):
🌍 Weather in London, GB

🌡️ Temperature: 12.3°C
🤒 Feels like: 10.1°C
💧 Humidity: 75%
🌤️ Conditions: Light Rain
💨 Wind: 4.1 m/s
✅ Weather data received successfully!

🎉 Weather server test complete!
```

---

### ✅ Checkpoint 4.1

- [ ] `weather_server.py` is saved at the root of `ex6-weather/`
- [ ] `$env:OPENWEATHER_API_KEY` is set in PowerShell
- [ ] `python test_weather.py` shows weather data for London
- [ ] You understand: API key is read from environment (`os.environ.get(...)`) — never hard-coded in source code

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

**Estimated time**: 20 minutes

---

### Step 1: Create the project folder

In PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab"
mkdir ex7-cloud-server
cd ex7-cloud-server

python -m venv venv
.\venv\Scripts\Activate
```

### Step 2: Install extra dependencies

```powershell
pip install "mcp[sse]" uvicorn starlette
```

Expected last lines:
```
Successfully installed mcp-1.x.x uvicorn-0.x.x starlette-0.x.x ...
```

### Step 3: Open the folder in VS Code

```powershell
code .
```

VS Code opens. Confirm the title bar shows `ex7-cloud-server`.

### Step 4: Create `cloud_server.py`

In VS Code: `Ctrl + N`, save as **`cloud_server.py`** at the root of `ex7-cloud-server` (same level as `venv/`). Paste:

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

async def root_redirect(request):
    """Redirect root to /sse so VS Code's streamable-HTTP probe gets a useful response."""
    from starlette.responses import RedirectResponse
    return RedirectResponse(url="/sse")

starlette_app = Starlette(
    routes=[
        Route("/",        root_redirect),
        Route("/health",  health),
        Route("/sse",     handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
```

Save (`Ctrl + S`). Folder structure:
```
ex7-cloud-server/
├── venv/
└── cloud_server.py   ← just created ✓
```

### Step 5: Start the server and verify it responds

Switch to PowerShell and run:

```powershell
python cloud_server.py
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

> **Leave this running**. Open a **second PowerShell window** (right-click the taskbar → "Windows Terminal") for the next commands.

In the second PowerShell window, test the health endpoint:

```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "server": "task-manager-cloud"}
```

Also confirm the SSE endpoint exists:

```powershell
curl -I http://localhost:8000/sse
```

Expected: HTTP `200` response (it will hang waiting for an SSE connection — press `Ctrl + C` after seeing the headers).

Press `Ctrl + C` in the **first** PowerShell window to stop the server when done.

### ✅ Checkpoint 7.1
- [ ] `cloud_server.py` is saved at the root of `ex7-cloud-server/`
- [ ] `python cloud_server.py` shows the `Uvicorn running on http://0.0.0.0:8000` line
- [ ] `curl http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] `/sse` endpoint is reachable (returns HTTP 200)

---

## Exercise 7.2: Containerize with Docker

**Goal**: Package your `cloud_server.py` into a Docker image so it runs identically anywhere.

**Estimated time**: 15 minutes

**Prerequisite**: Docker Desktop must be installed and running. Check with:
```powershell
docker --version
```
Expected: `Docker version 24.x.x ...`  
If missing, download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).

---

> **All files below go in the same `ex7-cloud-server` folder as `cloud_server.py`.**

---

### Step 1: Open `ex7-cloud-server` in VS Code

If VS Code is not already open on `ex7-cloud-server`:
```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab\ex7-cloud-server"
code .
```

---

### Step 2: Create `requirements.txt`

In VS Code: `Ctrl + N`, save as **`requirements.txt`** at the root of `ex7-cloud-server`. Paste:

```
mcp[sse]>=1.0.0
uvicorn>=0.30.0
starlette>=0.37.0
```

Save (`Ctrl + S`).

---

### Step 3: Create `Dockerfile`

In VS Code: `Ctrl + N`, save as **`Dockerfile`** (no extension) at the root of `ex7-cloud-server`. Paste:

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

Save (`Ctrl + S`).

Your folder now:
```
ex7-cloud-server/
├── venv/
├── cloud_server.py
├── requirements.txt   ← just created ✓
└── Dockerfile         ← just created ✓
```

---

### Step 4: Build the Docker image

Switch to PowerShell (make sure you're in `ex7-cloud-server`):

```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab\ex7-cloud-server"
docker build -t mcp-task-manager .
```

You will see Docker pulling the base image and installing packages. The final lines should be:
```
...
Successfully built abc123def456
Successfully tagged mcp-task-manager:latest
```

The build takes ~1–2 minutes the first time (downloading `python:3.11-slim`). Subsequent builds are much faster.

---

### Step 5: Run the container and verify

```powershell
# Create a data folder for persistent storage
mkdir data -ErrorAction SilentlyContinue

# Run the container, mounting the data folder as a volume
docker run -d -p 8000:8000 -v "${PWD}/data:/app/data" --name mcp-server mcp-task-manager
```

Check it's running:

```powershell
docker ps
```

Expected output includes a row like:
```
CONTAINER ID   IMAGE              COMMAND                  ...   PORTS
abc123...      mcp-task-manager   "python cloud_server…"   ...   0.0.0.0:8000->8000/tcp
```

Test the health endpoint:

```powershell
curl http://localhost:8000/health
```

Expected: `{"status": "ok", "server": "task-manager-cloud"}`

---

### Step 6: Confirm data persists across restarts

```powershell
# Stop the container
docker stop mcp-server

# Remove it
docker rm mcp-server

# Start a fresh container (pointing at same data volume)
docker run -d -p 8000:8000 -v "${PWD}/data:/app/data" --name mcp-server mcp-task-manager

# Health check again
curl http://localhost:8000/health
```

The `tasks.json` inside `./data/` survived the container restart.

Clean up when done:
```powershell
docker stop mcp-server
docker rm mcp-server
```

### ✅ Checkpoint 7.2
- [ ] `Dockerfile` and `requirements.txt` are in `ex7-cloud-server/`
- [ ] `docker build -t mcp-task-manager .` completes without errors
- [ ] `docker run` starts the container and it's visible in `docker ps`
- [ ] `curl http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] Data in `./data/` persists after container restart

---

## Exercise 7.3: Deploy to Azure Container Apps

**Goal**: Push the container to Azure and get a public HTTPS endpoint in ~5 minutes.

**Estimated time**: 20 minutes

---

### Prerequisites: Install and verify Azure CLI

Open a **fresh** PowerShell window and run:

```powershell
az --version
```

If you see `az: command not found` or nothing:
```powershell
# Install Azure CLI via winget
winget install Microsoft.AzureCLI
```

After installation, close and reopen PowerShell, then verify again:
```powershell
az --version
# Expected: azure-cli  2.x.x ...
```

Log in to your Azure account:
```powershell
az login
```

A browser window opens — sign in with your Microsoft or Azure account. When login completes, the terminal shows your subscription details.

Install the Container Apps extension:
```powershell
az extension add --name containerapp --upgrade
```

Expected last line: `Extension 'containerapp' ... is now installed.`

---

### Step 1: Set variables

In PowerShell, still in `ex7-cloud-server`:

```powershell
cd "$env:USERPROFILE\Desktop\mcp-lab\ex7-cloud-server"

# These variable names are used throughout the remaining steps
$RESOURCE_GROUP = "rg-mcp-demo"
$LOCATION       = "eastus"
$ACR_NAME       = "acrmcpdemo$(Get-Random -Maximum 9999)"   # must be globally unique
$APP_NAME       = "mcp-task-manager"
$ENV_NAME       = "mcp-env"

# Confirm they're set
Write-Host "Resource group : $RESOURCE_GROUP"
Write-Host "ACR name       : $ACR_NAME"
```

---

### Step 2: Create Azure resources

```powershell
# Create a resource group (a logical container for all resources)
az group create --name $RESOURCE_GROUP --location $LOCATION
```

Expected output includes `"provisioningState": "Succeeded"`.

```powershell
# Create a private Docker registry (Azure Container Registry)
az acr create `
  --resource-group $RESOURCE_GROUP `
  --name $ACR_NAME `
  --sku Basic `
  --admin-enabled true
```

The command takes ~30 seconds. When it finishes you'll see a JSON block containing `"provisioningState": "Succeeded"`.

---

### Step 3: Push your image to ACR

```powershell
# Build the image inside Azure and push it to ACR
# (This does NOT require Docker Desktop to be running locally)
az acr build `
  --registry $ACR_NAME `
  --image mcp-task-manager:latest .
```

Watch the build log stream in your terminal. The last line should be:
```
Run ID: ... was successful after Xs
```

Get the registry credentials:
```powershell
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
$ACR_SERVER   = "$ACR_NAME.azurecr.io"
Write-Host "Registry: $ACR_SERVER"
```

---

### Step 4: Create Container Apps environment and deploy

```powershell
# Create the Container Apps environment (networking layer)
az containerapp env create `
  --name $ENV_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION
```

Takes ~2 minutes. Wait for `"provisioningState": "Succeeded"`.

```powershell
# Deploy the container
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
```

Takes ~1 minute. When done, get the public URL:

```powershell
$APP_URL = az containerapp show `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "✅ MCP Server deployed at: https://$APP_URL"
```

---

### Step 5: Verify deployment

```powershell
# Health check — should return {"status": "ok", "server": "task-manager-cloud"}
curl "https://$APP_URL/health"
```

Expected:
```json
{"status": "ok", "server": "task-manager-cloud"}
```

View live logs (useful if health check fails):
```powershell
az containerapp logs show `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --follow
```

Press `Ctrl + C` to stop following logs.

---

### Step 6: Connect VS Code to your deployed server

Switch to **VS Code**. Open (or create) `.vscode/settings.json` and add:

```json
{
    "mcp": {
        "servers": {
            "task-manager-cloud": {
                "type": "sse",
                "url": "https://<YOUR_APP_URL>/sse"
            }
        }
    }
}
```

Replace `<YOUR_APP_URL>` with the FQDN printed in Step 4 (e.g. `mcp-task-manager.nicefield-abc123.eastus.azurecontainerapps.io`).

> **Critical**: You must include **both** `"type": "sse"` and the `/sse` path in the URL.
> - `"type": "sse"` forces VS Code to use the legacy SSE transport directly instead of first probing for the newer streamable-HTTP transport at the root `/`. Without it, VS Code POSTs to `https://<APP_URL>/` first, gets a 404, and the connection fails.
> - The URL must end with `/sse` — using the bare domain without the path also causes a 404.

**Your exact entry** (replace the domain with your own):
```json
"url": "https://mcp-task-manager.agreeablepebble-67b5e2eb.eastus.azurecontainerapps.io/sse"
```

Reload VS Code (`Ctrl + Shift + P` → `Developer: Reload Window`), then open Copilot Chat and try:

```
Add a task: deploy monitoring dashboard
```

Copilot should call your *deployed Azure* MCP server!

---

### ✅ Checkpoint 7.3
- [ ] Image pushed to ACR (`az acr build` succeeded)
- [ ] Container App shows `Running` state (`az containerapp show`)
- [ ] `curl https://<APP_URL>/health` returns `{"status":"ok"}`
- [ ] VS Code Copilot calls tools on the deployed server

### 🧹 Cleanup (optional)

```powershell
# Remove all resources (stops billing)
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

**Goal**: Expose `task_review` and `task_standup` prompts from `cloud_server.py`.

**Estimated time**: 15 minutes

---

### Step 1: Open `cloud_server.py` in VS Code

In VS Code, confirm you have `ex7-cloud-server` as the workspace (title bar). Click **`cloud_server.py`** in the Explorer panel to open it.

---

### Step 2: Add the prompt imports at the top of the file

Find the line that reads:
```python
from mcp.types import Tool, TextContent
```

Replace it with:
```python
from mcp.types import Tool, TextContent, Prompt, PromptArgument, PromptMessage
```

Save with `Ctrl + S`.

---

### Step 3: Add the prompt handlers

Scroll to the very end of `cloud_server.py`, just **before** the `# ── SSE transport wiring ──` comment block. Add the following two functions:

```python
# ── Prompts ───────────────────────────────────────────────────────────────────

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
""".strip()
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text))]

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
""".strip()
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text))]

    raise ValueError(f"Unknown prompt: {name}")
```

Save (`Ctrl + S`).

---

### Step 4: Verify the server still starts

Switch to PowerShell (`ex7-cloud-server` folder, `(venv)` active):

```powershell
python cloud_server.py
```

Expected: `Uvicorn running on http://0.0.0.0:8000`. Press `Ctrl + C`.

If you see a `SyntaxError`, re-check that the import line was updated in Step 2.

---

### Step 5: Test the prompts in VS Code

1. Make sure `.vscode/settings.json` in `ex7-cloud-server` has the MCP server registered (from Exercise 2.2 — use `"command": "python"` and `"args": ["${workspaceFolder}/cloud_server.py"]`).
2. Start the server: `python cloud_server.py` (leave it running).
3. Reload VS Code: `Ctrl + Shift + P` → `Developer: Reload Window`.
4. Open Copilot Chat (`Ctrl + Shift + I`) in Agent mode.
5. Type:

```
Run the task_review prompt
```

Copilot should call the prompt and return an analysis of your current task list.

6. Try:

```
Run the task_standup prompt with your_name = "Alice"
```

Copilot should return a formatted standup report.

### ✅ Checkpoint 8.1
- [ ] `cloud_server.py` has the updated `from mcp.types import` line
- [ ] `python cloud_server.py` starts without errors
- [ ] Copilot Chat invokes `task_review` and returns useful output
- [ ] Prompts reference live task data

---

## Exercise 8.2: Create a Reusable VS Code `.prompt.md` Skill

**Goal**: Create a reusable slash-command in VS Code that automatically invokes your MCP tools.  
**What is a `.prompt.md` file?** It is a Markdown file stored under `.github/prompts/` that VS Code reads to create a named `/slash-command` in Copilot Chat. When you type `/manage-tasks`, Copilot loads your prompt text, substitutes `{{input}}`, then calls the MCP tools you listed.

**Working folder**: `ex7-cloud-server` — the same workspace your cloud server lives in.

---

### Step 1: Open the ex7-cloud-server workspace in VS Code

If VS Code is not already open on this workspace, do:

```powershell
# In any PowerShell window
cd C:\Users\akashdwivedi\Desktop\mcp-lab\ex7-cloud-server
code .
```

VS Code title bar should read **ex7-cloud-server**.

---

### Step 2: Create the `.github\prompts` directory

In VS Code, open the **integrated terminal** (`Ctrl + `` ` ``):

```powershell
# Make sure you are in the ex7-cloud-server folder
# The prompt should show:  PS C:\Users\<you>\Desktop\mcp-lab\ex7-cloud-server>

mkdir .github\prompts
```

**Expected output**:

```
    Directory: C:\Users\<you>\Desktop\mcp-lab\ex7-cloud-server\.github

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          <date>          <time>                prompts
```

> **If you see "A subdirectory or file .github already exists"**, that is fine — the `.github` folder was created in an earlier step. Just confirm the `prompts` sub-folder now exists.

After running the command, your folder tree should look like this:

```
ex7-cloud-server\
├── .github\
│   ├── prompts\         ← new folder
│   └── (other files)
├── .vscode\
│   └── settings.json
├── cloud_server.py
├── requirements.txt
├── Dockerfile
└── tasks.json
```

---

### Step 3: Create `manage-tasks.prompt.md` in VS Code

1. In the **Explorer panel** (`Ctrl + Shift + E`), expand `.github` → `prompts`
2. Right-click the `prompts` folder → **New File**
3. Type the filename exactly: `manage-tasks.prompt.md` and press **Enter**

The empty file opens automatically. Paste the full content below (`Ctrl + A` then paste):

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

4. Save with `Ctrl + S`.

**Verify the file exists:**

```powershell
Get-ChildItem .github\prompts
```

Expected output:

```
    Directory: C:\Users\<you>\Desktop\mcp-lab\ex7-cloud-server\.github\prompts

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          <date>          <time>            <size> manage-tasks.prompt.md
```

---

### Step 4: Reload VS Code to register the new slash-command

Press `Ctrl + Shift + P` → type **Developer: Reload Window** → press **Enter**.

Wait ~5 seconds for VS Code to finish loading.

---

### Step 5: Confirm the slash-command appears in Copilot Chat

1. Make sure your MCP server is running (open a new terminal tab, run `python cloud_server.py`)
2. Open Copilot Chat (`Ctrl + Alt + I` or the Copilot icon in the sidebar)
3. In the chat input box type `/` — a drop-down list of available commands appears
4. Look for **`/manage-tasks`** in the list.  
   If it appears, the `.prompt.md` was picked up correctly ✅

> **Not seeing it?** Check:
> - The file is saved as `.github\prompts\manage-tasks.prompt.md` (exactly this path)
> - The frontmatter block starts on line 1 with `---` (no blank line before it)
> - Try **Developer: Reload Window** once more

---

### Step 6: Use the slash-command

In Copilot Chat, type:

```
/manage-tasks Add three tasks: write tests, update README, deploy to staging
```

**What Copilot should do** (step by step):
1. Load the `manage-tasks.prompt.md` text and substitute `{{input}}`
2. Call `list_tasks` (because the prompt's rules say "always check first")
3. Call `add_task` three times, once for each item
4. Report back: *"Added task #1 (write tests), task #2 (update README), task #3 (deploy to staging)"*

**Another test — view and complete a task:**

```
/manage-tasks Show all tasks, then mark task #1 as done
```

Expected flow: Copilot calls `list_tasks`, shows the list, asks you to confirm, then calls `complete_task` with `task_id=1`.

---

### ✅ Checkpoint 8.2
- [ ] `.github\prompts\manage-tasks.prompt.md` exists
- [ ] `/manage-tasks` appears in the Copilot Chat slash-command list
- [ ] Copilot invokes the prompt and calls `add_task` / `list_tasks` / `complete_task` via MCP
- [ ] `tasks.json` shows the new tasks added during the test

---

## Exercise 8.3: Create a VS Code `.instructions.md` to Always Load MCP Context

**Goal**: Create an always-on instruction file so Copilot automatically understands your MCP server without you repeating yourself every session.  
**What is a `.instructions.md` file?** A Markdown file stored under `.github/instructions/` with `applyTo` frontmatter that VS Code injects into every Copilot Chat context automatically. When `applyTo: "**"` is set, Copilot reads the file before answering any question in this workspace — so it already knows your MCP tools without you explaining them.

**Working folder**: `ex7-cloud-server` — the same workspace as your cloud server.

---

### Step 1: Confirm VS Code is open in ex7-cloud-server

Check the title bar reads **ex7-cloud-server**. If not:

```powershell
cd C:\Users\akashdwivedi\Desktop\mcp-lab\ex7-cloud-server
code .
```

---

### Step 2: Create the `.github\instructions` directory

In the VS Code integrated terminal (`Ctrl + `` ` ``):

```powershell
mkdir .github\instructions
```

**Expected output**:

```
    Directory: C:\Users\<you>\Desktop\mcp-lab\ex7-cloud-server\.github

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          <date>          <time>                instructions
```

> **If you already created `.github\prompts` in Exercise 8.2**, you see the `.github` folder already exists — that is fine. Just confirm `instructions` was created inside it.

Your folder tree should now look like this:

```
ex7-cloud-server\
├── .github\
│   ├── prompts\
│   │   └── manage-tasks.prompt.md
│   └── instructions\       ← new folder
├── .vscode\
│   └── settings.json
├── cloud_server.py
├── requirements.txt
├── Dockerfile
└── tasks.json
```

---

### Step 3: Create the instructions file in VS Code

1. In the **Explorer panel** (`Ctrl + Shift + E`) expand `.github` → `instructions`
2. Right-click the `instructions` folder → **New File**
3. Type the filename exactly: `mcp-task-manager.instructions.md` and press **Enter**

The empty file opens. Paste the full content below (`Ctrl + A` then paste):

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

4. Save with `Ctrl + S`.

**Verify the file was saved correctly:**

```powershell
Get-ChildItem .github\instructions
```

Expected output:

```
    Directory: C:\Users\<you>\Desktop\mcp-lab\ex7-cloud-server\.github\instructions

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          <date>          <time>            <size> mcp-task-manager.instructions.md
```

---

### Step 4: Reload VS Code so Copilot picks up the new file

Press `Ctrl + Shift + P` → type **Developer: Reload Window** → press **Enter**.

Wait ~5 seconds for VS Code to finish loading.

---

### Step 5: Confirm Copilot can see the instruction context

1. Make sure `python cloud_server.py` is running (start it in a terminal tab if not)
2. Open Copilot Chat (`Ctrl + Alt + I`)
3. Click the **context** icon (paperclip or `#` button) near the Copilot Chat input — you should see `mcp-task-manager.instructions.md` listed as an active context source

> **Alternatively**: look for a small document icon in the Copilot pane header that lists loaded instruction files.

---

### Step 6: Test that Copilot uses the context automatically

Without typing any setup or explanation, ask Copilot:

```
What MCP tools do I have available and what are their required parameters?
```

**Expected**: Copilot answers directly from the table you defined, e.g.:

```
You have 3 MCP tools available:
- add_task (required: title)
- list_tasks (no params)
- complete_task (required: task_id)
```

It should NOT say "I don't know what tools you have" — the instructions file provides that context automatically.

**Second test — no-schema question:**

```
Add a high-priority task called "Deploy to prod"
```

Copilot should call `add_task` with `title="Deploy to prod"` and `priority="high"` without asking what parameters the tool needs.

**What to expect if it works correctly:**

```
✅ Called add_task(title="Deploy to prod", priority="high")
   → Task #4 created.
```

---

### Step 7: Understand what you just built

| Mechanism | File location | When it activates | Best for |
|-----------|--------------|-------------------|----------|
| MCP Prompt | Server (`cloud_server.py`) | User calls it explicitly | Data-aware AI workflows |
| `.prompt.md` | `.github/prompts/` | User types `/slash-command` | Repeatable agent tasks |
| `.instructions.md` | `.github/instructions/` | Every Copilot session | Always-on context & conventions |

All three work together in your workspace right now.

---

### ✅ Checkpoint 8.3
- [ ] `.github\instructions\mcp-task-manager.instructions.md` file exists
- [ ] File has `applyTo: "**"` in the frontmatter
- [ ] After **Developer: Reload Window**, Copilot answers tool questions without setup
- [ ] `add_task` called with correct params without Copilot asking for the schema
- [ ] `tasks.json` contains the task added during the test

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
