# osTicket MCP Server - Configuration Example

# 1. Get your API Key
#    - Go to http://localhost:8080/scp/
#    - Navigate to: Manage → API Keys
#    - Click "Add New API Key"
#    - Configure:
#      * IP Address: 0.0.0.0/0 (for development)
#      * Can Create Tickets: ✓ Enabled
#      * Can Execute Cron: (optional)
#    - Copy the generated API key

# 2. Set environment variables (choose your platform)

# Windows PowerShell:
$env:OSTICKET_URL = "http://localhost:8080"
$env:OSTICKET_API_KEY = "YOUR_API_KEY_HERE"

# Linux/Mac Bash:
# export OSTICKET_URL="http://localhost:8080"
# export OSTICKET_API_KEY="YOUR_API_KEY_HERE"

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test the server
python test.py

# 5. Run the MCP server
python server.py
