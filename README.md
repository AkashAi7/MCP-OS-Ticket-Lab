# MCP osTicket Lab

> **Learn Model Context Protocol (MCP) by building an AI-powered support ticket system**

<a href="https://osticket.com"><img height="80px" width="80px" src="images/favicon.png" align="left" hspace="10" vspace="6"></a>

This repository provides a complete hands-on learning environment for **Model Context Protocol (MCP)** development using **osTicket** as a real-world application. You'll learn to build MCP servers from scratch, integrate them with AI assistants, and create production-ready tools.

<br clear="left"/>

---

## 🚀 One-Click Quick Start

Get osTicket running locally with MCP integration in 2 simple steps:

### Step 1: Install osTicket
```powershell
.\install-local.cmd
```
This will:
- Start Docker containers (osTicket, MySQL, phpMyAdmin)
- Install and configure osTicket automatically
- Create admin account: `ostadmin` / `ChangeMe123!`

### Step 2: Prepare MCP Integration
```powershell
.\prepare-mcp-local.cmd
```
This will:
- Validate osTicket installation
- Install Python MCP dependencies
- Test the MCP server
- Register with VS Code

**That's it!** 🎉 You now have:
- ✅ osTicket running at http://localhost:8080
- ✅ Staff panel at http://localhost:8080/scp
- ✅ phpMyAdmin at http://localhost:8081
- ✅ MCP server ready for VS Code Copilot

---

## 📚 Learning Labs

Two comprehensive lab tracks with exercises, challenges, and solutions:

| Lab | Duration | Level | Focus |
|-----|----------|-------|-------|
| **[Lab 1: MCP Fundamentals](labs/01_MCP_FUNDAMENTALS_LAB.md)** | 4-6 hours | Beginner → Advanced | MCP concepts, tools, resources, testing |
| **[Lab 2: osTicket MCP Development](labs/02_OSTICKET_MCP_LAB.md)** | 6-8 hours | Intermediate → Advanced | Real-world MCP server, Docker integration |

**Quick References:**
- [Lab Overview & Learning Path](labs/README.md)
- [MCP Development Cheat Sheet](labs/MCP_CHEAT_SHEET.md)

---

## 🎯 What You'll Learn

### Lab 1: MCP Fundamentals
- ✅ Build your first MCP server (Hello World)
- ✅ Define tools with JSON Schema validation
- ✅ Create resources and prompts
- ✅ Integrate with VS Code Copilot
- ✅ Handle external APIs (Weather API example)
- ✅ Implement error handling and testing
- ✅ Build production-ready MCP solutions

### Lab 2: osTicket MCP Development
- ✅ Set up osTicket locally with Docker
- ✅ Understand osTicket architecture and API
- ✅ Build PHP helper scripts for osTicket
- ✅ Create an MCP server for ticket operations
- ✅ Test MCP integration end-to-end
- ✅ Extend with custom tools and features

---

## 📋 Prerequisites

| Component | Version | Check Command |
|-----------|---------|---------------|
| **Docker Desktop** | Latest | `docker --version` |
| **Python** | 3.10+ | `python --version` |
| **VS Code** | Latest | `code --version` |
| **Git** | Any | `git --version` |

**Python Packages:**
```powershell
pip install mcp>=1.0.0 httpx>=0.27.0
```

