# 🔗 MCP Integration Patterns

## 📌 Overview

Building an MCP server is just the first step. This document covers **integration patterns** — how to connect MCP servers to hosts, architect multi-server systems, handle security, and build production-ready agentic applications.

Understanding these patterns is essential for building scalable, maintainable, and secure AI-powered systems.

---

## 🏠 MCP Host Integration

### Supported Hosts

MCP is supported by a growing ecosystem of AI applications:

| Host | Type | MCP Support | Notes |
|------|------|-------------|-------|
| **Claude Desktop** | Desktop App | ✅ Full | Reference implementation |
| **Cursor** | Code Editor | ✅ Full | AI-first IDE |
| **Zed** | Code Editor | ✅ Full | Modern, fast editor |
| **VS Code** | Code Editor | 🔄 Extensions | Via community extensions |
| **Continue** | IDE Extension | ✅ Full | Open-source AI assistant |
| **Custom Apps** | Any | ✅ SDK | Build your own host |

### Claude Desktop Integration

#### Configuration Deep Dive

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      },
      "cwd": "/working/directory"
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `command` | ✅ | Executable to run |
| `args` | ❌ | Command-line arguments |
| `env` | ❌ | Environment variables |
| `cwd` | ❌ | Working directory |

#### Common Configuration Patterns

**Python with uv:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/server", "run", "main.py"]
    }
  }
}
```

**Python with venv:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "/path/to/server/.venv/bin/python",
      "args": ["/path/to/server/main.py"]
    }
  }
}
```

**Node.js:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server/index.js"]
    }
  }
}
```

**NPX (for published packages):**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

---

## 🏗️ Multi-Server Architectures

### Pattern 1: Specialized Servers

Each server handles a specific domain.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPECIALIZED SERVERS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌──────────────┐                           │
│                      │  MCP HOST    │                           │
│                      │ (Claude)     │                           │
│                      └──────┬───────┘                           │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   HR        │    │  Finance    │    │   IT        │         │
│  │   Server    │    │   Server    │    │   Server    │         │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤         │
│  │ • Leave     │    │ • Expenses  │    │ • Tickets   │         │
│  │ • Payroll   │    │ • Budgets   │    │ • Assets    │         │
│  │ • Benefits  │    │ • Reports   │    │ • Access    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Clear separation of concerns
- Independent scaling
- Easier maintenance
- Domain-specific expertise

**Configuration:**
```json
{
  "mcpServers": {
    "hr": {
      "command": "uv",
      "args": ["--directory", "/servers/hr", "run", "main.py"]
    },
    "finance": {
      "command": "uv",
      "args": ["--directory", "/servers/finance", "run", "main.py"]
    },
    "it": {
      "command": "uv",
      "args": ["--directory", "/servers/it", "run", "main.py"]
    }
  }
}
```

### Pattern 2: Layered Servers

Servers organized by abstraction level.

```
┌─────────────────────────────────────────────────────────────────┐
│                      LAYERED SERVERS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌──────────────┐                           │
│                      │  MCP HOST    │                           │
│                      └──────┬───────┘                           │
│                             │                                    │
│  ┌──────────────────────────┼──────────────────────────┐        │
│  │                          │                          │        │
│  │    APPLICATION LAYER     │                          │        │
│  │  ┌─────────────┐  ┌─────────────┐                  │        │
│  │  │ Workflow    │  │ Analytics   │                  │        │
│  │  │ Server      │  │ Server      │                  │        │
│  │  └──────┬──────┘  └──────┬──────┘                  │        │
│  │         │                │                          │        │
│  └─────────┼────────────────┼──────────────────────────┘        │
│            │                │                                    │
│  ┌─────────┼────────────────┼──────────────────────────┐        │
│  │         │                │                          │        │
│  │    DATA LAYER            │                          │        │
│  │  ┌──────▼──────┐  ┌──────▼──────┐                  │        │
│  │  │ Database    │  │ File        │                  │        │
│  │  │ Server      │  │ Server      │                  │        │
│  │  └─────────────┘  └─────────────┘                  │        │
│  │                                                     │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Reusable data layer
- Application logic separated from data access
- Easier testing

### Pattern 3: Gateway Server

Single entry point that routes to backend servers.

