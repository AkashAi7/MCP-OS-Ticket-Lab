# Frequently Asked Questions (FAQ)

Answers to the most common questions about the **MCP osTicket Lab**.

---

## Table of Contents

- [General](#general)
- [Setup & Installation](#setup--installation)
- [MCP Server](#mcp-server)
- [Docker & Containers](#docker--containers)
- [VS Code / GitHub Copilot](#vs-code--github-copilot)
- [Claude Desktop](#claude-desktop)
- [osTicket](#osticket)
- [Security](#security)

---

## General

### What is this repository?

This repository is a hands-on learning lab for [Model Context Protocol (MCP)](https://modelcontextprotocol.io) development. It uses [osTicket](https://osticket.com) — a real-world open-source helpdesk system — as the backend, so you can practice building production-ready MCP servers against a realistic application.

### Do I need to know PHP to use this lab?

No. The PHP helper scripts (`mcp_*.php`) are already written for you. You only need PHP knowledge if you want to extend them with new operations. The main development work is in Python (`mcp-server/server.py`).

### Which operating system is supported?

The one-click installers (`install-local.cmd`, `prepare-mcp-local.cmd`) target **Windows**. The Docker containers and Python MCP server run on **Windows, macOS, and Linux** — just substitute PowerShell commands with their Bash equivalents where needed.

---

## Setup & Installation

### How do I get started quickly?

```powershell
# Step 1 – Install osTicket (Docker required)
.\install-local.cmd

# Step 2 – Set up the MCP server
.\prepare-mcp-local.cmd
```

Then open VS Code in this folder — the MCP server is already registered in `.vscode/settings.json`.

For detailed instructions see [DOCKER_SETUP.md](DOCKER_SETUP.md).

### What are the default credentials?

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| osTicket Admin Panel | http://localhost:8080/scp/ | `ostadmin` | `ChangeMe123!` |
| phpMyAdmin | http://localhost:8081/ | `osticket` | `osticket123` |
| MySQL (direct) | localhost:3306 | `osticket` | `osticket123` |

> ⚠️ Change these before exposing the services outside your local machine.

### The installer says "Docker daemon is not running". What do I do?

Start **Docker Desktop** and wait for the whale icon in the system tray to show a steady (non-animated) state, then re-run `.\install-local.cmd`.

### Port 8080 is already in use on my machine. How do I change it?

Edit `docker-compose.yml` and change the host port:

```yaml
ports:
  - "8082:80"   # was 8080:80 — use any free port
```

Then update `OSTICKET_URL` in `mcp-server/.env` (or `.vscode/settings.json`) to match the new port.

### How do I reset everything to a clean state?

```powershell
.\install-local.ps1 -ResetData
```

This stops the containers, removes all Docker volumes (deleting all data), rebuilds the images, and re-runs the unattended installer.

---

## MCP Server

### How do I run the MCP server manually?

```powershell
cd mcp-server
python server.py
```

The server listens on **stdio** — it is meant to be launched by an MCP client (VS Code, Claude Desktop), not run standalone in a terminal. Running it in a terminal will display nothing until a client connects.

### How do I test that the MCP server works?

```powershell
cd mcp-server
python test.py
```

Expected output:
```
🔧 Testing osTicket MCP Server
✅ All tests completed successfully!
```

### What environment variables does the MCP server use?

| Variable | Default | Description |
|----------|---------|-------------|
| `OSTICKET_URL` | `http://localhost:8080` | Base URL of the osTicket instance |
| `OSTICKET_BACKEND` | `http` | `local` (Docker exec) or `http` (REST API) |
| `OSTICKET_API_KEY` | _(empty)_ | API key (required for `http` backend) |
| `OSTICKET_DOCKER_PROJECT_DIR` | Parent dir of `server.py` | Path to repo root (local backend) |
| `DOCKER_EXE` | `docker` | Path to the Docker executable |

Copy `mcp-server/.env.example` to `mcp-server/.env` and fill in your values.

### What is the difference between the `local` and `http` backends?

| | `local` | `http` |
|-|---------|--------|
| How it works | Runs PHP helper scripts inside the Docker container via `docker compose exec` | Calls the osTicket REST API over HTTP |
| Requires Docker | Yes | No (osTicket can be remote) |
| Requires API key | No (uses internal PHP API) | Yes |
| Recommended for | Local lab work | Remote / production instances |

### How do I add a new MCP tool?

1. Write a PHP helper script `mcp_<action>.php` at the repository root.
2. Add the script path to `HELPER_SCRIPT_MAP` in `mcp-server/server.py`.
3. Add the tool definition to `list_tools()` and a handler to `call_tool()`.
4. Update `mcp-server/README.md` with the new tool's documentation.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full step-by-step guide.

---

## Docker & Containers

### What containers are started?

| Container | Purpose | Default port |
|-----------|---------|-------------|
| `osticket` | osTicket (PHP + Apache) | 8080 |
| `mysql` | MySQL 8.0 database | 3306 (internal) |
| `phpmyadmin` | Database web UI | 8081 |

### How do I view container logs?

```bash
docker logs osTicket-osticket   # osTicket web container
docker compose logs -f          # all containers, live
```

### How do I access a shell inside the osTicket container?

```bash
docker compose exec osticket bash
```

### How do I back up the database?

```bash
docker exec osTicket-mysql mysqldump -u osticket -posticket123 osticket > backup.sql
```

---

## VS Code / GitHub Copilot

### How is the MCP server registered in VS Code?

The server is registered in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.mcp.servers": {
    "osticket": {
      "command": "python",
      "args": ["${workspaceFolder}/mcp-server/server.py"],
      "env": {
        "OSTICKET_URL": "http://localhost:8080",
        "OSTICKET_BACKEND": "local",
        "OSTICKET_DOCKER_PROJECT_DIR": "${workspaceFolder}",
        "DOCKER_EXE": "docker"
      }
    }
  }
}
```

> **Windows users:** If `docker` is not on your PATH, set `DOCKER_EXE` to the full path, e.g. `C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe`.

### The MCP server doesn't appear in VS Code. What should I do?

1. Make sure the Python dependencies are installed: `pip install -r mcp-server/requirements.txt`
2. Reload the VS Code window: `Ctrl+Shift+P` → **Developer: Reload Window**
3. Check the Output panel (`Ctrl+Shift+U`) → select **GitHub Copilot** from the dropdown for error messages.

### How do I use the MCP tools from GitHub Copilot Chat?

In the Copilot Chat panel (Ask mode), you can use natural language:

```
Create a support ticket for Alice (alice@example.com) about a login issue — high priority.
Get the details of ticket number 123456.
Reply to ticket 123456 saying the issue has been resolved.
```

Copilot will call the appropriate MCP tool automatically.

---

## Claude Desktop

### How do I connect the MCP server to Claude Desktop?

Edit (or create) the Claude Desktop config file:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osticket": {
      "command": "python",
      "args": ["C:\\path\\to\\MCP-OS-Ticket-Lab\\mcp-server\\server.py"],
      "env": {
        "OSTICKET_URL": "http://localhost:8080",
        "OSTICKET_BACKEND": "local",
        "OSTICKET_DOCKER_PROJECT_DIR": "C:\\path\\to\\MCP-OS-Ticket-Lab"
      }
    }
  }
}
```

Replace `C:\\path\\to\\MCP-OS-Ticket-Lab` with the actual path where you cloned this repository. Restart Claude Desktop after saving the file.

---

## osTicket

### Where is the osTicket admin panel?

http://localhost:8080/scp/ — default credentials: `ostadmin` / `ChangeMe123!`

### How do I create an API key in osTicket?

1. Open the Admin Panel: http://localhost:8080/scp/
2. Go to **Manage → API Keys → Add New API Key**
3. Set **IP Address** to `0.0.0.0/0` (development only — restrict in production)
4. Enable **Can Create Tickets**
5. Click **Add Key** and copy the generated key

Set the key as `OSTICKET_API_KEY` in your environment (see `mcp-server/.env.example`).

### How do I load sample tickets for testing?

The one-click installer creates sample tickets automatically. To reload them:

```powershell
.\install-local.ps1 -ResetData
```

Or run the Python script manually:

```powershell
pip install mysql-connector-python
python create_sample_tickets.py
```

See [SAMPLE_TICKETS_README.md](SAMPLE_TICKETS_README.md) for details.

---

## Security

### Is it safe to run this lab on a public server?

No. This setup is designed for **local development only**. The default passwords are weak, phpMyAdmin is unauthenticated, and the MCP server has no access control. See [SECURITY.md](SECURITY.md) for hardening guidance before any public deployment.

### I accidentally committed my API key. What should I do?

1. Rotate the key immediately: **osTicket Admin → Manage → API Keys → Delete** the compromised key and create a new one.
2. Remove the secret from the repository history (e.g., using `git filter-repo` or the GitHub secret scanning remediation flow).
3. Add `mcp-server/.env` to `.gitignore` (it already is in this repo — do not remove that entry).

### How do I avoid committing secrets?

- Copy `mcp-server/.env.example` to `mcp-server/.env` for your local config — `.env` is listed in `.gitignore` and will not be tracked.
- Never hard-code API keys or passwords in source files.
- See [SECURITY.md](SECURITY.md) for the full security policy.
