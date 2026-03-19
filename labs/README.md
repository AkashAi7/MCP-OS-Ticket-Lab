# MCP Learning Labs

> Hands-on exercises for learning Model Context Protocol (MCP) from beginner to advanced.

---

## 📚 Lab Overview

| Lab | Title | Level | Duration | Prerequisites |
|-----|-------|-------|----------|---------------|
| [Lab 1](01_MCP_FUNDAMENTALS_LAB.md) | MCP Fundamentals | Beginner → Advanced | 4-6 hours | Python, VS Code |
| [Lab 2](02_OSTICKET_MCP_LAB.md) | osTicket MCP Development | Intermediate → Advanced | 6-8 hours | Lab 1, Docker |

---

## 🎯 Learning Path

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           BEGINNER TRACK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Lab 1: Module 1                Lab 1: Module 2                       │
│   ┌──────────────────┐          ┌──────────────────┐                   │
│   │ Hello World MCP  │ ───────► │ Multiple Tools   │                   │
│   │ Server           │          │ + VS Code Setup  │                   │
│   └──────────────────┘          └──────────────────┘                   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                         INTERMEDIATE TRACK                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Lab 1: Module 3                Lab 2: Part A                          │
│   ┌──────────────────┐          ┌──────────────────┐                   │
│   │ Resources &      │ ───────► │ osTicket Setup   │                   │
│   │ Prompts          │          │ & Exploration    │                   │
│   └──────────────────┘          └──────────────────┘                   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                           ADVANCED TRACK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Lab 1: Modules 4-6             Lab 2: Parts B-C                      │
│   ┌──────────────────┐          ┌──────────────────┐                   │
│   │ API Integration  │ ───────► │ Full MCP Server  │                   │
│   │ Error Handling   │          │ for osTicket     │                   │
│   │ Testing          │          │ + Extensions     │                   │
│   └──────────────────┘          └──────────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: MCP Fundamentals Only
Start with Lab 1 to learn MCP concepts without external dependencies.

```powershell
# Create a new folder for Lab 1
mkdir mcp-labs
cd mcp-labs

# Follow Lab 1 exercises
```

### Option 2: Full osTicket Lab
Start with the one-click osTicket setup, then work through both labs.

```powershell
# Clone and setup osTicket
.\install-local.cmd

# Then follow Lab 2 (which includes Lab 1 concepts)
```

---

## 📋 Prerequisites Checklist

### For Lab 1 (MCP Fundamentals)
- [ ] Python 3.10+ installed
- [ ] VS Code with Copilot extension
- [ ] Basic Python knowledge
- [ ] Git installed

### For Lab 2 (osTicket MCP)
- [ ] All Lab 1 prerequisites
- [ ] Docker Desktop installed and running
- [ ] Lab 1 completed (or MCP basics understood)

---

## 🎓 Skills You'll Gain

| Skill | Lab 1 | Lab 2 |
|-------|-------|-------|
| MCP Server Architecture | ✅ | ✅ |
| Tool Definition (JSON Schema) | ✅ | ✅ |
| Error Handling Patterns | ✅ | ✅ |
| VS Code Integration | ✅ | ✅ |
| Docker Integration | - | ✅ |
| External API Integration | ✅ | ✅ |
| PHP Backend Integration | - | ✅ |
| Production Patterns | ✅ | ✅ |
| Testing MCP Servers | ✅ | ✅ |
| Resources & Prompts | ✅ | ✅ |

---

## 📖 Quick Reference

### MCP Tool Template

```python
Tool(
    name="my_tool",
    description="What this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Description"},
            "param2": {"type": "integer", "default": 10}
        },
        "required": ["param1"]
    }
)
```

### VS Code MCP Configuration

```json
{
    "mcp": {
        "servers": {
            "server-name": {
                "command": "python",
                "args": ["path/to/server.py"],
                "env": {"KEY": "value"}
            }
        }
    }
}
```

### Common Commands

```powershell
# Test MCP server manually
python server.py

# Run MCP test suite
python test.py

# Check Docker containers
docker ps

# View Docker logs
docker logs osTicket-osticket

# Execute PHP in container
docker compose exec osticket php /var/www/html/script.php
```

---

## 🆘 Troubleshooting

### MCP Server Won't Start
```powershell
# Check Python version
python --version

# Check dependencies
pip install mcp httpx

# Check for syntax errors
python -m py_compile server.py
```

### VS Code Doesn't See MCP Server
1. Check `.vscode/settings.json` exists
2. Reload VS Code window
3. Check MCP panel (bottom status bar)

### osTicket Container Issues
```powershell
# Restart containers
docker compose down
docker compose up -d

# Check container logs
docker logs osTicket-osticket

# Verify health
docker compose exec osticket php -v
```

---

## 📝 Assessment Rubric

### Lab 1 Completion
| Criteria | Points |
|----------|--------|
| Hello World Server | 10 |
| Calculator Tools | 15 |
| Task Manager | 20 |
| VS Code Integration | 15 |
| Resources & Prompts | 20 |
| Testing | 10 |
| Final Challenge | 10 |
| **Total** | **100** |

### Lab 2 Completion
| Criteria | Points |
|----------|--------|
| osTicket Setup | 10 |
| Understanding osTicket | 10 |
| PHP Helpers | 20 |
| MCP Server | 25 |
| VS Code Integration | 10 |
| Extensions | 15 |
| Final Project | 10 |
| **Total** | **100** |

---

## 📫 Support

- **Issues**: Check the troubleshooting section
- **Documentation**: See individual lab files
- **MCP Spec**: https://modelcontextprotocol.io

---

**Happy Learning!** 🎉
