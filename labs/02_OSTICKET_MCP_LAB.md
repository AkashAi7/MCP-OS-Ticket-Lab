# Lab 2: Building an MCP Server for osTicket

> **From Helpdesk Platform to AI-Powered Ticketing** - A Complete Hands-On Journey

---

## 🎯 Learning Objectives

By completing this lab, you will be able to:
- Set up and run osTicket locally using Docker
- Understand osTicket's architecture and API
- Design MCP tools for a real-world application
- Build a production-ready MCP server for osTicket
- Test and debug MCP integrations
- Extend the MCP server with custom features

---

## 📋 Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Docker Desktop | Latest | `docker --version` |
| Python | 3.10+ | `python --version` |
| VS Code | Latest | `code --version` |
| Completed Lab 1 | - | MCP Fundamentals |

---

# Part A: Getting Started with osTicket

## Module A.1: Understanding osTicket

### What is osTicket?

**osTicket** is a widely-used open-source support ticket system. It seamlessly integrates customer inquiries via email, phone, and web forms into a simple, easy-to-use multi-user web interface.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        osTicket System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Web Portal  │    │  Staff Panel │    │  Admin Panel │      │
│  │  (Customers) │    │   (Agents)   │    │  (Settings)  │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                    │                   │               │
│         └────────────┬───────┴───────────────────┘               │
│                      │                                           │
│              ┌───────▼───────┐                                   │
│              │   PHP Core    │                                   │
│              │   (Backend)   │                                   │
│              └───────┬───────┘                                   │
│                      │                                           │
│              ┌───────▼───────┐                                   │
│              │    MySQL      │                                   │
│              │   Database    │                                   │
│              └───────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Entities

| Entity | Description | Database Table |
|--------|-------------|----------------|
| **Ticket** | Support request from customer | `ost_ticket` |
| **User** | Customer who submits tickets | `ost_user` |
| **Staff** | Agent who handles tickets | `ost_staff` |
| **Department** | Organizational unit | `ost_department` |
| **Topic** | Help topic category | `ost_help_topic` |
| **Thread** | Ticket conversation thread | `ost_thread` |
| **Thread Entry** | Individual message in thread | `ost_thread_entry` |

---

## Exercise A.1: Setting Up osTicket Locally

**Goal**: Get osTicket running in Docker with one click.

### Step 1: Clone the Repository

```powershell
# Clone the osTicket repository with MCP setup
git clone https://github.com/your-repo/osTicket.git
cd osTicket
```

### Step 2: Run the Installation Script

```powershell
# Windows - One-click install
.\install-local.cmd

# Or using PowerShell directly
powershell -ExecutionPolicy Bypass -File .\install-local.ps1
```

### Step 3: Wait for Installation

The script will:
1. Start Docker containers (osTicket, MySQL, phpMyAdmin)
2. Wait for MySQL to be ready
3. Run the osTicket installer
4. Configure admin credentials

### Step 4: Verify Installation

Open your browser and visit:

| URL | Purpose | Credentials |
|-----|---------|-------------|
| http://localhost:8080 | Customer Portal | (Create account) |
| http://localhost:8080/scp | Staff Panel | `ostadmin` / `ChangeMe123!` |
| http://localhost:8081 | phpMyAdmin | `root` / `rootpassword` |

### ✅ Checkpoint A.1
- [ ] Docker containers running (`docker ps`)
- [ ] Customer portal loads at localhost:8080
- [ ] Staff panel login works
- [ ] phpMyAdmin shows database tables

---

## Exercise A.2: Exploring osTicket

**Goal**: Understand osTicket by using it.

### Task 1: Create a Test Ticket

1. Go to http://localhost:8080
2. Click "Open a New Ticket"
3. Fill in the form:
   - Email: `test@example.com`
   - Name: `Test User`
   - Help Topic: Select any
   - Subject: `Test Ticket - Learning osTicket`
   - Message: `This is a test ticket for the MCP lab.`
4. Submit the ticket
5. Note the ticket number

### Task 2: Process the Ticket as Staff

1. Go to http://localhost:8080/scp
2. Login as `ostadmin` / `ChangeMe123!`
3. Find your ticket in the queue
4. Click to open it
5. Add an internal note
6. Send a reply to the customer
7. Change the ticket status

### Task 3: Explore the Database

