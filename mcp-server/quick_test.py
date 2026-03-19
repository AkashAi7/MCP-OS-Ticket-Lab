"""
Quick inline test of MCP server - creates a ticket directly
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from server import OsTicketClient

async def test():
    client = OsTicketClient(
        "http://localhost:8080",
        "62528D6F9730D7B834DF39E970FD7894"
    )
    
    print("🎫 Creating test ticket via MCP server...\n")
    
    result = await client.create_ticket(
        name="VS Code Test User",
        email="vscode.test@example.com",
        subject="MCP Server Integration Test",
        message="This ticket was created directly from VS Code using the osTicket MCP server!",
        priority=2,
        topic_id=1
    )
    
    print("✅ Success!")
    print(f"\nTicket Details:")
    print(f"  Subject: {result['subject']}")
    print(f"  Name: {result['name']}")
    print(f"  Email: {result['email']}")
    print(f"  Status: {result['status']}")
    print(f"\n🌐 View in osTicket: http://localhost:8080/scp/")

if __name__ == "__main__":
    asyncio.run(test())