```
┌─────────────────────────────────────────────────────────────────┐
│                      GATEWAY PATTERN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌──────────────┐                           │
│                      │  MCP HOST    │                           │
│                      └──────┬───────┘                           │
│                             │                                    │
│                      ┌──────▼───────┐                           │
│                      │   GATEWAY    │                           │
│                      │   SERVER     │                           │
│                      │              │                           │
│                      │ • Auth       │                           │
│                      │ • Routing    │                           │
│                      │ • Logging    │                           │
│                      └──────┬───────┘                           │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Backend 1  │    │  Backend 2  │    │  Backend 3  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Centralized authentication
- Unified logging and monitoring
- Simplified host configuration
- Rate limiting at gateway

---

## 🔐 Security Patterns

### Authentication Strategies

#### API Key Authentication

```python
import os
from functools import wraps

API_KEY = os.getenv("MCP_API_KEY")

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In production, validate against request headers
        if not API_KEY:
            raise ValueError("API key not configured")
        return func(*args, **kwargs)
    return wrapper

@mcp.tool()
@require_auth
def sensitive_operation(data: str) -> str:
    """Perform a sensitive operation that requires authentication."""
    # Implementation
    pass
```

#### Environment-Based Secrets

```json
{
  "mcpServers": {
    "secure-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/server", "run", "main.py"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host/db",
        "API_KEY": "secret-key-here",
        "ENCRYPTION_KEY": "encryption-key"
      }
    }
  }
}
```

### Input Validation

Always validate inputs before processing:

```python
import re
import re
from datetime import datetime
from typing import List

def validate_employee_id(employee_id: str) -> bool:
    """Validate employee ID format (E followed by 3 digits)."""
    return bool(re.match(r'^E\d{3}$', employee_id))

