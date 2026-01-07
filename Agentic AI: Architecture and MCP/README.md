# 🏗️ Agentic AI: Architecture and MCP

## 📌 Overview

This module explores the **architecture of agentic systems** and the **Model Context Protocol (MCP)** — an open standard that revolutionizes how AI agents interact with external tools, data sources, and services. MCP provides a unified, standardized way to connect AI applications to the world, much like USB-C standardized device connectivity.

---

## 🧱 What is Agentic Architecture?

**Agentic Architecture** refers to the structured design patterns used to build AI systems that can autonomously perceive, reason, plan, and act.

### Core Components

| Layer | Purpose | Components |
|-------|---------|------------|
| **LLM Core** | Natural language understanding and generation | GPT, Claude, Gemini, Llama |
| **Reasoning Engine** | Multi-step logical thinking | Chain-of-thought, Tree-of-thought |
| **Planning Module** | Task breakdown and execution strategy | Goal decomposition, action sequencing |
| **Memory System** | Context across interactions | Short-term, long-term, episodic memory |
| **Tools Interface** | External capabilities | MCP, function calling, APIs |
| **Orchestration** | Execution flow management | State machine, error handling, retries |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTIC SYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   LLM Core   │◄──►│  Reasoning   │◄──►│   Planning   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              Orchestration Layer                     │        │
│  └─────────────────────────────────────────────────────┘        │
│         │                   │                   │                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │    Memory    │    │   Knowledge  │    │    Tools     │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                  │                │
└──────────────────────────────────────────────────│───────────────┘
                                                   ▼
                              ┌─────────────────────────────────┐
                              │     External World (via MCP)    │
                              └─────────────────────────────────┘