1. Go to http://localhost:8081 (phpMyAdmin)
2. Login as `root` / `rootpassword`
3. Select the `osticket` database
4. Browse these tables:
   - `ost_ticket` - See your ticket
   - `ost_user` - See the test user
   - `ost_thread` - See the conversation thread
   - `ost_thread_entry` - See individual messages

### 🏆 Challenge A.2
Create a simple diagram showing the relationship between:
- A ticket
- Its thread
- Thread entries
- The user who created it

<details>
<summary>💡 View Answer</summary>

```
ost_user (1) ──────────────────┐
     │                         │
     │ user_id                 │ user_id
     ▼                         ▼
ost_ticket (1) ──────────► ost_thread (1)
     │                         │
     │ ticket_id               │ id → object_id
     │                         ▼
     │                    ost_thread_entry (N)
     │                         │
     └─────────────────────────┘
```

</details>

---

## Exercise A.3: Understanding osTicket's API

**Goal**: Learn how to interact with osTicket programmatically.

### osTicket API Overview

osTicket provides a REST-like API for ticket operations.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/tickets.json` | POST | Create ticket |
| `/api/tickets/{id}` | GET | Get ticket details |
| `/api/tickets.email` | POST | Create ticket via email |

### API Authentication

osTicket uses API keys for authentication:

1. Go to Admin Panel → Manage → API Keys
2. Click "Add New API Key"
3. Configure:
   - IP Address: `127.0.0.1` or your Docker network
   - Status: Active
   - Enable "Can Create Tickets"

### Making API Requests

```python
import requests

API_URL = "http://localhost:8080/api/tickets.json"
API_KEY = "YOUR_API_KEY_HERE"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Create a ticket
ticket_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "API Test Ticket",
    "message": "This ticket was created via the API.",
    "topicId": 1  # Default help topic
}

response = requests.post(API_URL, json=ticket_data, headers=headers)
print(response.json())
```

### Limitations of the Default API

The default osTicket API is limited:
- ❌ Cannot fetch ticket details (read)
- ❌ Cannot reply to tickets
- ❌ Cannot update ticket status
- ❌ Cannot manage users programmatically

**This is why we build an MCP server with helper scripts!**

---

# Part B: Building the MCP Server

## Module B.1: Design Phase

### Identifying Use Cases

What should our MCP server enable?

| Use Case | Tool Needed | Priority |
|----------|-------------|----------|
| Create support ticket | `create_ticket` | High |
| Get ticket details | `get_ticket` | High |
| Reply to ticket | `reply_to_ticket` | High |
| Create/find user | `create_user` | Medium |
| Get system status | `get_osticket_status` | Medium |
| List all tickets | `list_tickets` | Medium |
| Search tickets | `search_tickets` | Low |
| Update ticket status | `update_ticket` | Low |

### Architecture Decision

Since osTicket's API is limited, we'll use **PHP helper scripts** that run inside the Docker container:

```
┌─────────────────┐     stdio     ┌──────────────────┐
│   VS Code       │ ◄───────────► │   MCP Server     │
│   Copilot       │               │   (Python)       │
└─────────────────┘               └────────┬─────────┘
                                           │
                                           │ docker exec
                                           ▼
                                  ┌──────────────────┐
                                  │   PHP Helper     │
                                  │   Scripts        │
                                  │   (in container) │
                                  └────────┬─────────┘
                                           │
                                           │ Direct DB
                                           ▼
                                  ┌──────────────────┐
                                  │     MySQL        │
                                  │   osTicket DB    │
                                  └──────────────────┘
```

---

## Exercise B.1: Creating PHP Helper Scripts

**Goal**: Build PHP scripts that interact with osTicket directly.

### Step 1: Create the MCP Helper Script

Create `mcp_create_ticket.php`:

```php
<?php
/**
 * MCP Helper: Create Ticket
 * 
 * Usage: php mcp_create_ticket.php <json_payload>
 */

error_reporting(0);

// Bootstrap osTicket
define('ROOT_DIR', '/var/www/html/');
require_once ROOT_DIR . 'main.inc.php';
require_once INCLUDE_DIR . 'class.ticket.php';
require_once INCLUDE_DIR . 'class.user.php';
require_once INCLUDE_DIR . 'class.client.php';

// Get input from command line
$json_input = $argv[1] ?? '{}';
$data = json_decode($json_input, true);

if (!$data) {
    echo json_encode(['error' => 'Invalid JSON input']);
    exit(1);
}

