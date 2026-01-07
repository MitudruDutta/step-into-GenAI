# 🤝 Coordinator Team Pattern

## 📌 Overview

The **Coordinator Team** pattern is a multi-agent architecture where a central coordinator delegates tasks to specialized agents and synthesizes their responses. This pattern is ideal when a single query requires input from multiple experts working together.

In this example, we build an **E-commerce Support Team** with an FAQ Agent and an Inventory Agent, coordinated to handle complex customer queries.

---

## 🎯 When to Use Coordinator Pattern

| Use Case | Why Coordinator? |
|----------|------------------|
| Complex queries needing multiple skills | Coordinator combines specialist outputs |
| Research + Analysis + Writing tasks | Each agent handles one phase |
| Customer support with multiple concerns | FAQ + Inventory + Shipping agents |
| Report generation | Data + Analysis + Formatting agents |

### Coordinator vs Router

| Aspect | Coordinator | Router |
|--------|-------------|--------|
| **Agents involved** | Multiple (parallel/sequential) | Single (selected) |
| **Response** | Synthesized from all agents | From one agent only |
| **Use case** | Complex, multi-faceted queries | Single-category queries |
| **Example** | "Check stock AND return policy" | "What's your return policy?" |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 E-COMMERCE SUPPORT TEAM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query: "Is iPhone 15 in stock? What's the return policy?" │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │   COORDINATOR    │                         │
│                    │   (Support Team) │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│              ┌──────────────┴──────────────┐                    │
│              ▼                             ▼                    │
│       ┌──────────────┐            ┌──────────────┐              │
│       │  FAQ Agent   │            │  Inventory   │              │
│       │              │            │    Agent     │              │
│       ├──────────────┤            ├──────────────┤              │
│       │ Web Search   │            │ Stock Check  │              │
│       │ (DuckDuckGo) │            │ (Custom Tool)│              │
│       └──────┬───────┘            └──────┬───────┘              │
│              │                           │                       │
│              │  "Return policy is..."    │  "iPhone 15: In stock"│
│              │                           │                       │
│              └───────────┬───────────────┘                       │
│                          ▼                                       │
│                 ┌──────────────────┐                            │
│                 │   SYNTHESIZED    │                            │
│                 │    RESPONSE      │                            │
│                 └──────────────────┘                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Implementation

### Step 1: Define Custom Tools

```python
def check_inventory(product_name: str) -> str:
    """Check the inventory status for a given product.
    
    Args:
        product_name: The name of the product to check.
        
    Returns:
        The inventory status of the product.
    """
    inventory = {
        "iPhone 15": "In stock (Ships in 2 days)",
        "AirPods Pro": "Out of stock (Available in 2 weeks)",
        "MacBook Air M3": "Low stock (Only 3 left!)",
    }
    return inventory.get(product_name, "Product not found in inventory.")
```

**Key Points:**
- Docstring is critical — the LLM reads it to understand when to use the tool
- Return informative messages for all cases
- Simulate real inventory lookup (in production, connect to actual database)

### Step 2: Create Specialized Agents

#### FAQ Agent

```python
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

faq_agent = Agent(
    name="FAQ Agent",
    role="Answer customer questions using web search",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[DuckDuckGoTools()],
    instructions="Answer e-commerce related queries using web search. "
                 "Use Best Buy store if someone is asking about electronics. "
                 "Include source if possible.",
    tool_choice="auto",
    markdown=True,
)
```

**Configuration Breakdown:**

| Parameter | Purpose |
|-----------|---------|
| `name` | Identifier for the agent |
| `role` | Describes agent's responsibility |
| `model` | LLM to use (Qwen 32B via Groq) |
| `tools` | Capabilities (DuckDuckGo search) |
| `instructions` | Behavior guidelines |
| `tool_choice="auto"` | Let LLM decide when to use tools |

#### Inventory Agent

```python
inventory_agent = Agent(
    name="Inventory Agent",
    role="Check inventory for a given product",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[check_inventory],
    instructions="Only respond with inventory status of the product.",
    tool_choice="auto",
    markdown=True,
)
```