**See full requirements:** [Requirements Guide](labs/README.md#prerequisites-checklist)

---

## 🏗️ Repository Structure

```
MCP-OS-Ticket-Lab/
├── README.md                          # This file
├── install-local.cmd                  # One-click osTicket setup
├── prepare-mcp-local.cmd              # One-click MCP preparation
├── DOCKER_SETUP.md                    # Detailed Docker setup guide
│
├── labs/                              # 📚 Learning Labs
│   ├── README.md                      # Lab index & learning path
│   ├── 01_MCP_FUNDAMENTALS_LAB.md     # Lab 1: MCP basics to advanced
│   ├── 02_OSTICKET_MCP_LAB.md         # Lab 2: osTicket MCP development
│   └── MCP_CHEAT_SHEET.md             # Quick reference guide
│
├── mcp-server/                        # 🔧 MCP Server Implementation
│   ├── server.py                      # Main MCP server
│   ├── test.py                        # MCP validation tests
│   └── requirements.txt               # Python dependencies
│
├── mcp_*.php                          # PHP helper scripts for osTicket
├── docker-compose.yml                 # Docker orchestration
├── Dockerfile                         # osTicket container image
└── [osTicket core files]              # osTicket application files
```

---

## 🎓 Learning Path

```
┌─────────────────────────────────────────────────────────────┐
│  START HERE: One-Click Setup                                │
│  .\install-local.cmd                                        │
│  .\prepare-mcp-local.cmd                                    │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │   Choose Path   │
        └────┬──────┬─────┘
             │      │
    ┌────────▼──┐  │
    │  Lab 1    │  │  Beginner? Start with MCP Fundamentals
    │  MCP      │  │  Learn concepts, build simple servers
    │  Basics   │  │
    └────────┬──┘  │
             │     │
             │  ┌──▼──────┐
             │  │  Lab 2  │  Intermediate? Jump to osTicket
             │  │ osTicket│  Build real-world MCP server
             │  │   MCP   │
             │  └────┬────┘
             │       │
        ┌────▼───────▼─────┐
        │  MCP Expert! 🎉   │
        │  Build your own   │
        │  MCP projects     │
        └───────────────────┘
```

---

## 🔧 MCP Server Features

The included MCP server provides these tools for osTicket:

| Tool | Description |
|------|-------------|
| `create_ticket` | Create new support tickets |
| `get_ticket` | Retrieve ticket details by number |
| `reply_to_ticket` | Add replies or internal notes |
| `create_user` | Create new osTicket users |
| `get_osticket_status` | Check system status |

**Test it in VS Code Copilot:**
```
@mcp create a ticket from john@example.com about password reset
@mcp get details of ticket 123456
@mcp reply to ticket 123456 saying we've resolved the issue
```

---

## 🐳 Docker Quick Reference

```powershell
# Start osTicket
docker compose up -d

# Stop osTicket
docker compose down

# View logs
docker logs osTicket-osticket

# Restart containers
docker compose restart

# Access container shell
docker compose exec osticket bash
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8080 already in use | Stop other services or edit `docker-compose.yml` |
| Docker won't start | Enable WSL2/Hyper-V, restart Docker Desktop |
| MySQL connection refused | Wait 30 seconds after startup |
| MCP server not found in VS Code | Reload window: `Ctrl+Shift+P` → "Reload Window" |

**See detailed troubleshooting:** [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

## 📖 Additional Resources

**In this repository:**
- [FAQ](FAQ.md) — Answers to common questions
- [Architecture Overview](ARCHITECTURE.md) — How components fit together
- [Docker Setup Guide](DOCKER_SETUP.md) — Detailed Docker instructions
- [MCP Server Reference](mcp-server/README.md) — Tool documentation
- [Contributing Guide](CONTRIBUTING.md) — How to extend the lab
- [Security Policy](SECURITY.md) — Security considerations

**External links:**
- **osTicket Documentation:** https://docs.osticket.com
- **MCP Specification:** https://modelcontextprotocol.io
- **Python MCP SDK:** https://github.com/modelcontextprotocol/python-sdk
- **Docker Documentation:** https://docs.docker.com

---

## 🤝 Contributing

This is a learning repository. Feel free to:
- Add new lab exercises
- Improve existing materials
- Fix bugs or typos
- Share your MCP server extensions

---

## 📜 License

- osTicket core: GPL License (see [LICENSE.txt](LICENSE.txt))
- Lab materials: MIT License
- MCP server implementation: MIT License

---

## 🙏 Acknowledgments

- **osTicket Team** - For the excellent open-source helpdesk system
- **Anthropic** - For the Model Context Protocol specification
- **GitHub Copilot** - For MCP integration capabilities

---

**Ready to start?** Run `.\install-local.cmd` and begin your MCP journey! 🚀

Requirements
------------
  * HTTP server running Microsoft® IIS or Apache
  * PHP version 8.2 - 8.4 (8.4 recommended)
  * mysqli extension for PHP
  * MySQL database version 5.5 (or greater)

### Recommendations
  * ctype, fileinfo, gd, gettext, iconv, imap, intl, json, mbstring,
    Zend OPcache, phar, xml, xml-dom, and zip extensions for PHP
  * APCu module enabled and configured for PHP

Deployment
----------
osTicket now supports bleeding-edge installations. The easiest way to
install the software and track updates is to clone the public repository.
Create a folder on you web server (using whatever method makes sense for
you) and cd into it. Then clone the repository (the folder must be empty!):

    git clone https://github.com/osTicket/osTicket

And deploy the code into somewhere in your server's www root folder, for
instance

    cd osTicket
    php manage.php deploy --setup /var/www/htdocs/osticket/

Then you can configure your server if necessary to serve that folder, and
visit the page and install osTicket as usual. Go ahead and even delete
setup/ folder out of the deployment location when you’re finished. Then,
later, you can fetch updates and deploy them (from the folder where you
cloned the git repo into)

    git pull
    php manage.php deploy -v /var/www/htdocs/osticket/

Upgrading
---------
osTicket supports upgrading from 1.6-rc1 and later versions. As with any
upgrade, strongly consider a backup of your attachment files, database, and
osTicket codebase before embarking on an upgrade. Please review our [Upgrade
Guide](https://docs.osticket.com/en/latest/Getting%20Started/Upgrade%20and%20Migration.html)
or the [UPGRADING.txt file](UPGRADING.txt) for upgrade instructions.

Help
----
Visit the [Documentation](https://docs.osticket.com/) or the
[forum](https://forum.osticket.com/). And if you'd like professional help
managing your osTicket installation,
[commercial support](https://osticket.com/support/) is available.

Contributing
------------
Create your own fork of the project and use
[git-flow](https://github.com/nvie/gitflow) to create a new feature. Once
the feature is published in your fork, send a pull request to begin the
conversation of integrating your new feature into osTicket.

### Localization
[![Crowdin](https://badges.crowdin.net/osticket-official/localized.svg)](https://crowdin.com/project/osticket-official)

The interface for osTicket is now completely translatable. Language packs
are available on the [download page](https://osticket.com/download). If you
do not see your language there, join the [Crowdin](https://crowdin.com/project/osticket-official)
project and request to have your language added. Languages which reach 100%
translated are are significantly reviewed will be made available on the
osTicket download page.

The software can also be translated in place in our [JIPT site](http://jipt.i18n.osticket.com).
Once you have a Crowdin account, login and translate the software in your browser!

Localizing strings in new code requires usage of a [few rules](setup/doc/i18n.md).

License
-------
osTicket is released under the GPL2 license. See the included LICENSE.txt
file for the gory details of the General Public License.

osTicket is supported by several magical open source projects including:

  * [Font-Awesome](https://fontawesome.com/)
  * [HTMLawed](https://www.bioinformatics.org/phplabware/internal_utilities/htmLawed)
  * [jQuery dropdown](https://labs.abeautifulsite.net/jquery-dropdown/) (Project Deleted)
  * [jsTimezoneDetect](https://pellepim.bitbucket.org/jstz/)
  * [laminas-mail](https://github.com/laminas/laminas-mail)
  * [mPDF](https://github.com/mpdf/mpdf)
  * [PasswordHash](https://www.openwall.com/phpass/)
  * [PEAR](https://pear.php.net/package/PEAR)
  * [PEAR/Auth_SASL](https://pear.php.net/package/Auth_SASL)
  * [PEAR/Mail](https://pear.php.net/package/mail)
  * [PEAR/Net_SMTP](https://pear.php.net/package/Net_SMTP)
  * [PEAR/Net_Socket](https://pear.php.net/package/Net_Socket)
  * [PEAR/Serivces_JSON](https://pear.php.net/package/Services_JSON)
  * [php-gettext](https://launchpad.net/php-gettext/)
  * [phpseclib](https://phpseclib.sourceforge.net/)
  * [Spyc](https://github.com/mustangostang/spyc)
