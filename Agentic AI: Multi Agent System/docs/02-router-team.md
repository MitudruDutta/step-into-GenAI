# 🔀 Router Team Pattern

## 📌 Overview

The **Router Team** pattern is a multi-agent architecture where a router analyzes incoming queries and directs them to the single most appropriate specialized agent. Unlike the coordinator pattern (which combines multiple agents), the router selects **one expert** to handle each query.

In this example, we build a **Customer Care Chatbot** with Technical, Sales, and General Inquiry agents, with a router that classifies and routes queries.

---

## 🎯 When to Use Router Pattern

| Use Case | Why Router? |
|----------|-------------|
| Customer support with distinct categories | Tech vs Sales vs Billing |
| FAQ systems | Route to topic-specific handlers |
| Helpdesk ticketing | Classify and assign to right team |
| Intent-based chatbots | Different intents → different handlers |

### Router vs Coordinator

| Aspect | Router | Coordinator |
|--------|--------|-------------|
| **Agents involved** | ONE (selected) | Multiple (all relevant) |
| **Response source** | Single agent | Synthesized from many |
| **Query type** | Single-category | Multi-faceted |
| **Example** | "How do I reset password?" | "Reset password AND check bill" |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 CUSTOMER CARE CHATBOT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query: "Do you have any ongoing discounts?"               │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │     ROUTER       │                         │
│                    │ (Query Analyzer) │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│                    Analyzes: "discounts" → Sales                │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              │              │              │                    │
│              ▼              ▼              ▼                    │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │   Tech   │   │  Sales   │   │ General  │               │
│       │  Agent   │   │  Agent   │   │  Agent   │               │
│       │          │   │    ✓     │   │          │               │
│       └──────────┘   └────┬─────┘   └──────────┘               │
│                           │                                      │
│                           ▼                                      │
│              "Yes! We're offering 20% off..."                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Implementation

### Step 1: Define Specialized Tools

#### Technical Support Tool

```python
def technical_support(query: str) -> str:
    """Handle technical support queries.
    
    Args:
        query: The technical support question or issue description.
        
    Returns:
        A helpful response to the technical issue.
    """
    responses = {
        "app crash": "Please try reinstalling the app and update your OS.",
        "login issue": "Try resetting your password using the 'Forgot Password' link.",
        "freezing": "Clear the app cache and restart your device.",
    }
    for keyword, response in responses.items():
        if keyword in query.lower():
            return response
    return "Please provide more details about the technical issue."
```

#### Sales Support Tool

```python
def sales_support(query: str) -> str:
    """Handle sales and pricing queries.
    
    Args:
        query: The sales or pricing question.
        
    Returns:
        Information about pricing, discounts, or sales.
    """
    responses = {
        "cost": "Our premium plan costs $49.99/month with 24/7 support.",
        "discount": "Yes! We are offering 20% off for new users this week.",
        "pricing": "We have Basic, Pro, and Premium plans starting at $9.99/month.",
    }
    for keyword, response in responses.items():
        if keyword in query.lower():
            return response
    return "Let me connect you to a sales representative for more details."
```

#### General Info Tool

```python
def general_info(query: str) -> str:
    """Handle general information queries.
    
    Args:
        query: The general information question.
        
    Returns:
        General information about business hours, location, or contact details.
    """
    responses = {
        "hours": "We are open from 9 AM to 6 PM, Monday to Friday.",
        "location": "Our headquarters are located in San Francisco, CA.",
        "contact": "You can contact us at support@example.com or call 1800-123-456.",
    }
    for keyword, response in responses.items():
        if keyword in query.lower():
            return response
    return "Can you clarify your question? I'm here to help."
```

### Step 2: Create Specialized Agents

```python
from agno.agent import Agent
from agno.models.groq import Groq

# Technical Support Agent
tech_agent = Agent(
    name="Tech Support Agent",
    role="Handle technical issues",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[technical_support],
    instructions="Use the technical support tool to answer user queries. "
                 "Keep responses helpful and simple. "
                 "Provide direct answer, do not ask further questions. "
                 "Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)

# Sales Agent
sales_agent = Agent(
    name="Sales Agent",
    role="Handle pricing and sales questions",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[sales_support],
    instructions="Use the sales tool to answer pricing and discount-related questions. "
                 "Provide direct answer, do not ask further questions. "
                 "Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)

# General Inquiry Agent
general_agent = Agent(
    name="General Inquiry Agent",
    role="Answer general questions like hours, location, and contact info",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[general_info],
    instructions="Use the general info tool to help with common inquiries. "
                 "Provide direct answer, do not ask further questions. "
                 "Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)
```

### Step 3: Create Router Team

```python
from agno.team import Team

router_team = Team(
    name="Customer Care Chatbot Agent",
    role="route",
    members=[tech_agent, sales_agent, general_agent],
    model=Groq(id="llama-3.1-8b-instant"),
    instructions="Route the query to the correct agent based on whether "
                 "it's technical, sales, or general.",
    tool_choice="auto",
    markdown=True,
    show_members_responses=True,
)
```

**Key Configuration:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `role` | `"route"` | Enables router pattern |
| `members` | List of agents | Available routing targets |
| `instructions` | Routing logic | How to classify queries |
| `show_members_responses` | `True` | Show which agent responded |

