# osTicket MCP Server - Quick Start Guide

## ✅ Installation Complete!

Your osTicket MCP server is now installed with all dependencies.

## 📋 Next Steps

### Step 1: Get Your API Key

1. Open osTicket Admin Panel: http://localhost:8080/scp/
2. Login (default credentials vary by image - check container docs)
3. Go to: **Manage** → **API Keys**
4. Click **"Add New API Key"**
5. Configure:
   - **IP Address**: `0.0.0.0/0` (allows all IPs for development)
   - **Can Create Tickets**: ✓ **Enabled**
   - **Can Execute Cron**: Optional
6. Click **"Add Key"**
7. **Copy the generated API key** (you won't be able to see it again!)

### Step 2: Configure Environment Variables

**Option A: PowerShell (Windows)**
```powershell
cd mcp-server
$env:OSTICKET_URL = "http://localhost:8080"
$env:OSTICKET_API_KEY = "PASTE_YOUR_API_KEY_HERE"
```

**Option B: Bash (Linux/Mac)**
```bash
cd mcp-server
export OSTICKET_URL="http://localhost:8080"
export OSTICKET_API_KEY="PASTE_YOUR_API_KEY_HERE"
```

### Step 3: Test the Server

```powershell
python test.py
```

Expected output:
```
🔧 Testing osTicket MCP Server
✅ Success! Ticket created
✅ All tests completed successfully!
🎉 Your osTicket MCP server is ready to use!
```

### Step 4: Run the MCP Server

```powershell
python server.py
```

The server will run and wait for MCP client connections.

## 🔧 Configure in Your AI Assistant

### For Claude Desktop

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osticket": {
      "command": "python",
      "args": [
        "C:\\path\\to\\MCP-OS-Ticket-Lab\\mcp-server\\server.py"
      ],
      "env": {
        "OSTICKET_URL": "http://localhost:8080",
        "OSTICKET_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

> **Note:** Replace `C:\\path\\to\\MCP-OS-Ticket-Lab` with the actual path where you cloned this repository.

**After adding the config:**
1. Restart Claude Desktop
2. Look for the 🔌 icon showing MCP servers connected
3. Try: "Create a support ticket for testing"

### For VS Code / GitHub Copilot

The MCP server is already available in this workspace context!

You can now ask me to:
- Create support tickets
- Get ticket information
- Reply to tickets
- Manage users

## 🎯 Example Commands

Once configured, you can ask your AI assistant:

```
"Create a ticket for John Doe (john@example.com) about login issues"

"Get details for ticket #123456"

"Reply to ticket #123456 saying we've fixed the issue"

"Create a new user named Jane Smith with email jane@company.com"

"Check osTicket server status"
```

## 🚀 Available Tools

1. **create_ticket** - Create new support tickets
2. **get_ticket** - Retrieve ticket details
3. **reply_to_ticket** - Add responses to tickets
4. **create_user** - Register new users
5. **get_osticket_status** - Check server status

## 🔍 Troubleshooting

### "API Key not configured"
```powershell
$env:OSTICKET_API_KEY = "your-actual-api-key"
```

### "401 Unauthorized"
- Double-check your API key is correct
- Verify API is enabled in osTicket admin panel
- Make sure IP 0.0.0.0/0 is in the allowed list

### "Connection refused"
```powershell
docker ps  # Make sure osticket-web container is running
```

### Test isn't working
```powershell
# Make sure you're in the mcp-server directory
cd mcp-server

# Verify environment variables are set
echo $env:OSTICKET_URL
echo $env:OSTICKET_API_KEY

# Run test again
python test.py
```

## 📚 Documentation

- Full documentation: See `README.md`
- osTicket API docs: http://localhost:8080/api/docs/
- MCP Protocol: https://modelcontextprotocol.io/

## 💡 Advanced Use Cases

Now that you have the MCP server running, you can:

1. **Automate Support** - AI creates tickets from customer conversations
2. **Smart Triage** - AI analyzes and prioritizes tickets
3. **Auto-Responses** - AI suggests or sends responses
4. **Integration** - Connect with Teams, Slack, email systems
5. **Analytics** - Pull ticket data for insights

## ✨ You're All Set!

Your osTicket MCP server is ready to make your support system AI-powered! 🎉
