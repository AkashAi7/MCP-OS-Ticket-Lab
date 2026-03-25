# Security Policy

## Supported Versions

This repository is a **learning lab** and does not maintain versioned releases in the traditional sense. The latest commit on the `main` branch is the supported version.

---

## Reporting a Vulnerability

### MCP Server / Lab Materials

If you discover a security vulnerability in the MCP server (`mcp-server/`) or the PHP helper scripts (`mcp_*.php`), please **do not** open a public GitHub issue. Instead, use [GitHub's private vulnerability reporting](https://github.com/AkashAi7/MCP-OS-Ticket-Lab/security/advisories/new) or email the maintainer directly.

Please include:
- A clear description of the vulnerability.
- Steps to reproduce.
- Potential impact.
- Any suggested mitigations.

### osTicket Core

For vulnerabilities in the underlying osTicket application files, please follow the upstream security process:

> Send all proof-of-concept reports to **security[at]osticket[dot]com**.

---

## Security Considerations for This Lab

### ⚠️ This setup is for development / learning only

The default configuration is intentionally simple to aid learning. **Do not expose this setup to the public internet** without following the hardening steps below.

### API Keys

- The `OSTICKET_API_KEY` environment variable grants full access to create and read tickets.
- **Never commit API keys** to version control.
- Rotate API keys regularly, especially after sharing with others.
- Use IP restrictions on the osTicket API key when possible (Manage → API Keys in the admin panel).

### Docker / Local Environment

- The default MySQL password (`osticket123`) and admin password (`ChangeMe123!`) must be changed before deploying outside a local machine.
- The `phpmyadmin` container exposes your database without authentication by default. Do not expose port `8081` to the network.
- The `OSTICKET_BACKEND=local` mode lets the MCP server run arbitrary PHP inside the container via `docker compose exec`. Ensure only trusted users can send MCP tool-call requests to the server.

### MCP Server

- The MCP server runs as the current OS user. Do not run it as root.
- Tool input is passed directly to PHP scripts; always validate parameters inside each `mcp_*.php` helper.
- The `OST_MCP_PAYLOAD` environment variable is set per-request and cleaned up after execution. Ensure `OST_MCP_RESULT_FILE` temp files are deleted after use (the server does this automatically).

### Production Deployment

If you adapt this project for a real production environment:

- Use HTTPS for all traffic to osTicket.
- Store secrets in a secrets manager (Azure Key Vault, AWS Secrets Manager, etc.) rather than environment variables.
- Restrict network access to the MCP server so only trusted AI clients can reach it.
- Enable osTicket audit logs and monitor for unusual activity.
- Keep PHP, MySQL, and Docker images up to date.

