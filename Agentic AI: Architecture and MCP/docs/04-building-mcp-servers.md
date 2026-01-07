# 🏭 Building MCP Servers

## 📌 Overview

This document provides a hands-on guide to building your own MCP servers using **FastMCP** — a high-level Python framework that simplifies MCP server development. We'll walk through the complete process from setup to deployment, using a Leave Management System as our example.

By the end of this guide, you'll understand how to create tools, resources, and prompts, and how to connect your server to MCP hosts like Claude Desktop.

---

## 🛠️ Development Environment Setup

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.12+ | Runtime environment |
| uv | Latest | Fast Python package manager |
| Claude Desktop | Latest | MCP host for testing |

### Project Initialization

```bash
# Create project directory
mkdir mcp-server
cd mcp-server

# Initialize with uv
uv init

# Add MCP dependency
uv add mcp

# Verify installation
uv run python -c "from mcp.server.fastmcp import FastMCP; print('MCP installed successfully')"
```

### Project Structure

```
mcp-server/
├── main.py              # MCP server implementation
├── pyproject.toml       # Project configuration
├── .python-version      # Python version specification
├── uv.lock              # Dependency lock file
└── README.md            # Project documentation
```

---

## 🚀 FastMCP Framework

### What is FastMCP?

**FastMCP** is a high-level framework built on top of the MCP SDK that provides:

| Feature | Benefit |
|---------|---------|
| **Decorator-based API** | Define tools/resources with simple decorators |
| **Automatic schema generation** | Type hints become JSON schemas |
| **Built-in validation** | Input validation from type annotations |
| **Simple server lifecycle** | One-line server startup |

### FastMCP vs Raw MCP SDK

| Aspect | Raw MCP SDK | FastMCP |
|--------|-------------|---------|
| **Lines of code** | 50+ for basic server | 10-15 for same functionality |
| **Schema definition** | Manual JSON Schema | Automatic from type hints |
| **Learning curve** | Steep | Gentle |
| **Flexibility** | Maximum | Slightly constrained |
| **Best for** | Complex custom servers | Most use cases |

---

## 📝 Building the Leave Management Server

Let's build a complete MCP server for managing employee leave requests.

### Step 1: Basic Server Setup

```python
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with a name
mcp = FastMCP("LeaveManager")

if __name__ == "__main__":
    mcp.run()
```

**What's happening:**
1. Import FastMCP from the MCP SDK
2. Create a server instance with a descriptive name
3. Start the server with `mcp.run()`

### Step 2: Define Data Storage

For this example, we'll use an in-memory dictionary. In production, you'd connect to a real database.

```python
from mcp.server.fastmcp import FastMCP
from typing import List

# In-memory employee leave data
employee_leaves = {
    "E001": {'balance': 18, 'history': ["2025-12-25", "2026-01-01"]},
    "E002": {'balance': 20, 'history': []}
}

mcp = FastMCP("LeaveManager")
```

**Data Structure:**
- `employee_id` → Key for lookup
- `balance` → Remaining leave days
- `history` → List of dates when leave was taken

### Step 3: Implement Tools

#### Tool 1: Get Leave Balance (Read-Only)

```python
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """
    Check how many leave days are left for the employee.
    
    Args:
        employee_id: The unique identifier for the employee (e.g., "E001")
    
    Returns:
        A message indicating the employee's remaining leave balance,
        or an error message if the employee is not found.
    """
    data = employee_leaves.get(employee_id)
    if data:
        return f"Employee {employee_id} has {data['balance']} leave days remaining."
    return f"Employee {employee_id} not found."
```

**Key Points:**
- `@mcp.tool()` decorator registers the function as an MCP tool
- Type hints (`str`) enable automatic schema generation
- Docstring is **critical** — AI reads this to understand when to use the tool
- Return informative messages for both success and failure cases

#### Tool 2: Apply Leave (Write Operation)

