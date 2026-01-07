# 🧱 MCP Server Primitives

## 📌 Overview

MCP servers expose capabilities through three fundamental primitives: **Tools**, **Resources**, and **Prompts**. Understanding when and how to use each primitive is essential for building effective MCP servers that provide the right capabilities to AI applications.

This document provides a deep dive into each primitive, including implementation patterns, best practices, and real-world examples.

---

## 🛠️ Tools: Model-Controlled Actions

### What Are Tools?

**Tools** are executable functions that the AI model can decide to invoke. They represent actions the AI can take in the world — from simple calculations to complex API calls.

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOOL ANATOMY                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  NAME: get_leave_balance                                 │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  DESCRIPTION:                                            │    │
│  │  Check how many leave days are left for the employee.    │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  INPUT SCHEMA:                                           │    │
│  │  {                                                       │    │
│  │    "employee_id": {                                      │    │
│  │      "type": "string",                                   │    │
│  │      "description": "Unique employee identifier"         │    │
│  │    }                                                     │    │
│  │  }                                                       │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  OUTPUT: String with leave balance information           │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  SIDE EFFECTS: None (read-only)                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Model-Controlled** | The AI decides when to call the tool based on context |
| **Can Have Side Effects** | Tools can modify state, send data, trigger actions |
| **Requires Input Schema** | JSON Schema defines expected parameters |
| **Returns Content** | Results returned as text, images, or structured data |
| **May Need Approval** | Sensitive tools should require user confirmation |

### Tool Categories

#### Read-Only Tools

Tools that retrieve information without modifying state.

| Example | Description |
|---------|-------------|
| `get_weather(city)` | Fetch current weather |
| `search_database(query)` | Query database records |
| `get_stock_price(symbol)` | Retrieve stock information |
| `get_leave_balance(employee_id)` | Check leave balance |

**Characteristics:**
- Safe to call repeatedly
- No user confirmation typically needed
- Idempotent operations

#### Write Tools

Tools that modify state or trigger external actions.

| Example | Description |
|---------|-------------|
| `send_email(to, subject, body)` | Send an email |
| `create_file(path, content)` | Create a new file |
| `apply_leave(employee_id, dates)` | Submit leave request |
| `update_record(id, data)` | Modify database record |

**Characteristics:**
- Have side effects
- May require user confirmation
- Should be idempotent when possible
- Need careful error handling

#### Destructive Tools

Tools that delete or irreversibly modify data.

| Example | Description |
|---------|-------------|
| `delete_file(path)` | Remove a file |
| `drop_table(name)` | Delete database table |
| `cancel_subscription(id)` | Cancel a service |

**Characteristics:**
- **Always** require user confirmation
- Should have undo mechanisms when possible
- Need extensive logging
- Consider soft-delete patterns