**Key Difference:** Uses custom `check_inventory` function instead of web search.

### Step 3: Create Coordinator Team

```python
from agno.team import Team

support_team = Team(
    role="coordinate",
    members=[faq_agent, inventory_agent],
    model=Groq(id="llama-3.1-8b-instant"),
    instructions=["Be polite", "Include product availability and any relevant policies"],
    tool_choice="auto",
    markdown=True,
)
```

**Team Configuration:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `role` | `"coordinate"` | Enables coordinator pattern |
| `members` | List of agents | Agents to coordinate |
| `model` | LLM | For coordination decisions |
| `instructions` | List | Guidelines for synthesis |

### Step 4: Execute Query

```python
support_team.print_response(
    "Is the iPhone 15 in stock? Also, what's your return policy on electronics?",
    stream=True
)
```

---

## 🔄 Execution Flow

```
1. USER QUERY
   "Is the iPhone 15 in stock? Also, what's your return policy?"
                              │
                              ▼
2. COORDINATOR ANALYSIS
   - Identifies two sub-tasks:
     a) Stock check → Inventory Agent
     b) Return policy → FAQ Agent
                              │
                              ▼
3. PARALLEL DELEGATION
   ┌─────────────────────────────────────┐
   │  FAQ Agent          Inventory Agent │
   │  ↓                  ↓               │
   │  Web search         check_inventory │
   │  ↓                  ↓               │
   │  "Return policy..." "In stock..."   │
   └─────────────────────────────────────┘
                              │
                              ▼
4. RESPONSE SYNTHESIS
   Coordinator combines both responses:
   "The iPhone 15 is in stock and ships in 2 days.
    Regarding return policy, Best Buy offers..."
                              │
                              ▼
5. FINAL RESPONSE TO USER
```

---

## 📊 Sample Output

**Query:**
> "Is the iPhone 15 in stock? Also, what's your return policy on electronics?"

**Response:**
```markdown
Great question! Let me help you with both:

**iPhone 15 Availability:**
✅ In stock (Ships in 2 days)

**Return Policy for Electronics:**
Based on Best Buy's policy:
- 15-day return window for most electronics
- Must be in original packaging
- Restocking fee may apply for opened items

Is there anything else I can help you with?
```

---

## 🎯 Best Practices

### 1. Clear Agent Specialization

Each agent should have a **single, well-defined responsibility**:

| ❌ Bad | ✅ Good |
|--------|---------|
| "General Support Agent" | "FAQ Agent", "Inventory Agent", "Shipping Agent" |
| One agent with 10 tools | Multiple agents with 1-2 tools each |

### 2. Descriptive Instructions

```python
# ❌ Vague
instructions="Help the customer"

# ✅ Specific
instructions="Answer e-commerce related queries using web search. "
             "Use Best Buy store for electronics questions. "
             "Include source links when available."
```

### 3. Coordinator Instructions

Guide how the coordinator should synthesize:

```python
instructions=[
    "Be polite and professional",
    "Include product availability information",
    "Mention relevant policies",
    "Provide a cohesive, unified response"
]
```

### 4. Tool Documentation

```python
def check_inventory(product_name: str) -> str:
    """Check the inventory status for a given product.
    
    Args:
        product_name: The name of the product to check.
        
    Returns:
        The inventory status of the product.
    """
```

The docstring is **not optional** — it's how the LLM understands the tool.

---

## ⚠️ Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Agents with overlapping responsibilities | Define clear boundaries |
| Missing tool docstrings | Always document tools thoroughly |
| Coordinator not synthesizing well | Add specific synthesis instructions |
| Too many agents | Start with 2-3, add as needed |

---

## 🎯 Key Takeaways

1. **Coordinator pattern** combines outputs from multiple specialized agents
2. **`role="coordinate"`** enables the coordination behavior in Agno Teams
3. **Specialization** — each agent should excel at one thing
4. **Tool docstrings** are critical for LLM understanding
5. **Instructions guide synthesis** — tell the coordinator how to combine responses

---

## 📖 Next Steps

→ [02-router-team.md](02-router-team.md) — Learn the Router pattern for query classification
