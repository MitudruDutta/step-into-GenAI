# 🏢 Leave Management MCP Server

## 📌 Overview

This is a **Model Context Protocol (MCP) server** that provides leave management capabilities to AI applications. Built with **FastMCP**, it demonstrates how to create tools and resources that AI assistants like Claude can use to help manage employee leave requests.

---

## 🎯 What This Server Does

The Leave Management MCP Server exposes the following capabilities:

### Tools (Actions)

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_leave_balance` | Check remaining leave days | `employee_id: str` |
| `apply_leave` | Submit a leave request | `employee_id: str`, `leave_dates: List[str]` |
| `get_leave_history` | View past leave dates | `employee_id: str` |

### Resources (Data)

| Resource | URI Pattern | Description |
|----------|-------------|-------------|
| Greeting | `greeting://{name}` | Personalized welcome message |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  LEAVE MANAGEMENT MCP SERVER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    FastMCP Framework                     │    │
│  │                                                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │    │
│  │  │    TOOLS     │  │  RESOURCES   │  │   PROMPTS    │   │    │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤   │    │
│  │  │ get_balance  │  │ greeting://  │  │   (future)   │   │    │
│  │  │ apply_leave  │  │              │  │              │   │    │
│  │  │ get_history  │  │              │  │              │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    DATA LAYER                            │    │
│  │                                                          │    │
│  │  employee_leaves = {                                     │    │
│  │    "E001": {'balance': 18, 'history': [...]},           │    │
│  │    "E002": {'balance': 20, 'history': []}               │    │
│  │  }                                                       │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mcp-server/
├── main.py              # MCP server implementation
├── pyproject.toml       # Project configuration
├── .python-version      # Python version (3.12)
├── uv.lock              # Dependency lock file
├── README.md            # This file
└── .venv/               # Virtual environment
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager

### Installation

```bash
# Navigate to the mcp-server directory
cd "Agentic AI: Architecture and MCP/mcp-server"

# Install dependencies
uv sync

# Verify installation
uv run python -c "from mcp.server.fastmcp import FastMCP; print('✅ MCP installed')"
```

### Running the Server