### Tool Implementation Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """
    Check how many leave days are left for the employee.
    
    Args:
        employee_id: The unique identifier for the employee (e.g., "E001")
    
    Returns:
        A message indicating the employee's remaining leave balance
    """
    # Implementation
    data = employee_database.get(employee_id)
    if data:
        return f"Employee {employee_id} has {data['balance']} leave days remaining."
    return f"Employee {employee_id} not found."
```

### Tool Design Best Practices

| Practice | Why It Matters |
|----------|----------------|
| **Clear naming** | AI uses name to understand purpose |
| **Detailed docstring** | AI reads this to decide when to use tool |
| **Type hints** | Enables automatic schema generation |
| **Single responsibility** | One tool, one job |
| **Graceful errors** | Return error messages, don't crash |
| **Idempotency** | Same input should produce same result |

---

## 📂 Resources: Application-Controlled Data

### What Are Resources?

**Resources** are data sources that the application exposes to the AI. Unlike tools, resources are **read-only** and the **application controls** what gets exposed.

```
┌─────────────────────────────────────────────────────────────────┐
│                       RESOURCE ANATOMY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  URI: greeting://{name}                                  │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  NAME: Personalized Greeting                             │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  DESCRIPTION:                                            │    │
│  │  Returns a personalized greeting message for the user    │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  MIME TYPE: text/plain                                   │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  ACCESS: Read-only                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Resource Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Application-Controlled** | Host decides what resources to expose |
| **Read-Only** | Resources cannot be modified through MCP |
| **URI-Based** | Identified by URI (can include templates) |
| **MIME-Typed** | Content type specified for proper handling |
| **Can Be Dynamic** | Content can be generated on request |

### Resource Types

#### Static Resources

Fixed content that doesn't change.

```
┌─────────────────────────────────────────────────────────────────┐
│                     STATIC RESOURCE                              │
├─────────────────────────────────────────────────────────────────┤
│  URI: config://app-settings                                      │
│  Content: Application configuration (fixed)                      │
│  Updates: Only when server restarts                              │
└─────────────────────────────────────────────────────────────────┘
```

**Examples:**
- Configuration files
- Documentation
- Static datasets
- Template files

#### Dynamic Resources

Content generated at request time.

```
┌─────────────────────────────────────────────────────────────────┐
│                     DYNAMIC RESOURCE                             │
├─────────────────────────────────────────────────────────────────┤
│  URI: metrics://system-status                                    │
│  Content: Current system metrics (generated on request)          │
│  Updates: Every request returns fresh data                       │
└─────────────────────────────────────────────────────────────────┘
```

**Examples:**
- System metrics
- Live data feeds
- Database query results
- Computed reports

#### Templated Resources

URIs with parameters that customize the resource.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEMPLATED RESOURCE                            │
├─────────────────────────────────────────────────────────────────┤
│  URI Template: user://{user_id}/profile                          │
│  Example: user://12345/profile                                   │
│  Content: Profile data for specific user                         │
└─────────────────────────────────────────────────────────────────┘
```

**Examples:**
- `file://{path}` — Access specific files
- `user://{id}/profile` — User-specific data
- `report://{date}` — Date-specific reports

### Resource Implementation Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

# Static resource
@mcp.resource("config://settings")
def get_settings() -> str:
    """Application configuration settings."""
    return json.dumps({
        "version": "1.0.0",
        "environment": "production"
    })

# Templated resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Returns a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the Leave Management System."

# Dynamic resource
@mcp.resource("metrics://current")
def get_metrics() -> str:
    """Current system metrics."""
    return json.dumps({
        "timestamp": datetime.now().isoformat(),
        "active_users": get_active_user_count(),
        "requests_per_minute": calculate_rpm()
    })
```

### Resource vs Tool: When to Use Which?

| Scenario | Use Resource | Use Tool |
|----------|--------------|----------|
| Reading configuration | ✅ | |
| Fetching user profile | ✅ | |
| Searching with parameters | | ✅ |
| Modifying data | | ✅ |
| Static documentation | ✅ | |
| Complex queries | | ✅ |
| File contents | ✅ | |
| Sending notifications | | ✅ |

**Rule of Thumb:**
- **Resource** = "Here's some data you can read"
- **Tool** = "Here's an action you can perform"

---

## 📝 Prompts: User-Controlled Templates

### What Are Prompts?

**Prompts** are reusable templates that provide structured context and instructions to the AI. Unlike tools (model-controlled) and resources (application-controlled), prompts are **user-controlled** — the user explicitly chooses to invoke them.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PROMPT ANATOMY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  NAME: leave_request_review                              │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  DESCRIPTION:                                            │    │
│  │  Review and process a leave request with policy checks   │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  ARGUMENTS:                                              │    │
│  │  - employee_id: string (required)                        │    │
│  │  - leave_type: string (optional, default: "annual")      │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  TEMPLATE:                                               │    │
│  │  System: You are an HR assistant reviewing leave...      │    │
│  │  User: Please review leave request for {employee_id}...  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Prompt Characteristics

| Characteristic | Description |
|----------------|-------------|
| **User-Controlled** | User explicitly invokes the prompt |
| **Templated** | Can include dynamic arguments |
| **Structured** | Provides consistent context format |
| **Reusable** | Same prompt can be used repeatedly |
| **Multi-Message** | Can include system, user, and assistant messages |

### Prompt Use Cases

#### Workflow Templates

Standardized workflows for common tasks.

| Prompt | Purpose |
|--------|---------|
| `code_review` | Structured code review process |
| `bug_report` | Consistent bug reporting format |
| `meeting_summary` | Meeting notes template |
| `leave_request` | Leave application workflow |

#### Persona Templates

Different AI personalities for different contexts.

| Prompt | Persona |
|--------|---------|
| `technical_expert` | Deep technical knowledge |
| `friendly_assistant` | Casual, helpful tone |
| `formal_business` | Professional communication |
| `creative_writer` | Imaginative, expressive |

#### Domain-Specific Templates

Specialized prompts for specific domains.

| Prompt | Domain |
|--------|--------|
| `legal_review` | Legal document analysis |
| `medical_summary` | Patient information summary |
| `financial_analysis` | Investment analysis |
| `hr_policy_check` | HR compliance verification |

### Prompt Implementation Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.prompt()
def leave_request_review(employee_id: str, leave_type: str = "annual") -> list:
    """
    Review and process a leave request with policy compliance checks.
    
    Args:
        employee_id: The employee requesting leave
        leave_type: Type of leave (annual, sick, personal)
    """
    return [
        {
            "role": "system",
            "content": """You are an HR assistant specialized in leave management.
            Your role is to:
            1. Check the employee's leave balance
            2. Verify policy compliance
            3. Identify any conflicts with team schedules
            4. Provide a recommendation (approve/deny/discuss)
            
            Be thorough but concise in your analysis."""
        },
        {
            "role": "user",
            "content": f"""Please review the {leave_type} leave request for employee {employee_id}.
            
            Check their current balance, recent leave history, and any policy considerations.
            Provide your recommendation with reasoning."""
        }
    ]
```

### Prompt vs Tool vs Resource

| Aspect | Tool | Resource | Prompt |
|--------|------|----------|--------|
| **Control** | Model | Application | User |
| **Purpose** | Execute action | Provide data | Structure interaction |
| **Invocation** | AI decides | App exposes | User selects |
| **Side Effects** | Possible | None | None |
| **Returns** | Action result | Data content | Message template |

---

## 🔄 Primitives Working Together

### Real-World Example: Leave Management System

Let's see how all three primitives work together in a leave management MCP server:

```
┌─────────────────────────────────────────────────────────────────┐
│              LEAVE MANAGEMENT MCP SERVER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TOOLS (Actions):                                                │
│  ├── get_leave_balance(employee_id)     [Read]                  │
│  ├── apply_leave(employee_id, dates)    [Write]                 │
│  ├── get_leave_history(employee_id)     [Read]                  │
│  └── cancel_leave(employee_id, date)    [Write]                 │
│                                                                  │
│  RESOURCES (Data):                                               │
│  ├── greeting://{name}                  [Personalized welcome]  │
│  ├── policy://leave-rules               [Company leave policy]  │
│  └── calendar://holidays                [Holiday calendar]      │
│                                                                  │
│  PROMPTS (Templates):                                            │
│  ├── leave_request_review               [HR review workflow]    │
│  ├── team_coverage_check                [Coverage analysis]     │
│  └── leave_summary_report               [Monthly reporting]     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Interaction Flow

```
User: "I want to apply for leave next week"

┌─────────────────────────────────────────────────────────────────┐
│                    INTERACTION FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. AI reads RESOURCE: policy://leave-rules                     │
│     → Understands leave policies                                 │
│                                                                  │
│  2. AI calls TOOL: get_leave_balance("E001")                    │
│     → Checks if user has enough days                            │
│                                                                  │
│  3. AI reads RESOURCE: calendar://holidays                      │
│     → Checks for conflicts with holidays                        │
│                                                                  │
│  4. AI calls TOOL: apply_leave("E001", ["2026-01-12", ...])    │
│     → Submits the leave request                                 │
│                                                                  │
│  5. AI responds with confirmation and new balance               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Primitive Selection Guide

### Decision Tree

```
                    ┌─────────────────────┐
                    │ What do you need?   │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Execute an  │     │ Expose data │     │ Structure   │
    │ action?     │     │ for reading?│     │ interaction?│
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │    TOOL     │     │  RESOURCE   │     │   PROMPT    │
    └─────────────┘     └─────────────┘     └─────────────┘
```

### Quick Reference Table

| Need | Primitive | Example |
|------|-----------|---------|
| Search something | Tool | `search_documents(query)` |
| Read a file | Resource | `file://{path}` |
| Send a message | Tool | `send_slack_message(channel, text)` |
| Get configuration | Resource | `config://settings` |
| Structured workflow | Prompt | `code_review` template |
| Modify database | Tool | `update_record(id, data)` |
| Expose API data | Resource | `api://users/{id}` |
| Consistent persona | Prompt | `technical_expert` template |

---

## 🎯 Key Takeaways

1. **Tools are for actions** — Model decides when to call them, can have side effects

2. **Resources are for data** — Application controls exposure, read-only access

3. **Prompts are for structure** — User invokes them, provide consistent templates

4. **Use the right primitive** — Don't use a tool when a resource would suffice

5. **Combine primitives** — Real applications use all three together

6. **Document thoroughly** — AI relies on descriptions to understand capabilities

---

## 📖 Next Steps

→ [04-building-mcp-servers.md](04-building-mcp-servers.md) — Hands-on guide to building your own MCP servers with FastMCP
