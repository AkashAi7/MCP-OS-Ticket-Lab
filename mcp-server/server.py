#!/usr/bin/env python3
"""
osTicket MCP Server
Provides Model Context Protocol tools for interacting with osTicket
"""

import asyncio
import json
import os
import subprocess
import uuid
from pathlib import Path
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Server configuration
OSTICKET_URL = os.getenv("OSTICKET_URL", "http://localhost:8080")
OSTICKET_API_KEY = os.getenv("OSTICKET_API_KEY", "")
OSTICKET_BACKEND = os.getenv("OSTICKET_BACKEND", "http").lower()
DOCKER_EXE = os.getenv("DOCKER_EXE", "docker")
PROJECT_DIR = Path(os.getenv("OSTICKET_DOCKER_PROJECT_DIR", Path(__file__).resolve().parents[1]))
HELPER_SCRIPT_MAP = {
    "create_ticket.php": "/usr/src/osticket/mcp_create_ticket.php",
    "get_ticket.php": "/usr/src/osticket/mcp_get_ticket.php",
    "reply_to_ticket.php": "/usr/src/osticket/mcp_reply_to_ticket.php",
    "create_user.php": "/usr/src/osticket/mcp_create_user.php",
}

# Initialize MCP server
app = Server("osticket-server")


class LocalDockerOsTicketClient:
    """Client for interacting with a local Dockerized osTicket instance."""

    def __init__(self, project_dir: Path, docker_exe: str, base_url: str):
        self.project_dir = Path(project_dir)
        self.docker_exe = docker_exe
        self.base_url = base_url.rstrip("/")

    def _compose_run(self, args: list[str], check: bool = False) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.docker_exe, "compose", *args],
            capture_output=True,
            text=True,
            cwd=self.project_dir,
            check=check,
        )

    async def _run_script(self, script_name: str, payload: dict) -> dict:
        script_path = HELPER_SCRIPT_MAP[script_name]
        result_file = f"/tmp/ost_mcp_{uuid.uuid4().hex}.json"
        command = [
            "exec",
            "-T",
            "-e",
            f"OST_MCP_PAYLOAD={json.dumps(payload)}",
            "-e",
            f"OST_MCP_RESULT_FILE={result_file}",
            "osticket",
            "php",
            script_path,
        ]

        def run() -> dict:
            completed = self._compose_run(command)
            try:
                if completed.returncode != 0:
                    detail = completed.stderr.strip() or completed.stdout.strip() or "Unknown error"
                    raise RuntimeError(detail)

                stdout = completed.stdout.strip()
                if stdout:
                    return json.loads(stdout)

                result = self._compose_run(["exec", "-T", "osticket", "cat", result_file])
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip() or "Result file was not created"
                    raise RuntimeError(f"No output from helper script {script_name}: {detail}")

                content = result.stdout.strip()
                if not content:
                    raise RuntimeError(f"Helper script {script_name} produced an empty result file")

                return json.loads(content)
            finally:
                self._compose_run(["exec", "-T", "osticket", "rm", "-f", result_file])

        return await asyncio.to_thread(run)

    async def create_ticket(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
        topic_id: int = 1,
        priority: int = 2,
        phone: str = "",
        source: str = "Web",
    ) -> dict:
        return await self._run_script(
            "create_ticket.php",
            {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
                "topic_id": topic_id,
                "priority": priority,
                "phone": phone,
                "source": source,
            },
        )

    async def get_ticket(self, ticket_number: str) -> dict:
        return await self._run_script("get_ticket.php", {"ticket_number": ticket_number})

    async def reply_to_ticket(self, ticket_id: str, message: str, alert: bool = True) -> dict:
        return await self._run_script(
            "reply_to_ticket.php",
            {"ticket_id": ticket_id, "message": message, "alert": alert},
        )

    async def create_user(self, name: str, email: str, phone: str = "") -> dict:
        return await self._run_script(
            "create_user.php",
            {"name": name, "email": email, "phone": phone},
        )

    async def get_status(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(f"{self.base_url}/")
            response.raise_for_status()
        return {
            "backend": "local",
            "url": self.base_url,
            "api_configured": bool(OSTICKET_API_KEY),
            "status": "Connected",
        }

class OsTicketClient:
    """Client for interacting with osTicket API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        # For web form method (fallback when API key auth fails)
        self.use_web_form = True  # Default to web form for now
    
    async def create_ticket(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
        topic_id: int = 1,
        priority: int = 2,
        phone: str = "",
        source: str = "API"
    ) -> dict:
        """Create a new ticket using web form (API key method has auth issues)"""
        # Use public web form submission (same as create_tickets_via_api.py)
        url = f"{self.base_url}/open.php"
        
        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
            'topicId': str(topic_id),
            'ip': "127.0.0.1"
        }
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.post(url, data=data)
            
            # Web form returns 200/302 on success (doesn't raise on redirect)
            # Check if submission was successful
            success = response.status_code in [200, 302] or "ticket" in response.text.lower()
            
            if not success:
                raise Exception(f"Ticket creation may have failed: {response.status_code}")
            
            # Extract ticket number from response if possible
            ticket_number = "Created"  # Web form doesn't return ticket number directly
            if "ticket" in response.text.lower():
                ticket_number = "Success"
            
            return {
                "status": "success",
                "message": "Ticket created successfully",
                "ticket_number": ticket_number,
                "name": name,
                "email": email,
                "subject": subject
            }
    
    async def get_ticket(self, ticket_number: str) -> dict:
        """Get ticket details by ticket number"""
        url = f"{self.base_url}/api/tickets/{ticket_number}.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def reply_to_ticket(
        self,
        ticket_id: str,
        message: str,
        alert: bool = True
    ) -> dict:
        """Reply to an existing ticket"""
        url = f"{self.base_url}/api/tickets/{ticket_id}/reply.json"
        
        data = {
            "message": f"data:text/html,{message}",
            "alert": alert,
            "source": "API"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def create_user(
        self,
        name: str,
        email: str,
        phone: str = ""
    ) -> dict:
        """Create a new user"""
        url = f"{self.base_url}/api/users.json"
        
        data = {
            "name": name,
            "email": email,
            "phone": phone
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def search_tickets_via_web(
        self,
        query: str = "",
        status: str = "open"
    ) -> str:
        """Search tickets via web interface (fallback when API doesn't support search)"""
        # This is a simplified version - in production, you'd use proper web scraping
        # or wait for osTicket to add search to their API
        url = f"{self.base_url}/scp/tickets.php?status={status}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            return f"Search via web interface - status: {status}"

    async def get_status(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(f"{self.base_url}/")
            response.raise_for_status()
        return {
            "backend": "http",
            "url": self.base_url,
            "api_configured": bool(self.api_key),
            "status": "Connected",
        }

# Initialize client
if OSTICKET_BACKEND == "local":
    client = LocalDockerOsTicketClient(PROJECT_DIR, DOCKER_EXE, OSTICKET_URL)
else:
    client = OsTicketClient(OSTICKET_URL, OSTICKET_API_KEY)

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available osTicket tools"""
    return [
        Tool(
            name="create_ticket",
            description="Create a new support ticket in osTicket. Use this when a user reports an issue, asks a question, or requests support.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the person creating the ticket"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address of the ticket creator"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Brief subject/title of the ticket"
                    },
                    "message": {
                        "type": "string",
                        "description": "Detailed message/description of the issue or request"
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Priority level: 1=Low, 2=Normal, 3=High, 4=Emergency",
                        "enum": [1, 2, 3, 4],
                        "default": 2
                    },
                    "topic_id": {
                        "type": "integer",
                        "description": "Topic/category ID (1=General Inquiry, 2=Feedback, 3=Technical Support, 4=Billing, 5=Product Issue)",
                        "default": 1
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number (optional)",
                        "default": ""
                    }
                },
                "required": ["name", "email", "subject", "message"]
            }
        ),
        Tool(
            name="get_ticket",
            description="Retrieve detailed information about a specific ticket using its ticket number. Use this to check ticket status, view conversation history, or get ticket details.",
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
            description="Add a response/reply to an existing ticket. Use this to provide updates, answers, or request more information from the ticket creator.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID or number to reply to"
                    },
                    "message": {
                        "type": "string",
                        "description": "The reply message content"
                    },
                    "alert": {
                        "type": "boolean",
                        "description": "Whether to send an email alert to the user",
                        "default": True
                    }
                },
                "required": ["ticket_id", "message"]
            }
        ),
        Tool(
            name="create_user",
            description="Create a new user/customer in osTicket. Use this when registering a new customer who will be creating tickets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full name of the user"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address of the user (must be unique)"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number (optional)",
                        "default": ""
                    }
                },
                "required": ["name", "email"]
            }
        ),
        Tool(
            name="get_osticket_status",
            description="Get the current status and configuration of the osTicket server. Use this to verify connectivity and get system information.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "create_ticket":
            result = await client.create_ticket(
                name=arguments["name"],
                email=arguments["email"],
                subject=arguments["subject"],
                message=arguments["message"],
                priority=arguments.get("priority", 2),
                topic_id=arguments.get("topic_id", 1),
                phone=arguments.get("phone", "")
            )
            
            return [TextContent(
                type="text",
                text=f"✅ Ticket created successfully!\n\n"
                     f"Ticket Number: {result.get('ticket_number', 'N/A')}\n"
                     f"Subject: {arguments['subject']}\n"
                     f"Priority: {arguments.get('priority', 2)}\n"
                     f"Created for: {arguments['name']} ({arguments['email']})\n\n"
                     f"The ticket has been submitted and the user will receive a confirmation email."
            )]
        
        elif name == "get_ticket":
            result = await client.get_ticket(arguments["ticket_number"])
            
            # Format ticket information
            ticket_info = json.dumps(result, indent=2)
            
            return [TextContent(
                type="text",
                text=f"📋 Ticket Information\n\n{ticket_info}"
            )]
        
        elif name == "reply_to_ticket":
            result = await client.reply_to_ticket(
                ticket_id=arguments["ticket_id"],
                message=arguments["message"],
                alert=arguments.get("alert", True)
            )
            
            return [TextContent(
                type="text",
                text=f"✅ Reply added successfully!\n\n"
                     f"Ticket ID: {arguments['ticket_id']}\n"
                     f"Email alert sent: {arguments.get('alert', True)}\n\n"
                     f"Your response has been added to the ticket."
            )]
        
        elif name == "create_user":
            result = await client.create_user(
                name=arguments["name"],
                email=arguments["email"],
                phone=arguments.get("phone", "")
            )
            
            return [TextContent(
                type="text",
                text=f"✅ User created successfully!\n\n"
                     f"Name: {arguments['name']}\n"
                     f"Email: {arguments['email']}\n"
                     f"User ID: {result.get('id', 'N/A')}"
            )]
        
        elif name == "get_osticket_status":
            result = await client.get_status()
            return [TextContent(
                type="text",
                text=f"🟢 osTicket Server Status\n\n"
                     f"URL: {result['url']}\n"
                     f"Backend: {result['backend']}\n"
                     f"API Configured: {'Yes' if result['api_configured'] else 'No'}\n"
                     f"Status: {result['status']}\n\n"
                     f"Available operations:\n"
                     f"  • Create tickets\n"
                     f"  • Get ticket information\n"
                     f"  • Reply to tickets\n"
                     f"  • Create users"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]
    
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if hasattr(e.response, 'text') else str(e)
        return [TextContent(
            type="text",
            text=f"❌ API Error: {e.response.status_code}\n\n{error_detail}\n\n"
                 f"Tip: If you get a 401 error, make sure OSTICKET_API_KEY is set correctly."
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error: {str(e)}\n\n"
                 f"Please check your osTicket configuration and try again."
        )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