```bash
# Run the MCP server
uv run main.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

---

## 🔗 Connecting to Claude Desktop

### Step 1: Locate Configuration File

| OS | Path |
|----|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### Step 2: Add Server Configuration

```json
{
  "mcpServers": {
    "leave-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/Agentic AI: Architecture and MCP/mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

> ⚠️ **Important:** Use the absolute path to the mcp-server directory.

### Step 3: Restart Claude Desktop

Completely quit and restart Claude Desktop for the configuration to take effect.

### Step 4: Verify Connection

1. Open Claude Desktop
2. Look for the MCP tools icon (🔌) in the chat interface
3. Click to see "leave-manager" and its available tools

---

## 🛠️ Tool Reference

### get_leave_balance

Check how many leave days are remaining for an employee.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `employee_id` | string | ✅ | Employee identifier (e.g., "E001") |

**Returns:** String with balance information or error message.

**Example Usage (via Claude):**
> "Check the leave balance for employee E001"

**Example Response:**
> "Employee E001 has 18 leave days remaining."

---

### apply_leave

Submit a leave request for specific dates.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `employee_id` | string | ✅ | Employee identifier |
| `leave_dates` | List[string] | ✅ | Dates in YYYY-MM-DD format |

**Returns:** Confirmation with new balance or error message.

**Example Usage (via Claude):**
> "Apply leave for employee E001 on January 15th and 16th, 2026"

**Example Response:**
> "Leave applied for 2 days. New balance is 16 days."

**Validation:**
- Checks if employee exists
- Prevents duplicate date applications
- Verifies sufficient balance

---

### get_leave_history

View the dates when an employee has taken leave.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `employee_id` | string | ✅ | Employee identifier |

**Returns:** List of leave dates or message indicating no history.

**Example Usage (via Claude):**
> "Show me the leave history for E001"

**Example Response:**
> "Employee E001 has taken leave on: 2025-12-25, 2026-01-01"

---

## 📂 Resource Reference

### greeting://{name}

Returns a personalized greeting message.

**URI Pattern:** `greeting://{name}`

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `name` | string | Name to include in greeting |

**Example:**
- URI: `greeting://John`
- Response: "Hello, John! Welcome to the Leave Management System."

---

## 📊 Sample Data

The server comes with pre-configured sample data:

```python
employee_leaves = {
    "E001": {
        'balance': 18,
        'history': ["2025-12-25", "2026-01-01"]
    },
    "E002": {
        'balance': 20,
        'history': []
    }
}
```

| Employee | Balance | Leave History |
|----------|---------|---------------|
| E001 | 18 days | Dec 25, Jan 1 |
| E002 | 20 days | None |

---

## 🧪 Testing

### Manual Testing

Test the tools directly in Python:

```python
# test_tools.py
from main import get_leave_balance, apply_leave, get_leave_history

# Test balance check
print(get_leave_balance("E001"))
# Output: Employee E001 has 18 leave days remaining.

# Test leave application
print(apply_leave("E001", ["2026-02-01"]))
# Output: Leave applied for 1 days. New balance is 17 days.

# Test history
print(get_leave_history("E001"))
# Output: Employee E001 has taken leave on: 2025-12-25, 2026-01-01, 2026-02-01
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

This opens a web interface for testing MCP interactions.

---

## 🔧 Customization

### Adding New Employees

Modify the `employee_leaves` dictionary in `main.py`:

```python
employee_leaves = {
    "E001": {'balance': 18, 'history': ["2025-12-25", "2026-01-01"]},
    "E002": {'balance': 20, 'history': []},
    "E003": {'balance': 25, 'history': []},  # New employee
}
```

### Adding New Tools

Add a new tool using the `@mcp.tool()` decorator:

```python
@mcp.tool()
def cancel_leave(employee_id: str, date: str) -> str:
    """
    Cancel a previously applied leave.
    
    Args:
        employee_id: The employee identifier
        date: The date to cancel (YYYY-MM-DD format)
    
    Returns:
        Confirmation message or error
    """
    if employee_id not in employee_leaves:
        return f"Employee {employee_id} not found."
    
    if date not in employee_leaves[employee_id]['history']:
        return f"No leave found on {date} for employee {employee_id}."
    
    employee_leaves[employee_id]['history'].remove(date)
    employee_leaves[employee_id]['balance'] += 1
    
    return f"Leave on {date} cancelled. New balance is {employee_leaves[employee_id]['balance']} days."
```

### Adding New Resources

Add a new resource using the `@mcp.resource()` decorator:

```python
@mcp.resource("policy://leave-rules")
def get_leave_policy() -> str:
    """Company leave policy document."""
    return """
    LEAVE POLICY
    ============
    
    1. Annual Leave: 20 days per year
    2. Sick Leave: 10 days per year
    3. Minimum notice: 3 days for planned leave
    4. Maximum consecutive days: 10
    5. Carry forward: Up to 5 days to next year
    """
```

---

## 🐛 Troubleshooting

### Server Not Appearing in Claude

| Issue | Solution |
|-------|----------|
| Config syntax error | Validate JSON format |
| Wrong path | Use absolute path |
| Server not running | Check for Python errors |
| Claude not restarted | Fully quit and restart |

### Tool Calls Failing

| Issue | Solution |
|-------|----------|
| Invalid employee ID | Use existing IDs (E001, E002) |
| Wrong date format | Use YYYY-MM-DD format |
| Insufficient balance | Check balance first |

### Debug Mode

Add logging to troubleshoot:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='mcp_debug.log'
)
```

---

## 📚 Related Documentation

| Document | Description |
|----------|-------------|
| [01-agentic-architecture.md](../docs/01-agentic-architecture.md) | Agent architecture patterns |
| [02-introduction-to-mcp.md](../docs/02-introduction-to-mcp.md) | MCP fundamentals |
| [03-mcp-primitives.md](../docs/03-mcp-primitives.md) | Tools, Resources, Prompts |
| [04-building-mcp-servers.md](../docs/04-building-mcp-servers.md) | Server development guide |
| [05-mcp-integration.md](../docs/05-mcp-integration.md) | Integration patterns |

---

## 📄 License

This project is part of the Step Into GenAI learning repository and is licensed under the MIT License.

---

<div align="center">
  <i>Managing leave, one MCP call at a time 📅</i>
</div>
