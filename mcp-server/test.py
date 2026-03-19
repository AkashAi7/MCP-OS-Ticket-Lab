"""
Quick test script to verify the osTicket MCP server is working
"""

import asyncio
import os
import httpx
from server import OsTicketClient
from server import LocalDockerOsTicketClient
from pathlib import Path

async def test_client():
    """Test the osTicket client"""
    
    # Configure client
    url = os.getenv("OSTICKET_URL", "http://localhost:8080")
    api_key = os.getenv("OSTICKET_API_KEY", "")
    backend = os.getenv("OSTICKET_BACKEND", "http")

    if backend != "local" and not api_key:
        print("❌ Error: OSTICKET_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  PowerShell: $env:OSTICKET_API_KEY = 'your-api-key'")
        print("  Bash: export OSTICKET_API_KEY='your-api-key'")
        return
    
    print("🔧 Testing osTicket MCP Server\n")
    print(f"URL: {url}")
    print(f"Backend: {backend}")
    if backend != "local":
        print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else f"API Key: {api_key}")
    print()

    if backend == "local":
        client = LocalDockerOsTicketClient(
            Path(os.getenv("OSTICKET_DOCKER_PROJECT_DIR", Path(__file__).resolve().parents[1])),
            os.getenv("DOCKER_EXE", "docker"),
            url,
        )
    else:
        client = OsTicketClient(url, api_key)
    
    try:
        # Test 1: Create a test ticket
        print("📝 Test 1: Creating a test ticket...")
        unique_suffix = int(asyncio.get_event_loop().time())
        result = await client.create_ticket(
            name="Jordan Rivers",
            email=f"jordan.rivers.{unique_suffix}@example.com",
            subject="Unable to access billing dashboard",
            message="I can sign in successfully, but the billing dashboard shows an access denied message for my account.",
            priority=2,
            topic_id=1
        )
        print(f"✅ Success! Ticket created: {result}")
        print()

        print("📄 Test 1b: Fetching created ticket...")
        ticket_result = await client.get_ticket(result["ticket_number"])
        print(f"✅ Success! Ticket fetched: {ticket_result.get('ticket_number', result['ticket_number'])}")
        print()
        
        # Test 2: Get user (if create_user is implemented)
        print("👤 Test 2: Creating a test user...")
        try:
            user_result = await client.create_user(
                name="MCP Validation User",
                email=f"mcptest{asyncio.get_event_loop().time()}@example.com",
                phone="555-1234"
            )
            print(f"✅ Success! User created: {user_result}")
        except httpx.HTTPStatusError as e:
            print(f"⚠️  User creation failed: {e}")
            print(f"Response: {e.response.text}")
        except Exception as e:
            print(f"⚠️  User creation failed (may already exist): {e}")
        print()

        print("💬 Test 3: Replying to the test ticket...")
        reply_result = await client.reply_to_ticket(
            ticket_id=result["ticket_number"],
            message="We have verified the account details and are investigating the billing dashboard access issue now.",
            alert=False,
        )
        print(f"✅ Success! Reply posted: {reply_result}")
        print()
        
        print("✅ All tests completed successfully!")
        print("\n🎉 Your osTicket MCP server is ready to use!")
        
    except httpx.HTTPStatusError as e:
        print(f"❌ Test failed: {e}")
        print(f"\nResponse body: {e.response.text}")
        print("\nTroubleshooting:")
        print("1. Make sure osTicket is running: docker-compose ps")
        print("2. Verify your API key in Admin Panel → Manage → API Keys")
        print("3. Ensure the API key has 'Can Create Tickets' permission")
        print("4. Check that IP address 0.0.0.0/0 is allowed (for testing)")

if __name__ == "__main__":
    asyncio.run(test_client())