def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates."""
    # Validate employee ID
    if not validate_employee_id(employee_id):
        return "Invalid employee ID format. Expected format: E001"
    
    # Validate dates
    invalid_dates = [d for d in leave_dates if not validate_date(d)]
    if invalid_dates:
        return f"Invalid date format for: {', '.join(invalid_dates)}. Use YYYY-MM-DD."
    
    # Proceed with validated inputs
    # ...
```

### Output Sanitization

Prevent sensitive data leakage:

```python
def sanitize_output(data: dict) -> dict:
    """Remove sensitive fields from output."""
    sensitive_fields = ['password', 'ssn', 'credit_card', 'api_key']
    return {k: v for k, v in data.items() if k.lower() not in sensitive_fields}

@mcp.tool()
def get_employee_info(employee_id: str) -> str:
    """Get employee information."""
    data = database.get_employee(employee_id)
    safe_data = sanitize_output(data)
    return json.dumps(safe_data, indent=2)
```

### Rate Limiting

Prevent abuse through rate limiting:

```python
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        now = time()
        # Remove old calls outside window
        self.calls[key] = [t for t in self.calls[key] if now - t < self.window]
        
        if len(self.calls[key]) >= self.max_calls:
            return False
        
        self.calls[key].append(now)
        return True

rate_limiter = RateLimiter(max_calls=100, window_seconds=60)

@mcp.tool()
def rate_limited_operation(data: str) -> str:
    """An operation with rate limiting."""
    if not rate_limiter.is_allowed("global"):
        return "Rate limit exceeded. Please try again later."
    
    # Proceed with operation
    # ...
```

---

## 📊 Monitoring and Observability

### Logging Best Practices

```python
import logging
import json
from datetime import datetime
from time import time

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def log_tool_call(tool_name: str, params: dict, result: str, duration_ms: float):
    """Log tool calls in structured format."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "tool_call",
        "tool": tool_name,
        "params": params,
        "result_length": len(result),
        "duration_ms": duration_ms
    }
    logger.info(json.dumps(log_entry))

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check leave balance."""
    start = time()
    
    # Implementation
    result = f"Employee {employee_id} has 18 days remaining."
    
    duration = (time() - start) * 1000
    log_tool_call("get_leave_balance", {"employee_id": employee_id}, result, duration)
    
    return result
```

### Metrics Collection

```python
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Metrics:
    tool_calls: dict = field(default_factory=lambda: defaultdict(int))
    errors: dict = field(default_factory=lambda: defaultdict(int))
    latencies: dict = field(default_factory=lambda: defaultdict(list))
    
    def record_call(self, tool: str, duration_ms: float, error: bool = False):
        self.tool_calls[tool] += 1
        self.latencies[tool].append(duration_ms)
        if error:
            self.errors[tool] += 1
    
    def get_summary(self) -> dict:
        return {
            "total_calls": sum(self.tool_calls.values()),
            "by_tool": dict(self.tool_calls),
            "errors": dict(self.errors),
            "avg_latency_ms": {
                tool: sum(lats) / len(lats) 
                for tool, lats in self.latencies.items()
            }
        }

metrics = Metrics()

# Expose metrics as a resource
@mcp.resource("metrics://summary")
def get_metrics_summary() -> str:
    """Current server metrics."""
    return json.dumps(metrics.get_summary(), indent=2)
```

---

## 🔄 Error Handling Patterns

### Graceful Degradation

```python
@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    try:
        # Primary source
        return fetch_from_primary_api(city)
    except PrimaryAPIError:
        try:
            # Fallback source
            return fetch_from_backup_api(city)
        except BackupAPIError:
            # Graceful degradation
            return f"Weather service temporarily unavailable. Please try again later."
```

### Retry Logic

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for automatic retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_external_data(url: str) -> dict:
    """Fetch data from external API with retry."""
    import requests  # Ensure requests is installed: pip install requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### Circuit Breaker

```python
from enum import Enum
from time import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        return True  # HALF_OPEN allows one request
    
    def record_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED
    
    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

circuit = CircuitBreaker()

@mcp.tool()
def external_api_call(query: str) -> str:
    """Call external API with circuit breaker protection."""
    if not circuit.can_execute():
        return "Service temporarily unavailable. Circuit breaker is open."
    
    try:
        result = make_api_call(query)
        circuit.record_success()
        return result
    except Exception as e:
        circuit.record_failure()
        return f"API call failed: {e}"
```

---

## 🧪 Testing Strategies

### Unit Testing Tools

```python
import pytest
from main import get_leave_balance, apply_leave, employee_leaves

class TestLeaveManagement:
    def setup_method(self):
        """Reset data before each test."""
        employee_leaves.clear()
        employee_leaves.update({
            "E001": {'balance': 20, 'history': []},
            "E002": {'balance': 5, 'history': ["2026-01-01"]}
        })
    
    def test_get_balance_existing_employee(self):
        result = get_leave_balance("E001")
        assert "20 leave days remaining" in result
    
    def test_get_balance_nonexistent_employee(self):
        result = get_leave_balance("E999")
        assert "not found" in result
    
    def test_apply_leave_success(self):
        result = apply_leave("E001", ["2026-02-01", "2026-02-02"])
        assert "Leave applied for 2 days" in result
        assert employee_leaves["E001"]["balance"] == 18
    
    def test_apply_leave_insufficient_balance(self):
        result = apply_leave("E002", ["2026-02-01", "2026-02-02", "2026-02-03",
                                       "2026-02-04", "2026-02-05", "2026-02-06"])
        assert "Insufficient leave balance" in result
    
    def test_apply_leave_duplicate_dates(self):
        result = apply_leave("E002", ["2026-01-01"])
        assert "already applied" in result
```

### Integration Testing

```python
import subprocess
import json

def test_mcp_server_starts():
    """Test that the MCP server starts without errors."""
    process = subprocess.Popen(
        ["uv", "run", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_request).encode() + b'\n')
    process.stdin.flush()
    
    # Read response
    response = process.stdout.readline()
    result = json.loads(response)
    
    assert "result" in result
    assert "serverInfo" in result["result"]
    
    process.terminate()
```

---

## 🎯 Key Takeaways

1. **Choose the right architecture** — Specialized, layered, or gateway based on your needs

2. **Security is non-negotiable** — Validate inputs, sanitize outputs, implement rate limiting

3. **Monitor everything** — Structured logging and metrics are essential for production

4. **Handle errors gracefully** — Retry, circuit breakers, and graceful degradation

5. **Test thoroughly** — Unit tests for tools, integration tests for the server

6. **Start simple, evolve** — Begin with a single server, add complexity as needed

---

## 📖 Further Reading

- [MCP Official Specification](https://spec.modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

---

<div align="center">
  <i>Building robust connections between AI and the world 🌐</i>
</div>