// Required fields
$name = $data['name'] ?? '';
$email = $data['email'] ?? '';
$subject = $data['subject'] ?? '';
$message = $data['message'] ?? '';
$topic_id = $data['topic_id'] ?? 1;
$priority = $data['priority'] ?? 2;

// Validate
if (!$email || !$subject || !$message) {
    echo json_encode(['error' => 'Missing required fields: email, subject, message']);
    exit(1);
}

try {
    // Find or create user
    $user = User::lookupByEmail($email);
    if (!$user) {
        $user = User::create([
            'name' => $name ?: explode('@', $email)[0],
            'email' => $email
        ]);
    }
    
    // Create ticket
    $ticket = Ticket::create([
        'topicId' => $topic_id,
        'userId' => $user->getId(),
        'name' => $name,
        'email' => $email,
        'subject' => $subject,
        'message' => $message,
        'source' => 'API',
        'ip' => '127.0.0.1',
        'autorespond' => false,
        'alertstaff' => false
    ]);
    
    if ($ticket) {
        echo json_encode([
            'success' => true,
            'ticket_id' => $ticket->getId(),
            'ticket_number' => $ticket->getNumber(),
            'subject' => $ticket->getSubject(),
            'user_id' => $user->getId()
        ]);
    } else {
        echo json_encode(['error' => 'Failed to create ticket']);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
```

### Step 2: Create Get Ticket Helper

Create `mcp_get_ticket.php`:

```php
<?php
/**
 * MCP Helper: Get Ticket Details
 * 
 * Usage: php mcp_get_ticket.php <ticket_number>
 */

error_reporting(0);

define('ROOT_DIR', '/var/www/html/');
require_once ROOT_DIR . 'main.inc.php';
require_once INCLUDE_DIR . 'class.ticket.php';

$ticket_number = $argv[1] ?? '';

if (!$ticket_number) {
    echo json_encode(['error' => 'Ticket number required']);
    exit(1);
}

try {
    $ticket = Ticket::lookupByNumber($ticket_number);
    
    if (!$ticket) {
        echo json_encode(['error' => 'Ticket not found']);
        exit(1);
    }
    
    // Get thread entries
    $thread = $ticket->getThread();
    $entries = [];
    
    if ($thread) {
        foreach ($thread->getEntries() as $entry) {
            $entries[] = [
                'type' => $entry->getType(),
                'poster' => $entry->getPoster(),
                'body' => strip_tags($entry->getBody()->getClean()),
                'created' => $entry->getCreateDate()
            ];
        }
    }
    
    echo json_encode([
        'success' => true,
        'ticket' => [
            'id' => $ticket->getId(),
            'number' => $ticket->getNumber(),
            'subject' => $ticket->getSubject(),
            'status' => $ticket->getStatus()->getName(),
            'priority' => $ticket->getPriority(),
            'department' => $ticket->getDeptName(),
            'created' => $ticket->getCreateDate(),
            'user' => [
                'name' => $ticket->getName()->name,
                'email' => $ticket->getEmail()
            ],
            'entries' => $entries
        ]
    ]);
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
```

### Step 3: Create Reply Helper

Create `mcp_reply_ticket.php`:

```php
<?php
/**
 * MCP Helper: Reply to Ticket
 * 
 * Usage: php mcp_reply_ticket.php <json_payload>
 */

error_reporting(0);

define('ROOT_DIR', '/var/www/html/');
require_once ROOT_DIR . 'main.inc.php';
require_once INCLUDE_DIR . 'class.ticket.php';
require_once INCLUDE_DIR . 'class.thread.php';

$json_input = $argv[1] ?? '{}';
$data = json_decode($json_input, true);

if (!$data) {
    echo json_encode(['error' => 'Invalid JSON input']);
    exit(1);
}

$ticket_number = $data['ticket_number'] ?? '';
$message = $data['message'] ?? '';
$is_internal = $data['is_internal'] ?? false;

if (!$ticket_number || !$message) {
    echo json_encode(['error' => 'Missing required fields: ticket_number, message']);
    exit(1);
}

try {
    $ticket = Ticket::lookupByNumber($ticket_number);
    
    if (!$ticket) {
        echo json_encode(['error' => 'Ticket not found']);
        exit(1);
    }
    
    $thread = $ticket->getThread();
    
    if ($is_internal) {
        // Add internal note
        $entry = $thread->addNote([
            'body' => $message,
            'staffId' => 1, // Admin
            'poster' => 'MCP Server',
            'title' => 'Internal Note'
        ]);
    } else {
        // Add reply (response to customer)
        $entry = $thread->addResponse([
            'body' => $message,
            'staffId' => 1,
            'poster' => 'Support Team'
        ]);
    }
    
    if ($entry) {
        echo json_encode([
            'success' => true,
            'ticket_number' => $ticket_number,
            'entry_id' => $entry->getId(),
            'type' => $is_internal ? 'note' : 'response'
        ]);
    } else {
        echo json_encode(['error' => 'Failed to add reply']);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
```

### Step 4: Copy Scripts to Container

```powershell
# Copy the PHP helper scripts to the container
docker cp mcp_create_ticket.php osTicket-osticket:/var/www/html/
docker cp mcp_get_ticket.php osTicket-osticket:/var/www/html/
docker cp mcp_reply_ticket.php osTicket-osticket:/var/www/html/
```

### ✅ Checkpoint B.1
- [ ] All PHP scripts created
- [ ] Scripts copied to Docker container
- [ ] Test manually: `docker exec osTicket-osticket php mcp_get_ticket.php 123456`

---

## Exercise B.2: Building the MCP Server

**Goal**: Create the Python MCP server that uses the PHP helpers.

### Step 1: Create the Server

Create `mcp-server/server.py`:

```python
"""
osTicket MCP Server
===================
Provides AI assistant tools for interacting with osTicket.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import subprocess
import json
import os
import sys

app = Server("osticket")

# Backend configuration
BACKEND = os.environ.get("OSTICKET_BACKEND", "local")
DOCKER_EXE = os.environ.get("DOCKER_EXE", "docker")
WORKSPACE = os.environ.get("OSTICKET_WORKSPACE", "")

class OsTicketClient:
    """Client for interacting with osTicket via Docker."""
    
    async def execute_php(self, script_name: str, arg: str = None) -> dict:
        """Execute a PHP helper script inside the Docker container."""
        
        # Build command
        cmd = [DOCKER_EXE, "compose"]
        
        if WORKSPACE:
            cmd.extend(["-f", f"{WORKSPACE}/docker-compose.yml"])
        
        cmd.extend(["exec", "-T", "osticket", "php", f"/var/www/html/{script_name}"])
        
        if arg:
            cmd.append(arg)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=WORKSPACE or None
            )
            
            if result.returncode != 0:
                return {"error": f"Command failed: {result.stderr}"}
            
            return json.loads(result.stdout)
        
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON response: {result.stdout}"}
        except Exception as e:
            return {"error": str(e)}

# Create client instance
client = OsTicketClient()

@app.list_tools()
async def list_tools():
    """Return available osTicket tools."""
    return [
        Tool(
            name="create_ticket",
            description="Create a new support ticket in osTicket",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Customer name"
                    },
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "Customer email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Ticket subject line"
                    },
                    "message": {
                        "type": "string",
                        "description": "Ticket message/description"
                    },
                    "priority": {
                        "type": "integer",
                        "enum": [1, 2, 3, 4],
                        "default": 2,
                        "description": "Priority (1=Low, 2=Normal, 3=High, 4=Emergency)"
                    }
                },
                "required": ["email", "subject", "message"]
            }
        ),
        Tool(
            name="get_ticket",
            description="Get details of an existing ticket by ticket number",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_number": {
                        "type": "string",
                        "description": "The ticket number (e.g., '123456')"
                    }
                },
                "required": ["ticket_number"]
            }
        ),
        Tool(
            name="reply_to_ticket",
            description="Reply to an existing ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_number": {
                        "type": "string",
                        "description": "The ticket number to reply to"
                    },
                    "message": {
                        "type": "string",
                        "description": "Reply message content"
                    },
                    "is_internal": {
                        "type": "boolean",
                        "default": False,
                        "description": "True for internal note, False for customer reply"
                    }
                },
                "required": ["ticket_number", "message"]
            }
        ),
        Tool(
            name="get_osticket_status",
            description="Get the status of the osTicket system",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute an osTicket tool."""
    
    if name == "create_ticket":
        payload = json.dumps({
            "name": arguments.get("name", ""),
            "email": arguments["email"],
            "subject": arguments["subject"],
            "message": arguments["message"],
            "priority": arguments.get("priority", 2)
        })
        
        result = await client.execute_php("mcp_create_ticket.php", payload)
        
        if result.get("error"):
            return [TextContent(type="text", text=f"❌ Error: {result['error']}")]
        
        return [TextContent(type="text", text=f"""
✅ **Ticket Created Successfully!**

- Ticket Number: `{result['ticket_number']}`
- Subject: {result['subject']}
- User ID: {result['user_id']}

View at: http://localhost:8080/scp/tickets.php?number={result['ticket_number']}
""".strip())]
    
    elif name == "get_ticket":
        result = await client.execute_php("mcp_get_ticket.php", arguments["ticket_number"])
        
        if result.get("error"):
            return [TextContent(type="text", text=f"❌ Error: {result['error']}")]
        
        ticket = result["ticket"]
        entries_text = "\n".join([
            f"  [{e['type']}] {e['poster']}: {e['body'][:100]}..."
            for e in ticket.get("entries", [])[:5]
        ])
        
        return [TextContent(type="text", text=f"""
📋 **Ticket #{ticket['number']}**

- Subject: {ticket['subject']}
- Status: {ticket['status']}
- Department: {ticket['department']}
- Created: {ticket['created']}
- Customer: {ticket['user']['name']} ({ticket['user']['email']})

**Recent Activity:**
{entries_text or '  No entries'}
""".strip())]
    
    elif name == "reply_to_ticket":
        payload = json.dumps({
            "ticket_number": arguments["ticket_number"],
            "message": arguments["message"],
            "is_internal": arguments.get("is_internal", False)
        })
        
        result = await client.execute_php("mcp_reply_ticket.php", payload)
        
        if result.get("error"):
            return [TextContent(type="text", text=f"❌ Error: {result['error']}")]
        
        reply_type = "Internal note" if arguments.get("is_internal") else "Reply"
        return [TextContent(type="text", text=f"""
✅ **{reply_type} Added to Ticket #{result['ticket_number']}**

Entry ID: {result['entry_id']}
""".strip())]
    
    elif name == "get_osticket_status":
        result = await client.execute_php("mcp_status.php")
        
        if result.get("error"):
            return [TextContent(type="text", text=f"❌ osTicket is not responding: {result['error']}")]
        
        return [TextContent(type="text", text=f"""
✅ **osTicket Status: Online**

- Version: {result.get('version', 'Unknown')}
- Open Tickets: {result.get('open_tickets', 0)}
- Database: Connected
""".strip())]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Create the Test Script

Create `mcp-server/test.py`:

```python
"""
osTicket MCP Server Test Suite
==============================
Validates all MCP operations end-to-end.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_tests():
    """Run end-to-end MCP tests."""
    
    print("=" * 60)
    print("osTicket MCP Server Test Suite")
    print("=" * 60)
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[os.path.join(os.path.dirname(__file__), "server.py")],
        env={
            **os.environ,
            "OSTICKET_BACKEND": "local",
            "OSTICKET_WORKSPACE": os.path.dirname(os.path.dirname(__file__))
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            print("\n✅ Server initialized")
            
            # List tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools ({len(tools.tools)}):")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description[:50]}...")
            
            # Test 1: Create ticket
            print("\n" + "-" * 40)
            print("Test 1: Create Ticket")
            result = await session.call_tool("create_ticket", {
                "name": "Test User",
                "email": f"test{os.getpid()}@example.com",
                "subject": "MCP Test Ticket",
                "message": "This ticket was created by the MCP test suite."
            })
            print(result.content[0].text)
            
            # Extract ticket number from result
            ticket_number = None
            for line in result.content[0].text.split("\n"):
                if "Ticket Number:" in line:
                    ticket_number = line.split("`")[1]
                    break
            
            if ticket_number:
                # Test 2: Get ticket
                print("\n" + "-" * 40)
                print(f"Test 2: Get Ticket #{ticket_number}")
                result = await session.call_tool("get_ticket", {
                    "ticket_number": ticket_number
                })
                print(result.content[0].text)
                
                # Test 3: Reply to ticket
                print("\n" + "-" * 40)
                print(f"Test 3: Reply to Ticket #{ticket_number}")
                result = await session.call_tool("reply_to_ticket", {
                    "ticket_number": ticket_number,
                    "message": "This is an automated test reply from the MCP server.",
                    "is_internal": False
                })
                print(result.content[0].text)
            
            # Test 4: Get status
            print("\n" + "-" * 40)
            print("Test 4: Get osTicket Status")
            result = await session.call_tool("get_osticket_status", {})
            print(result.content[0].text)
            
            print("\n" + "=" * 60)
            print("✅ All tests completed!")
            print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
```

### ✅ Checkpoint B.2
- [ ] MCP server starts without errors
- [ ] All 4 tools are listed
- [ ] Test script passes all tests

---

## Exercise B.3: VS Code Integration

**Goal**: Register the MCP server with VS Code Copilot.

### Step 1: Configure VS Code Settings

Create/update `.vscode/settings.json`:

```json
{
    "mcp": {
        "servers": {
            "osticket": {
                "command": "python",
                "args": ["${workspaceFolder}/mcp-server/server.py"],
                "env": {
                    "OSTICKET_BACKEND": "local",
                    "OSTICKET_URL": "http://localhost:8080",
                    "OSTICKET_WORKSPACE": "${workspaceFolder}",
                    "DOCKER_EXE": "docker"
                }
            }
        }
    }
}
```

### Step 2: Test in VS Code

1. Reload VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Open Copilot Chat (`Ctrl+Shift+I`)
3. Try these prompts:

```
@mcp create a support ticket from john@example.com about "Password Reset" saying they can't log in
```

```
@mcp get the details of ticket number 123456
```

```
@mcp reply to ticket 123456 saying we've reset their password
```

### ✅ Checkpoint B.3
- [ ] MCP server visible in VS Code MCP panel
- [ ] Can create tickets via Copilot
- [ ] Can query tickets via Copilot
- [ ] Can reply to tickets via Copilot

---

# Part C: Extending the MCP Server

## Exercise C.1: Adding New Tools

**Goal**: Extend the MCP server with additional capabilities.

### 🏆 Challenge C.1: Implement These Tools

Add these tools to your MCP server:

1. **`list_tickets`** - List recent tickets with optional filtering
   - Parameters: `status` (open/closed/all), `limit` (number)

2. **`search_tickets`** - Search tickets by keyword
   - Parameters: `query` (search string)

3. **`update_ticket_status`** - Change ticket status
   - Parameters: `ticket_number`, `status` (open/closed/resolved)

4. **`create_user`** - Create a new osTicket user
   - Parameters: `name`, `email`

### Solution Template for `list_tickets`

PHP Helper (`mcp_list_tickets.php`):

```php
<?php
error_reporting(0);

define('ROOT_DIR', '/var/www/html/');
require_once ROOT_DIR . 'main.inc.php';
require_once INCLUDE_DIR . 'class.ticket.php';

$json_input = $argv[1] ?? '{}';
$data = json_decode($json_input, true);

$status = $data['status'] ?? 'all';
$limit = min($data['limit'] ?? 10, 50);

try {
    $tickets = [];
    $sql = "SELECT ticket_id FROM " . TICKET_TABLE;
    
    if ($status !== 'all') {
        $sql .= " WHERE status_id = " . ($status === 'open' ? 1 : 3);
    }
    
    $sql .= " ORDER BY created DESC LIMIT " . (int)$limit;
    
    $res = db_query($sql);
    while ($row = db_fetch_array($res)) {
        $ticket = Ticket::lookup($row['ticket_id']);
        if ($ticket) {
            $tickets[] = [
                'number' => $ticket->getNumber(),
                'subject' => $ticket->getSubject(),
                'status' => $ticket->getStatus()->getName(),
                'created' => $ticket->getCreateDate(),
                'email' => $ticket->getEmail()
            ];
        }
    }
    
    echo json_encode(['success' => true, 'tickets' => $tickets, 'count' => count($tickets)]);
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
```

Add to `server.py`:

```python
Tool(
    name="list_tickets",
    description="List recent tickets",
    inputSchema={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["all", "open", "closed"],
                "default": "all",
                "description": "Filter by status"
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 10,
                "description": "Maximum tickets to return"
            }
        }
    }
)
```

---

## Exercise C.2: Adding Resources

**Goal**: Expose osTicket data as MCP resources.

Add resources to your server:

```python
from mcp.types import Resource, TextResourceContents

@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="osticket://statistics",
            name="osTicket Statistics",
            description="Current ticket statistics",
            mimeType="application/json"
        ),
        Resource(
            uri="osticket://departments",
            name="Departments",
            description="List of departments",
            mimeType="application/json"
        ),
        Resource(
            uri="osticket://help-topics",
            name="Help Topics",
            description="Available help topics",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    if uri == "osticket://statistics":
        result = await client.execute_php("mcp_statistics.php")
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(result, indent=2)
        )
    
    # Implement other resources...
    raise ValueError(f"Unknown resource: {uri}")
```

---

## Exercise C.3: Adding Prompts

**Goal**: Create useful prompt templates.

```python
from mcp.types import Prompt, PromptMessage, PromptArgument

@app.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="ticket_summary",
            description="Generate a summary of a ticket for handoff",
            arguments=[
                PromptArgument(
                    name="ticket_number",
                    description="Ticket number to summarize",
                    required=True
                )
            ]
        ),
        Prompt(
            name="compose_reply",
            description="Help compose a professional reply to a ticket",
            arguments=[
                PromptArgument(
                    name="ticket_number",
                    description="Ticket to reply to",
                    required=True
                ),
                PromptArgument(
                    name="tone",
                    description="Tone of reply (formal, friendly, apologetic)",
                    required=False
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None):
    if name == "ticket_summary":
        ticket_number = arguments.get("ticket_number")
        result = await client.execute_php("mcp_get_ticket.php", ticket_number)
        
        if result.get("error"):
            raise ValueError(result["error"])
        
        ticket = result["ticket"]
        prompt_text = f"""
Please summarize this support ticket for handoff to another agent:

**Ticket #{ticket['number']}**
- Subject: {ticket['subject']}
- Customer: {ticket['user']['name']} ({ticket['user']['email']})
- Status: {ticket['status']}
- Created: {ticket['created']}

**Conversation History:**
{json.dumps(ticket.get('entries', []), indent=2)}

Please provide:
1. Brief summary of the issue
2. What has been done so far
3. What the next agent should do
"""
        return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text.strip()))]
    
    raise ValueError(f"Unknown prompt: {name}")
```

---

# Final Project

## 🏆 Challenge: Build a Complete Support AI Assistant

Create a comprehensive MCP server that transforms osTicket into an AI-powered support system.

### Requirements

| Category | Feature | Points |
|----------|---------|--------|
| **Core Tools** | Create, read, reply to tickets | 20 |
| **Advanced Tools** | Search, list, update, bulk operations | 20 |
| **User Management** | Create users, lookup users | 10 |
| **Resources** | Statistics, departments, topics | 15 |
| **Prompts** | Summary, compose reply, escalation | 15 |
| **Error Handling** | Graceful errors, logging | 10 |
| **Testing** | Comprehensive test suite | 10 |
| **Total** | | **100** |

### Deliverables

1. **Complete MCP Server** (`server.py`)
   - 8+ tools
   - 3+ resources
   - 3+ prompts

2. **PHP Helper Scripts**
   - Robust error handling
   - Input validation

3. **Test Suite** (`test.py`)
   - Tests for all tools
   - Error case testing

4. **Documentation** (`README.md`)
   - Setup instructions
   - Tool reference
   - Troubleshooting guide

### Bonus Challenges

- **+10 points**: Add caching for frequently accessed data
- **+10 points**: Implement webhook support for real-time updates
- **+10 points**: Add support for file attachments

---

## 📚 Reference Materials

### osTicket Resources
- [osTicket Documentation](https://docs.osticket.com)
- [osTicket GitHub](https://github.com/osTicket/osTicket)
- [osTicket API Reference](https://docs.osticket.com/en/latest/Developer%20Documentation/API.html)

### MCP Resources
- [MCP Specification](https://modelcontextprotocol.io)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)

### Lab Resources
- [Lab 1: MCP Fundamentals](./01_MCP_FUNDAMENTALS_LAB.md)
- [Docker Setup Guide](../DOCKER_SETUP.md)

---

## ✅ Lab Completion Checklist

### Part A: osTicket Setup
- [ ] A.1: osTicket running in Docker
- [ ] A.2: Created and processed a test ticket
- [ ] A.3: Explored database structure

### Part B: MCP Server
- [ ] B.1: PHP helper scripts created
- [ ] B.2: MCP server running
- [ ] B.3: VS Code integration working

### Part C: Extensions
- [ ] C.1: Added new tools
- [ ] C.2: Implemented resources
- [ ] C.3: Created prompts

### Final Project
- [ ] Complete MCP server submitted
- [ ] All tests passing
- [ ] Documentation complete

**Congratulations on completing the osTicket MCP Lab!** 🎉
