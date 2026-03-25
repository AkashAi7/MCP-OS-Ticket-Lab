# Architecture Overview

This document describes how the components of the **MCP osTicket Lab** fit together.

---

## Table of Contents

- [High-Level Architecture](#high-level-architecture)
- [Component Descriptions](#component-descriptions)
- [Data Flow](#data-flow)
- [Directory Layout](#directory-layout)
- [Technology Stack](#technology-stack)
- [Environment Variables](#environment-variables)
- [Extending the Architecture](#extending-the-architecture)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Developer Machine                             │
│                                                                     │
│  ┌──────────────┐    MCP (stdio)    ┌──────────────────────────┐   │
│  │  AI Client   │ ◄──────────────► │   MCP Server             │   │
│  │  (VS Code /  │                  │   mcp-server/server.py   │   │
│  │   Claude)    │                  └────────────┬─────────────┘   │
│  └──────────────┘                               │                  │
│                                                 │ docker compose   │
│                              ┌──────────────────▼──────────────┐  │
│                              │        Docker Network            │  │
│                              │                                  │  │
│                              │  ┌────────────────────────────┐ │  │
│                              │  │  osticket container        │ │  │
│                              │  │  PHP 8.2 + Apache          │ │  │
│                              │  │  ┌──────────────────────┐  │ │  │
│                              │  │  │  mcp_*.php helpers   │  │ │  │
│                              │  │  │  (run inside this    │  │ │  │
│                              │  │  │   container)         │  │ │  │
│                              │  │  └──────────────────────┘  │ │  │
│                              │  └────────────────────────────┘ │  │
│                              │                │                  │  │
│                              │  ┌─────────────▼──────────────┐ │  │
│                              │  │  mysql container           │ │  │
│                              │  │  MySQL 8.0                 │ │  │
│                              │  └────────────────────────────┘ │  │
│                              │                                  │  │
│                              │  ┌────────────────────────────┐ │  │
│                              │  │  phpmyadmin container      │ │  │
│                              │  │  (optional – DB UI)        │ │  │
│                              │  └────────────────────────────┘ │  │
│                              └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Descriptions

### AI Client

The AI client (VS Code with GitHub Copilot, or Claude Desktop) communicates with the MCP server over **stdio** (standard input / standard output). The client sends JSON-RPC requests to call tools, and the server responds with JSON-encoded results.

Configuration lives in `.vscode/settings.json` (VS Code) or `claude_desktop_config.json` (Claude Desktop).

### MCP Server (`mcp-server/server.py`)

A Python application built on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). It:

- Registers a set of **tools** (functions the AI can call).
- Receives tool-call requests from the AI client over stdio.
- Dispatches requests to the appropriate **backend** (local Docker or remote HTTP).
- Returns structured JSON responses formatted as `TextContent`.

Two backends are supported, selected by the `OSTICKET_BACKEND` environment variable:

| Backend | Value | How it works |
|---------|-------|--------------|
| **Local Docker** (default for labs) | `local` | Executes PHP helper scripts inside the `osticket` container via `docker compose exec` |
| **Remote HTTP** | `http` | Calls the osTicket REST API directly over HTTP with an API key |

### PHP Helper Scripts (`mcp_*.php`)

Small PHP scripts that run **inside** the `osticket` Docker container. They use osTicket's internal PHP class library to perform operations on tickets and users, avoiding the limitations of the external REST API.

| Script | Purpose |
|--------|---------|
| `mcp_bootstrap.php` | Bootstraps the osTicket PHP environment; provides `mcp_emit_json()` and `mcp_emit_error()` helpers |
| `mcp_create_ticket.php` | Creates a ticket using `Ticket::create()` |
| `mcp_get_ticket.php` | Retrieves ticket details using `Ticket::lookupByNumber()` |
| `mcp_reply_to_ticket.php` | Posts a reply to an existing ticket thread |
| `mcp_create_user.php` | Creates a new osTicket user |

Scripts receive input via the `OST_MCP_PAYLOAD` environment variable (JSON-encoded) and write results either to stdout or to a temporary file specified by `OST_MCP_RESULT_FILE`.

### osTicket Container

Runs PHP 8.2 + Apache, built from the local `Dockerfile`. It serves:

- The **customer portal** at `http://localhost:8080/`
- The **staff control panel** at `http://localhost:8080/scp/`

The application files from this repository are bind-mounted into `/var/www/html` inside the container, so the PHP helper scripts at the repository root are available inside the container at `/usr/src/osticket/`.

### MySQL Container

Stores all osTicket data. The MCP server never connects to MySQL directly; all database access goes through the osTicket PHP layer.

### phpMyAdmin Container

Optional web UI for browsing the database directly, available at `http://localhost:8081/`.

---

## Data Flow

### Local Docker backend (lab default)

```
AI Client
   │  MCP tool-call request (stdio JSON-RPC)
   ▼
MCP Server (server.py)
   │  Serialises arguments to JSON → sets OST_MCP_PAYLOAD env var
   │  Runs: docker compose exec osticket php /usr/src/osticket/mcp_<action>.php
   ▼
PHP Helper Script (inside osticket container)
   │  Reads OST_MCP_PAYLOAD
   │  Calls osTicket PHP API (Ticket::create, Ticket::lookupByNumber, …)
   ▼
osTicket PHP Library
   │  SQL queries
   ▼
MySQL Container
   │  Returns rows
   ▼
osTicket PHP Library
   │  Returns PHP objects
   ▼
PHP Helper Script
   │  Encodes result as JSON → writes to OST_MCP_RESULT_FILE (or stdout)
   ▼
MCP Server (server.py)
   │  Reads result file (or stdout), parses JSON
   │  Returns TextContent to AI client
   ▼
AI Client
```

### Remote HTTP backend

```
AI Client
   │  MCP tool-call request (stdio JSON-RPC)
   ▼
MCP Server (server.py)
   │  HTTP POST/GET to http://<osticket-host>/api/tickets/<id>.json
   │  X-API-Key: <OSTICKET_API_KEY>
   ▼
osTicket REST API
   │  SQL queries
   ▼
MySQL
   │  Returns rows
   ▼
osTicket REST API
   │  Returns JSON response
   ▼
MCP Server (server.py)
   │  Parses JSON, returns TextContent to AI client
   ▼
AI Client
```

---

## Directory Layout

```
MCP-OS-Ticket-Lab/
│
├── mcp-server/                  # MCP server (Python)
│   ├── server.py                # Main server – tool definitions and handlers
│   ├── test.py                  # Validation test suite
│   ├── quick_test.py            # Lightweight inline test
│   ├── requirements.txt         # Python dependencies (mcp, httpx)
│   ├── README.md                # MCP server documentation
│   └── QUICKSTART.md            # Step-by-step quick start
│
├── mcp_bootstrap.php            # PHP bootstrap + helper functions
├── mcp_create_ticket.php        # PHP: create ticket
├── mcp_get_ticket.php           # PHP: get ticket
├── mcp_reply_to_ticket.php      # PHP: reply to ticket
├── mcp_create_user.php          # PHP: create user
│
├── labs/                        # Learning lab content
│   ├── README.md                # Lab index and learning path
│   ├── 01_MCP_FUNDAMENTALS_LAB.md
│   ├── 02_OSTICKET_MCP_LAB.md
│   └── MCP_CHEAT_SHEET.md
│
├── docker-compose.yml           # Orchestrates osticket, mysql, phpmyadmin
├── Dockerfile                   # Builds the osticket container image
├── docker-entrypoint.sh         # Container startup script
│
├── install-local.cmd            # Windows: one-click osTicket setup
├── install-local.ps1            # PowerShell: full unattended installer
├── prepare-mcp-local.cmd        # Windows: one-click MCP preparation
├── prepare-mcp-local.ps1        # PowerShell: MCP validation + VS Code wiring
│
├── .vscode/settings.json        # VS Code MCP server registration
│
├── README.md                    # Project overview and quick start
├── ARCHITECTURE.md              # This file
├── CONTRIBUTING.md              # Contribution guidelines
├── DOCKER_SETUP.md              # Detailed Docker setup guide
├── SECURITY.md                  # Security policy
└── [osTicket core files]        # Upstream osTicket application files
```

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| MCP server | Python + [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) | Python 3.10+, mcp ≥ 1.0.0 |
| HTTP client | [httpx](https://www.python-httpx.org/) | ≥ 0.27.0 |
| PHP backend | PHP + osTicket class library | PHP 8.2 |
| Web server | Apache (inside Docker) | 2.4 |
| Database | MySQL | 8.0 |
| Containerisation | Docker Compose | v2 |
| AI integration | MCP over stdio (VS Code Copilot / Claude Desktop) | – |

---

## Environment Variables

The MCP server reads the following environment variables at startup:

| Variable | Default | Description |
|----------|---------|-------------|
| `OSTICKET_URL` | `http://localhost:8080` | Base URL of the osTicket instance |
| `OSTICKET_API_KEY` | _(empty)_ | API key for the remote HTTP backend |
| `OSTICKET_BACKEND` | `http` | Backend selector: `local` (Docker) or `http` (REST API) |
| `OSTICKET_DOCKER_PROJECT_DIR` | Parent dir of `server.py` | Path to the repo root (used by the local Docker backend to locate `docker-compose.yml`) |
| `DOCKER_EXE` | `docker` | Path to the Docker executable |

The local Docker backend also uses two variables **inside the container** when running a PHP helper script:

| Variable | Description |
|----------|-------------|
| `OST_MCP_PAYLOAD` | JSON-encoded input payload for the helper script |
| `OST_MCP_RESULT_FILE` | Temp file path where the helper writes its JSON result |

---

## Extending the Architecture

### Adding a new MCP tool

1. Write a PHP helper script `mcp_<action>.php` at the repository root.
2. Register it in `HELPER_SCRIPT_MAP` in `mcp-server/server.py`.
3. Add the tool definition in `list_tools()` and a handler in `call_tool()`.
4. Update `mcp-server/README.md` with the new tool's documentation.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full step-by-step guide.

### Using a remote osTicket instance

Set the following environment variables before starting the MCP server:

```bash
export OSTICKET_BACKEND=http
export OSTICKET_URL=https://your-osticket.example.com
export OSTICKET_API_KEY=your-api-key
```

The server will use the REST API backend (`OsTicketClient`) instead of the Docker backend.

### Connecting a different AI client

Any MCP-compatible client can connect to the server. The server communicates over **stdio** so the client simply needs to launch `python mcp-server/server.py` as a subprocess and send JSON-RPC messages on its stdin/stdout. Refer to the [MCP specification](https://modelcontextprotocol.io) for the protocol details.
