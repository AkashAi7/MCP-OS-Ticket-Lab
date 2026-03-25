# Contributing to MCP osTicket Lab

Thank you for your interest in contributing! This repository is a learning environment for [Model Context Protocol (MCP)](https://modelcontextprotocol.io) development. Contributions that improve the learning experience, fix bugs, or extend the MCP server are very welcome.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Reporting Issues](#reporting-issues)

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/MCP-OS-Ticket-Lab.git
   cd MCP-OS-Ticket-Lab
   ```
3. Create a **feature branch** from `main`:
   ```bash
   git checkout -b feature/my-improvement
   ```
4. Make your changes, then open a **pull request** back to `main`.

---

## Ways to Contribute

| Type | Examples |
|------|---------|
| 🐛 Bug fixes | Typos in docs, broken scripts, incorrect commands |
| 📚 Lab improvements | New exercises, better explanations, additional solutions |
| 🔧 MCP server extensions | New tools, improved error handling, new backends |
| 🐳 Docker improvements | Better Dockerfile, docker-compose options, cross-platform fixes |
| 🌐 New integrations | Alternative ticket systems, additional AI assistant configs |
| 📖 Documentation | Missing guides, clearer examples, architecture diagrams |

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Docker Desktop | Latest | Run osTicket locally |
| Python | 3.10+ | MCP server development |
| VS Code | Latest | IDE with Copilot MCP support |
| Git | Any | Version control |

### 1. Start the local lab

```powershell
# Windows – one-click install
.\install-local.cmd
.\prepare-mcp-local.cmd
```

This will:
- Build and start the osTicket, MySQL, and phpMyAdmin Docker containers.
- Install and configure osTicket automatically.
- Install Python dependencies for the MCP server.
- Register the MCP server with VS Code.

### 2. Install Python dependencies manually (optional)

```bash
cd mcp-server
pip install -r requirements.txt
```

### 3. Verify the MCP server

```bash
cd mcp-server
python test.py
```

Expected output:
```
🔧 Testing osTicket MCP Server
✅ All tests completed successfully!
```

---

## Contribution Guidelines

### Adding Lab Exercises

Lab files live in the `labs/` directory. Follow the existing style:

- Use numbered headings (`## Exercise 1`, `## Exercise 2`).
- Include a **Concept** section, a **Task** section, and a **Solution** section.
- Keep difficulty labels consistent: `Beginner`, `Intermediate`, or `Advanced`.
- Test every code snippet before submitting.

### Adding MCP Tools

New tools are added to `mcp-server/server.py`:

1. Add the tool definition inside the `list_tools()` handler:
   ```python
   Tool(
       name="my_new_tool",
       description="Clear, one-sentence description of what this tool does.",
       inputSchema={
           "type": "object",
           "properties": {
               "param1": {"type": "string", "description": "..."}
           },
           "required": ["param1"]
       }
   )
   ```
2. Add the handler inside `call_tool()`:
   ```python
   elif name == "my_new_tool":
       result = await client.my_new_tool(arguments["param1"])
       return [TextContent(type="text", text=f"Result: {result}")]
   ```
3. If a PHP helper script is required, add it to the repository root as `mcp_<action>.php` and register it in `HELPER_SCRIPT_MAP` in `server.py`.
4. Update `mcp-server/README.md` with the new tool's parameters and an example.

### Adding PHP Helper Scripts

PHP helpers live at the repository root (`mcp_*.php`) and run inside the osTicket Docker container. Follow the pattern established by the existing helpers:

```php
<?php
require __DIR__ . '/mcp_bootstrap.php';

// Read payload
$raw = getenv('OST_MCP_PAYLOAD');
if ($raw === false || $raw === '') {
    $raw = stream_get_contents(STDIN);
}
$payload = json_decode($raw, true);

// Validate
if (!is_array($payload) || empty($payload['required_field'])) {
    mcp_emit_error('required_field is required');
}

// Do work using osTicket's PHP API…
// Emit result
mcp_emit_json(['status' => 'success', 'result' => $result]);
```

### Documentation Changes

- Place project-level docs at the repository root.
- Place MCP-server-specific docs inside `mcp-server/`.
- Place lab content inside `labs/`.
- Keep line length reasonable (≤ 120 characters in prose, no limit in code blocks).

---

## Pull Request Process

1. Ensure the MCP server tests still pass:
   ```bash
   cd mcp-server && python test.py
   ```
2. Update relevant documentation (README, lab files, etc.) to reflect your changes.
3. Open a pull request against the `main` branch.
4. Fill in the pull request description with:
   - **What** changed and **why**.
   - Steps to verify the change works.
   - Screenshots or example output where applicable.
5. A maintainer will review your PR. Address any feedback promptly.

---

## Code Style

### Python (MCP server)

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use `async`/`await` for all I/O operations.
- Add docstrings to every public function and class.
- Prefer explicit error messages that help users fix problems.

### PHP (helper scripts)

- Use 4-space indentation.
- Always call `mcp_emit_error()` on failure rather than `die()` or bare `exit`.
- Never expose raw database errors to the MCP client; include a safe summary only.

### Markdown (docs and labs)

- Use ATX headings (`##`, `###`).
- Fence code blocks with the language identifier (` ```python `, ` ```bash `, etc.).
- Use tables for structured comparisons.

---

## Reporting Issues

Use [GitHub Issues](https://github.com/AkashAi7/MCP-OS-Ticket-Lab/issues) to report bugs or suggest improvements. When reporting a bug, please include:

- Your operating system and version.
- Docker Desktop version (`docker --version`).
- Python version (`python --version`).
- The exact error message or unexpected behavior.
- Steps to reproduce the issue.

---

## License

By contributing, you agree that your contributions will be licensed under the same licenses as the rest of the project:

- Lab materials and MCP server: **MIT License**
- osTicket core files: **GPL2 License**