```python
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates.
    
    Args:
        employee_id: The unique identifier for the employee
        leave_dates: List of dates to apply leave for (format: ['2025-12-25', '2025-12-26'])
    
    Returns:
        Confirmation message with new balance, or error message if request fails.
    
    Example:
        apply_leave("E001", ["2026-01-15", "2026-01-16"])
    """
    # Validate employee exists
    if employee_id not in employee_leaves:
        return f"Employee {employee_id} not found."
    
    # Check for duplicate dates
    existing_history = employee_leaves[employee_id]['history']
    duplicates = [d for d in leave_dates if d in existing_history]
    if duplicates:
        return f"Error: Leave already applied for dates: {', '.join(duplicates)}"
    
    # Check balance
    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]['balance']
    
    if available_balance < requested_days:
        return f"Insufficient leave balance. You have {available_balance} days left."
    
    # Apply leave
    employee_leaves[employee_id]['balance'] -= requested_days
    employee_leaves[employee_id]['history'].extend(leave_dates)
    
    return f"Leave applied for {requested_days} days. New balance is {employee_leaves[employee_id]['balance']} days."
```

**Key Points:**
- Uses `List[str]` type hint for array parameter
- Includes validation logic (duplicates, balance check)
- Returns clear error messages for each failure case
- Updates state only after all validations pass

#### Tool 3: Get Leave History (Read-Only)

```python
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """
    Get the leave history of the employee.
    
    Args:
        employee_id: The unique identifier for the employee
    
    Returns:
        List of dates when the employee has taken leave,
        or a message indicating no history exists.
    """
    data = employee_leaves.get(employee_id)
    if data:
        history = data['history']
        if history:
            return f"Employee {employee_id} has taken leave on: {', '.join(history)}"
        else:
            return f"Employee {employee_id} has no leave history."
    return f"Employee {employee_id} not found."
```

### Step 4: Implement Resources

```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Returns a personalized greeting for the Leave Management System.
    
    Args:
        name: The name of the person to greet
    """
    return f"Hello, {name}! Welcome to the Leave Management System."
```

**Key Points:**
- `@mcp.resource()` decorator with URI template
- `{name}` in URI becomes a function parameter
- Resources are read-only — no side effects

### Step 5: Complete Server Code

```python
from mcp.server.fastmcp import FastMCP
from typing import List

# Data storage
employee_leaves = {
    "E001": {'balance': 18, 'history': ["2025-12-25", "2026-01-01"]},
    "E002": {'balance': 20, 'history': []}
}

# Initialize server
mcp = FastMCP("LeaveManager")


@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee."""
    data = employee_leaves.get(employee_id)
    if data:
        return f"Employee {employee_id} has {data['balance']} leave days remaining."
    return f"Employee {employee_id} not found."


@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates for example ['2025-12-25', '2025-12-26']."""
    if employee_id not in employee_leaves:
        return f"Employee {employee_id} not found."

    existing_history = employee_leaves[employee_id]['history']
    duplicates = [d for d in leave_dates if d in existing_history]
    if duplicates:
        return f"Error: Leave already applied for dates: {', '.join(duplicates)}"

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]['balance']

    if available_balance < requested_days:
        return f"Insufficient leave balance. You have {available_balance} days left."

    employee_leaves[employee_id]['balance'] -= requested_days
    employee_leaves[employee_id]['history'].extend(leave_dates)

    return f"Leave applied for {requested_days} days. New balance is {employee_leaves[employee_id]['balance']} days."


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get the leave history of the employee."""
    data = employee_leaves.get(employee_id)
    if data:
        history = data['history']
        if history:
            return f"Employee {employee_id} has taken leave on: {', '.join(history)}"
        else:
            return f"Employee {employee_id} has no leave history."
    return f"Employee {employee_id} not found."


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Returns a personalized greeting for the Leave Management System."""
    return f"Hello, {name}! Welcome to the Leave Management System."


if __name__ == "__main__":
    mcp.run()
```

---

## 🔧 Running and Testing

### Running the Server Standalone

```bash
# Navigate to server directory
cd mcp-server

# Run with uv
uv run main.py
```

The server will start and wait for MCP protocol messages on stdin/stdout.

### Testing with MCP Inspector