```

---

## 🔌 What is MCP?

**Model Context Protocol (MCP)** is an open standard developed by Anthropic that provides a **unified way** for AI applications to connect to external data sources, tools, and services.

### The USB-C Analogy

> **MCP is like USB-C for AI** — just as USB-C provides a universal port for connecting devices, MCP provides a universal protocol for connecting AI models to tools and data sources.

```
Before MCP:                          After MCP:
┌─────────┐                          ┌─────────┐     ┌─────────┐
│   AI    │──► Custom Slack API      │   AI    │────►│   MCP   │──► Any MCP Server
│   App   │──► Custom GitHub API     │   App   │     │ Client  │
│         │──► Custom DB Code        └─────────┘     └─────────┘
└─────────┘
(N integrations = N implementations)  (1 protocol = all integrations)
```

### Why MCP Matters

| Before MCP | With MCP |
|------------|----------|
| Custom integration for each tool | One standard protocol for all |
| Different auth methods per service | Unified authentication |
| Inconsistent data formats | Standardized request/response |
| Tight coupling | Loose coupling via protocol |
| Hard to swap tools | Plug-and-play replacement |

---

## 🛠️ MCP Primitives

MCP servers expose three types of capabilities:

### 1. Tools (Model-Controlled Actions)

Functions the AI can call to perform actions.

```python
@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    # Implementation
```

### 2. Resources (Application-Controlled Data)

Read-only data sources exposed to the AI.

```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Application configuration."""
    return json.dumps({"version": "1.0"})
```

### 3. Prompts (User-Controlled Templates)

Reusable templates for structured interactions.

| Primitive | Control | Purpose | Side Effects |
|-----------|---------|---------|--------------|
| **Tools** | Model | Actions | Yes |
| **Resources** | Application | Data | No |
| **Prompts** | User | Templates | No |

---

## 📚 What You'll Learn

| Topic | Description |
|-------|-------------|
| **Agentic Architecture** | Layered architecture, memory systems, execution patterns |
| **MCP Fundamentals** | Protocol components, USB-C analogy, JSON-RPC |
| **MCP Primitives** | Tools, Resources, Prompts — when to use each |
| **Building MCP Servers** | FastMCP framework, hands-on development |
| **Integration Patterns** | Multi-server setups, security, monitoring |

---

## 🗂️ Module Contents

### 1. 🏗️ Agentic Architecture Patterns

Understanding how modern AI agents are structured and designed.

**Key Concepts:**
- Five-layer architecture model
- Memory systems (short-term, long-term, episodic)
- Execution patterns (sequential, parallel, hierarchical)
- Error handling and safety guardrails

📖 **[Read Full Documentation →](./docs/01-agentic-architecture.md)**

---

### 2. 🔌 Introduction to MCP

Deep dive into the Model Context Protocol — what it is and how it works.

**Key Concepts:**
- The USB-C analogy for AI connectivity
- MCP components (hosts, clients, servers)
- JSON-RPC 2.0 communication protocol
- Connection lifecycle

📖 **[Read Full Documentation →](./docs/02-introduction-to-mcp.md)**

---

### 3. 🧱 MCP Server Primitives

Understanding Tools, Resources, and Prompts — the building blocks of MCP.

**Key Concepts:**
- Tools: executable actions with side effects
- Resources: read-only data access
- Prompts: reusable templates
- When to use each primitive

📖 **[Read Full Documentation →](./docs/03-mcp-primitives.md)**

---

### 4. 🏭 Building MCP Servers

Hands-on guide to creating MCP servers using FastMCP.

**Key Concepts:**
- FastMCP framework setup
- Defining tools with decorators
- Exposing resources with URI templates
- Testing and debugging

📖 **[Read Full Documentation →](./docs/04-building-mcp-servers.md)**

---

### 5. 🔗 MCP Integration Patterns

Connecting MCP servers to hosts and production deployment.

**Key Concepts:**
- Claude Desktop integration
- Multi-server architectures
- Security and authentication
- Monitoring and observability

📖 **[Read Full Documentation →](./docs/05-mcp-integration.md)**

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastMCP (MCP SDK) |
| **Language** | Python 3.12+ |
| **Package Manager** | uv |
| **Protocol** | JSON-RPC 2.0 |
| **Hosts** | Claude Desktop, Cursor, VS Code |

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
cd "Agentic AI: Architecture and MCP/mcp-server"
uv sync
```

### 2. Run the MCP Server

```bash
uv run main.py
```

### 3. Connect to Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "leave-manager": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-server", "run", "main.py"]
    }
  }
}
```

---

## 📂 Project Structure

```
Agentic AI: Architecture and MCP/
├── README.md                          # This file
├── docs/
│   ├── 01-agentic-architecture.md     # Architecture patterns
│   ├── 02-introduction-to-mcp.md      # MCP fundamentals
│   ├── 03-mcp-primitives.md           # Tools, Resources, Prompts
│   ├── 04-building-mcp-servers.md     # Server development guide
│   └── 05-mcp-integration.md          # Integration patterns
└── mcp-server/
    ├── README.md                      # Server documentation
    ├── main.py                        # Leave Management MCP Server
    ├── pyproject.toml                 # Project configuration
    └── .venv/                         # Virtual environment
```

---

## 🎯 Key Takeaways

1. **Layered architecture** enables modular, maintainable agent systems
2. **MCP is USB-C for AI** — one protocol to connect to everything
3. **Three primitives** — Tools (actions), Resources (data), Prompts (templates)
4. **FastMCP simplifies development** — decorators and type hints do the heavy lifting
5. **Security by design** — trust boundaries and user consent built into MCP

---

## 📖 Further Reading

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)

---

## 🔗 Related Modules

| Module | Focus |
|--------|-------|
| [Agentic AI: Basics](../Agentic%20AI%3A%20Basics/) | Agent fundamentals with Agno framework |
| [Gen AI: Foundation](../Gen%20AI%3A%20Foundation/) | LLM internals and tech stack |
| [Gen AI: Vector Database](../Gen%20AI%3A%20Vector%20Database/) | Knowledge storage for agent memory |

---

## ⏭️ Next Steps

After completing this module, you'll be ready to:

- Design scalable agentic architectures
- Build custom MCP servers for any use case
- Integrate MCP servers with Claude Desktop and other hosts
- Implement production-ready security and monitoring
