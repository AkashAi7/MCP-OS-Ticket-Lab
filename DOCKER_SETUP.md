# osTicket Docker Setup Guide

## Prerequisites
- Docker Desktop installed and running
- At least 2GB of free RAM
- Ports 8080, 8081, and 3306 available

## Simple Lab Flow

This repo now supports a two-step local lab:

1. Run osTicket locally with one click
2. Prepare and validate the MCP against that local instance

## Step 1: Run osTicket Locally

### Windows

Double-click `install-local.cmd`

Or run:

```powershell
.\install-local.ps1
```

The installer will:
- Build osTicket from this local repository
- Start MySQL, osTicket, and phpMyAdmin
- Complete the osTicket setup automatically
- Create sample tickets in the running osTicket instance
- Open the local URLs in your browser

Default local credentials created by the installer:
- Admin URL: http://localhost:8080/scp/
- Username: `ostadmin`
- Password: `ChangeMe123!`
- Email: `admin@local.test`

Change those values by passing parameters to `install-local.ps1`.

## Step 2: Prepare the MCP Locally

Double-click `prepare-mcp-local.cmd`

Or run:

```powershell
.\prepare-mcp-local.ps1
```

This step will:
- verify the local Docker lab is running
- normalize the running `ost-config.php` if needed
- install Python dependencies from `mcp-server/requirements.txt`
- run the local MCP validation suite

When it succeeds, the MCP server is ready through the workspace registration in `.vscode/settings.json`.

## Quick Start

### Recommended

```powershell
.\install-local.ps1 -ResetData
.\prepare-mcp-local.ps1
```

### Manual Start Only
```bash
docker compose up -d --build
```

This will start:
- **osTicket Web Interface** at http://localhost:8080
- **MySQL Database** (internal)
- **phpMyAdmin** at http://localhost:8081

### Manual Web Install

1. Open your browser and go to: **http://localhost:8080/setup/**

2. Fill in the installation form:

   **System Settings:**
   - Helpdesk Name: `My Support Desk` (or your choice)
   - Default Email: `support@yourdomain.com`

   **Admin User:**
   - First Name: Your first name
   - Last Name: Your last name
   - Email Address: Your email
   - Username: `admin`
   - Password: Choose a strong password

   **Database Settings:**
   - MySQL Hostname: `mysql`
   - MySQL Database: `osticket`
   - MySQL Username: `osticket`
   - MySQL Password: `osticket123`
   - MySQL Table Prefix: `ost_`

3. Click **Install Now**

### Manual Post-Installation

After installation completes:

1. **Delete the setup directory:**
   ```bash
   docker exec osticket-web rm -rf /var/www/html/setup
   ```

2. **Set proper permissions on ost-config.php:**
   ```bash
   docker exec osticket-web chmod 644 /var/www/html/include/ost-config.php
   ```

### Access Your System

- **Admin Panel:** http://localhost:8080/scp/
  - Login with the admin credentials you created

- **Customer Portal:** http://localhost:8080/
  - This is where users submit tickets

- **phpMyAdmin:** http://localhost:8081/
  - Access the database directly (username: `osticket`, password: `osticket123`)

## Useful Commands

### View Logs
```bash
docker-compose logs -f osticket
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Access Web Container Shell
```bash
docker exec -it osticket-web bash
```

### Access MySQL Container
```bash
docker exec -it osticket-mysql mysql -u osticket -posticket123 osticket
```

### Backup Database
```bash
docker exec osticket-mysql mysqldump -u osticket -posticket123 osticket > backup.sql
```

### Restore Database
```bash
docker exec -i osticket-mysql mysql -u osticket -posticket123 osticket < backup.sql
```

## Troubleshooting

### Docker daemon is not running
Start Docker Desktop and wait until it reports that the engine is running, then re-run `install-local.cmd` or `docker compose up -d --build`.

### Port Already in Use
If port 8080 is already in use, edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:80"  # Change 8080 to another port like 8082
```

### Permission Issues
```bash
docker exec osticket-web chmod -R 777 /var/www/html/uploads
```

### Reset Everything
```bash
docker compose down -v
docker compose up -d --build
```
This will delete all data and start fresh.

To fully rerun the unattended installer, execute:

```powershell
.\install-local.ps1 -ResetData
```

To revalidate the MCP after code changes, execute:

```powershell
.\prepare-mcp-local.ps1
```

## Configuration

### Email Configuration (Optional)
After installation, configure email in:
- Admin Panel → Emails → Settings
- Configure SMTP or use PHP mail()

### Create Departments
- Admin Panel → Agents → Departments

### Create Help Topics
- Admin Panel → Manage → Help Topics

### Add Agents (Staff)
- Admin Panel → Agents → Agents

## Sample Test Ticket

1. Go to http://localhost:8080/
2. Click "Open a New Ticket"
3. Fill in:
   - Email: test@example.com
   - Full Name: Test User
   - Help Topic: General Inquiry
   - Issue Summary: Test ticket
   - Details: This is a test support ticket
4. Submit and note the ticket number
5. Login to Admin Panel to see and respond to the ticket

## Production Considerations

⚠️ **This setup is for DEVELOPMENT ONLY**

For production:
- Use strong passwords (not the defaults)
- Use environment variables for sensitive data
- Enable SSL/HTTPS
- Configure proper email settings
- Set up regular database backups
- Restrict database access
- Use a reverse proxy (nginx/Traefik)

## Support

- osTicket Documentation: https://docs.osticket.com/
- osTicket Forums: https://forum.osticket.com/
- GitHub Issues: https://github.com/osTicket/osTicket/issues
