# osTicket MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to interact with osTicket helpdesk system.

## Features

This MCP server provides the following tools for AI assistants:

- **create_ticket** - Create new support tickets
- **get_ticket** - Retrieve ticket details and status
- **reply_to_ticket** - Add responses to existing tickets
- **create_user** - Register new users/customers
- **get_osticket_status** - Check server connectivity and status

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure osTicket API

1. Open your osTicket Admin Panel: http://localhost:8080/scp/
2. Go to **Manage** → **API Keys**
3. Click **Add New API Key**
4. Configure:
   - **IP Address**: `0.0.0.0/0` (for development)
   - **Can Create Tickets**: ✓ Enabled
   - **Can Execute Cron**: Optional
5. Copy the generated API key

### 3. Set Environment Variables

```bash
# Windows (PowerShell)
$env:OSTICKET_URL = "http://localhost:8080"
$env:OSTICKET_API_KEY = "YOUR_API_KEY_HERE"

# Linux/Mac
export OSTICKET_URL="http://localhost:8080"
export OSTICKET_API_KEY="YOUR_API_KEY_HERE"
```

## Usage

### Running the MCP Server

```bash
python server.py
```

### Configuring in Claude Desktop

Add to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osticket": {
      "command": "python",
      "args": [
        "C:\\Users\\akashdwivedi\\OneDrive - Microsoft\\Desktop\\IntrestingIdeas\\osTicket\\mcp-server\\server.py"
      ],
      "env": {
        "OSTICKET_URL": "http://localhost:8080",
        "OSTICKET_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Using with GitHub Copilot (VS Code)

Add to `.vscode/settings.json` or user settings:

```json
{
  "github.copilot.advanced": {
    "mcp.servers": {
      "osticket": {
        "command": "python",
        "args": ["./mcp-server/server.py"],
        "env": {
          "OSTICKET_URL": "http://localhost:8080",
          "OSTICKET_API_KEY": "YOUR_API_KEY_HERE"
        }
      }
    }
  }
}
```

## Available Tools

### 1. create_ticket

Create a new support ticket.

**Parameters:**
- `name` (required): Name of the person creating the ticket
- `email` (required): Email address
- `subject` (required): Brief subject/title
- `message` (required): Detailed description
- `priority` (optional): 1=Low, 2=Normal (default), 3=High, 4=Emergency
- `topic_id` (optional): Category ID (1=General, 2=Feedback, 3=Technical, 4=Billing, 5=Product Issue)
- `phone` (optional): Contact phone number

**Example:**
```
Create a ticket for John Smith (john@example.com) about "Cannot login to account" 
with message "I've been locked out of my account for 2 hours" - make it high priority.
```

### 2. get_ticket

Retrieve information about a specific ticket.

**Parameters:**
- `ticket_number` (required): The ticket number to retrieve

**Example:**
```
Get details for ticket #123456
```

### 3. reply_to_ticket

Add a response to an existing ticket.

**Parameters:**
- `ticket_id` (required): Ticket ID or number
- `message` (required): Reply message content
- `alert` (optional): Send email notification (default: true)

**Example:**
```
Reply to ticket #123456 with "We've reset your password. Please check your email."
```

### 4. create_user

Create a new user/customer.

**Parameters:**
- `name` (required): Full name
- `email` (required): Email address (must be unique)
- `phone` (optional): Phone number

**Example:**
```
Create a new user named "Jane Doe" with email jane@company.com
```

### 5. get_osticket_status

Check osTicket server status and configuration.

**Example:**
```
Check osTicket server status
```

## Use Cases

### Customer Support Automation
```
AI Assistant: "I see you're having login issues. Let me create a support ticket for you."
[Creates ticket with priority based on severity]
[Provides ticket number to customer]
```

### Ticket Management
```
AI Assistant: "Let me check the status of your ticket #123456"
[Retrieves ticket details]
[Provides update to customer]
```

### Automated Responses
```
AI Assistant: "I've found a solution to your issue."
[Replies to ticket with solution]
[Marks as resolved if appropriate]
```

## Advanced Integration Ideas

### 1. AI-Powered Triage
Use Azure OpenAI to analyze incoming messages and automatically:
- Set appropriate priority levels
- Route to correct departments
- Suggest relevant knowledge base articles

### 2. Sentiment Analysis
Integrate Azure Cognitive Services to:
- Detect frustrated customers
- Escalate urgent issues
- Track customer satisfaction

### 3. Chatbot Integration
Connect with Teams/Slack to:
- Create tickets from chat conversations
- Provide status updates in real-time
- Enable self-service ticket creation

### 4. Smart Knowledge Base
Use RAG (Retrieval Augmented Generation) to:
- Suggest solutions from past tickets
- Auto-respond to common questions
- Build a self-improving knowledge base

## Troubleshooting

### "API Key not configured"
Set the `OSTICKET_API_KEY` environment variable with your API key from the admin panel.

### "401 Unauthorized"
- Verify your API key is correct
- Check that API is enabled in osTicket admin panel
- Ensure IP restrictions allow your connection

### "Connection refused"
- Make sure osTicket is running: `docker-compose ps`
- Verify the URL is correct: http://localhost:8080
- Check if port 8080 is accessible

### "Tool not found"
Restart Claude Desktop or VS Code after adding the MCP server configuration.

## Development

### Testing the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:OSTICKET_URL = "http://localhost:8080"
$env:OSTICKET_API_KEY = "your-api-key"

# Run the server
python server.py
```

### Adding New Tools

Edit `server.py` and add new tools in the `@app.list_tools()` function, then implement the handler in `@app.call_tool()`.

## Security Notes

⚠️ **Important**: 
- Never commit API keys to version control
- Use IP restrictions in production
- Rotate API keys regularly
- Use HTTPS in production environments
- Validate and sanitize all inputs

## License

MIT

## Support

For issues related to:
- **osTicket**: Visit https://osticket.com/
- **MCP Protocol**: Visit https://modelcontextprotocol.io/
- **This Server**: Create an issue in the repository