### Step 4: Execute Queries

```python
# Technical query
router_team.print_response(
    "My app keeps freezing whenever I try to open settings.",
    stream=True
)

# Sales query
router_team.print_response(
    "Do you have any ongoing discounts on the premium plan?",
    stream=True
)

# General query
router_team.print_response(
    "What are your business hours on weekdays?",
    stream=True
)
```

---

## 🔄 Routing Logic

### How the Router Decides

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROUTING DECISION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query: "My app keeps freezing"                                 │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  ROUTER ANALYSIS │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│  ┌──────────────────────────┼──────────────────────────┐        │
│  │                          │                          │        │
│  │  Check agent roles:      │                          │        │
│  │                          │                          │        │
│  │  Tech Agent:             │  Sales Agent:            │        │
│  │  "Handle technical       │  "Handle pricing and     │        │
│  │   issues"                │   sales questions"       │        │
│  │  Keywords: crash,        │  Keywords: cost,         │        │
│  │  freezing, login         │  discount, pricing       │        │
│  │       ✓ MATCH            │       ✗ NO MATCH         │        │
│  │                          │                          │        │
│  └──────────────────────────┴──────────────────────────┘        │
│                             │                                    │
│                             ▼                                    │
│                    Route to: Tech Agent                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Query Classification Examples

| Query | Classification | Routed To |
|-------|----------------|-----------|
| "My app keeps crashing" | Technical | Tech Agent |
| "How much does premium cost?" | Sales | Sales Agent |
| "What are your business hours?" | General | General Agent |
| "Can't login to my account" | Technical | Tech Agent |
| "Any discounts available?" | Sales | Sales Agent |
| "Where is your office?" | General | General Agent |

---

## 📊 Sample Output

**Query 1: Technical**
```
Input: "My app keeps freezing whenever I try to open settings."

[Tech Support Agent]: Clear the app cache and restart your device.
```

**Query 2: Sales**
```
Input: "Do you have any ongoing discounts on the premium plan?"

[Sales Agent]: Yes! We are offering 20% off for new users this week.
```

**Query 3: General**
```
Input: "What are your business hours on weekdays?"

[General Inquiry Agent]: We are open from 9 AM to 6 PM, Monday to Friday.
```

---

## 🎯 Best Practices

### 1. Clear Role Definitions

Each agent's `role` should be distinct and non-overlapping:

```python
# ✅ Good - Clear boundaries
tech_agent = Agent(role="Handle technical issues")
sales_agent = Agent(role="Handle pricing and sales questions")
general_agent = Agent(role="Answer general questions like hours, location")

# ❌ Bad - Overlapping
agent1 = Agent(role="Help customers")
agent2 = Agent(role="Assist users")
```

### 2. Routing Instructions

Be explicit about classification criteria:

```python
# ✅ Good
instructions="Route to Tech Agent for crashes, errors, login issues. "
             "Route to Sales Agent for pricing, discounts, plans. "
             "Route to General Agent for hours, location, contact."

# ❌ Bad
instructions="Route to the right agent."
```

### 3. Concise Agent Responses

For router pattern, agents should give direct answers:

```python
instructions="Provide direct answer, do not ask further questions. "
             "Provide short answer in less than two lines."
```

### 4. Fallback Handling

Handle unclassifiable queries:

```python
def general_info(query: str) -> str:
    # ... keyword matching ...
    return "Can you clarify your question? I'm here to help."  # Fallback
```

---

## 🔄 Router vs Coordinator: Decision Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    PATTERN SELECTION GUIDE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query: "Check my order status"                                 │
│  → Single concern → ROUTER (to Order Agent)                     │
│                                                                  │
│  Query: "Check order status AND apply discount code"            │
│  → Multiple concerns → COORDINATOR (Order + Sales Agents)       │
│                                                                  │
│  Query: "What's your return policy?"                            │
│  → Single concern → ROUTER (to Policy Agent)                    │
│                                                                  │
│  Query: "Return policy AND current stock of iPhone"             │
│  → Multiple concerns → COORDINATOR (Policy + Inventory Agents)  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Question | Router | Coordinator |
|----------|--------|-------------|
| Single topic query? | ✅ | |
| Multiple topics in one query? | | ✅ |
| Need ONE expert answer? | ✅ | |
| Need combined expertise? | | ✅ |
| Customer support categories? | ✅ | |
| Complex research tasks? | | ✅ |

---

## ⚠️ Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Ambiguous routing | Add more specific role descriptions |
| Wrong agent selected | Improve routing instructions |
| Agents asking follow-up questions | Add "provide direct answer" instruction |
| Overlapping agent responsibilities | Define clear boundaries |

---

## 🎯 Key Takeaways

1. **Router pattern** selects ONE agent per query
2. **`role="route"`** enables routing behavior in Agno Teams
3. **Clear role definitions** are critical for accurate routing
4. **Non-overlapping responsibilities** prevent routing confusion
5. **Direct responses** — router agents should answer immediately

---

## 📖 Next Steps

→ [03-multi-agent-architecture.md](03-multi-agent-architecture.md) — Deep dive into multi-agent architecture patterns