MCP provides an inspector tool for testing servers:

```bash
# Install MCP CLI tools
npx @modelcontextprotocol/inspector uv run main.py
```

This opens a web interface where you can:
- View available tools and resources
- Test tool calls with different parameters
- Inspect request/response messages

---

## 🔗 Connecting to Claude Desktop

### Configuration File Location

| OS | Path |
|----|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### Configuration Format

```json
{
  "mcpServers": {
    "leave-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Configuration Fields:**

| Field | Description |
|-------|-------------|
| `mcpServers` | Object containing all MCP server configurations |
| `leave-manager` | Unique identifier for this server |
| `command` | Executable to run (uv, python, node, etc.) |
| `args` | Command-line arguments |

### Multiple Servers

You can configure multiple MCP servers:

```json
{
  "mcpServers": {
    "leave-manager": {
      "command": "uv",
      "args": ["--directory", "/path/to/leave-server", "run", "main.py"]
    },
    "file-system": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Verifying Connection

After configuring:

1. Restart Claude Desktop completely
2. Look for the MCP icon (🔌) in the chat interface
3. Click to see connected servers and available tools
4. Test by asking Claude to use your tools

---

## 🐛 Debugging Tips

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Server not appearing | Config syntax error | Validate JSON format |
| Tools not working | Path incorrect | Use absolute paths |
| Permission denied | File permissions | Check executable permissions |
| Server crashes | Python error | Check server logs |

### Enabling Debug Logging

Add logging to your server:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='mcp_server.log'
)

logger = logging.getLogger(__name__)

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee."""
    logger.debug(f"get_leave_balance called with employee_id: {employee_id}")
    # ... rest of implementation
```

### Testing Without Claude

Create a test script:

```python
# test_server.py
from main import get_leave_balance, apply_leave, get_leave_history

# Test get_leave_balance
print(get_leave_balance("E001"))
print(get_leave_balance("E999"))  # Non-existent

# Test apply_leave
print(apply_leave("E001", ["2026-02-01"]))
print(apply_leave("E001", ["2026-02-01"]))  # Duplicate

# Test get_leave_history
print(get_leave_history("E001"))
```

---

## 📦 Production Considerations

### Database Integration

Replace in-memory storage with a real database:

```python
import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "leave_management.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database schema."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                balance INTEGER NOT NULL,
                history TEXT NOT NULL
            )
        """)
        conn.commit()

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee."""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT balance FROM employees WHERE id = ?",
            (employee_id,)
        )
        row = cursor.fetchone()
        if row:
            return f"Employee {employee_id} has {row[0]} leave days remaining."
        return f"Employee {employee_id} not found."

# Call init_db at startup
if __name__ == "__main__":
    init_db()
    mcp.run()
```

### Error Handling

Implement robust error handling:

```python
import sqlite3
from datetime import datetime
from typing import List

@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates."""
    try:
        # Validate date format
        for date in leave_dates:
            datetime.strptime(date, "%Y-%m-%d")
        
        # Business logic...
        
    except ValueError as e:
        return f"Invalid date format. Please use YYYY-MM-DD format. Error: {e}"
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return "A system error occurred. Please try again later."
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return "An unexpected error occurred."
```

### Environment Variables

Use environment variables for configuration.

> **Note:** This example uses `python-dotenv` which is optional. Install it with `uv add python-dotenv` or `pip install python-dotenv` if you want to use `.env` files.

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///leave.db")
API_KEY = os.getenv("API_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## 🎯 Key Takeaways

1. **FastMCP simplifies development** — Decorators and type hints do the heavy lifting

2. **Docstrings are critical** — AI uses them to understand tool purpose

3. **Type hints enable schemas** — Automatic JSON Schema generation from Python types

4. **Test before connecting** — Use MCP Inspector and unit tests

5. **Use absolute paths** — Relative paths cause configuration issues

6. **Handle errors gracefully** — Return informative messages, don't crash

---

## 📖 Next Steps

→ [05-mcp-integration.md](05-mcp-integration.md) — Learn advanced integration patterns and multi-server architectures
