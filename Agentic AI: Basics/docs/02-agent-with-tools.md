# 🛠️ Agent with Custom Tools

## 📌 Overview

This document explores **tool creation** — one of the most powerful concepts in agentic AI. We examine how agents can be equipped with both pre-built tools and custom functions, enabling domain-specific capabilities that make agents truly useful for specialized tasks.

---

## 🎯 Why Custom Tools Matter

Pre-built tools like web search are useful, but real-world applications require **domain-specific capabilities**:

| Domain         | Custom Tool Examples                                            |
| -------------- | --------------------------------------------------------------- |
| **Finance**    | Stock lookup, portfolio analysis, risk calculation              |
| **Healthcare** | Patient lookup, drug interaction checker, appointment scheduler |
| **E-commerce** | Inventory check, price comparison, order status                 |
| **Legal**      | Case search, statute lookup, contract analyzer                  |

Without custom tools, agents are generic. With them, agents become **specialists**.

---

## 🧠 How Agents Understand Tools

This is the critical concept most people miss: **the LLM reads tool descriptions to decide when to use them**.

### The Tool Contract

Every tool has an implicit contract with the LLM:

| Component   | What the LLM Needs to Know          |
| ----------- | ----------------------------------- |
| **Name**    | What to call the tool               |
| **Purpose** | When this tool should be used       |
| **Inputs**  | What arguments the tool expects     |
| **Outputs** | What kind of information comes back |

This information is conveyed through **documentation** — specifically, docstrings in Python.

### The Docstring is Not Optional

Consider this critical distinction:

**Tool WITHOUT proper documentation:**

```
Function: get_stock_symbol
Arguments: company_name
```

The LLM sees this and thinks: "I have no idea when to use this or what it returns."

**Tool WITH proper documentation:**

```
Function: get_stock_symbol
Description: Use this function to get the stock symbol for a company.
Arguments: company_name (str) - The name of the company
Returns: str - The stock symbol (e.g., "AAPL" for Apple)
```

The LLM now understands exactly when and how to use this tool.

---

## 🔄 Tool Selection Intelligence

### How the Agent Decides

When a user asks "What is the current stock price of NVIDIA?", the agent's internal reasoning looks like this:

1. **Parse the query**: User wants stock price for NVIDIA
2. **Check available tools**:
   - `get_stock_symbol` — converts company name to ticker
   - `get_current_stock_price` — gets price for a ticker
   - `get_analyst_recommendations` — gets buy/sell ratings
   - `get_company_info` — gets company profile
3. **Determine tool necessity**:
   - Do I know NVIDIA's ticker? → Yes, it's NVDA (common knowledge)
   - Do I need `get_stock_symbol`? → No, skip it
   - Do I need `get_current_stock_price`? → Yes, use it
4. **Execute and respond**

### The "Don't Use Unless Necessary" Pattern

Smart agent design includes **negative instructions** — telling the agent when NOT to use tools:

> "Do not use get_stock_symbol if you can figure out the stock symbol from a company name on your own"

This optimization:

- Reduces unnecessary API calls
- Speeds up response time
- Saves resources

---

## 📊 Tool Types Explained

### Pre-built Tools (YFinance)

Pre-built tools are ready-to-use integrations with external services:

| YFinance Tool                 | What It Provides                           |
| ----------------------------- | ------------------------------------------ |
| `get_current_stock_price`     | Real-time price, day change, volume        |
| `get_analyst_recommendations` | Wall Street ratings (buy/hold/sell counts) |
| `get_company_info`            | Sector, industry, market cap, description  |
| `get_stock_fundamentals`      | P/E ratio, EPS, dividend yield             |
| `get_historical_prices`       | Price history over time                    |

**Advantage:** No implementation needed; just configure and use.

**Limitation:** Fixed functionality; can't customize behavior.

### Custom Tools (Functions)

Custom tools are Python functions you write:

| Advantage                   | Explanation                                         |
| --------------------------- | --------------------------------------------------- |
| **Domain-specific logic**   | Implement business rules unique to your application |
| **Data source integration** | Connect to your databases, APIs, internal systems   |
| **Complete control**        | Define exactly what the tool does and returns       |
| **Composability**           | Build complex capabilities from simple functions    |

**The pattern:** Write a function → Add a docstring → Give it to the agent → Agent uses it when appropriate.

---

## 🎯 Tool Choice Modes

Agents can be configured with different tool selection strategies:

### Auto Mode (Recommended)

The LLM decides when to use tools based on the query.

| Query                          | LLM Decision                     |
| ------------------------------ | -------------------------------- |
| "What's 2+2?"                  | No tools needed, answer directly |
| "What's NVIDIA's stock price?" | Use stock price tool             |
| "Compare NVIDIA and AMD"       | Use multiple tools               |

### Forced Tool Mode

Sometimes you want to guarantee tool usage:

| Mode                                    | Behavior                    |
| --------------------------------------- | --------------------------- |
| `tool_choice="any"`                     | Must use at least one tool  |
| `tool_choice="get_current_stock_price"` | Must use this specific tool |

**Use case:** When you know the tool is always needed, forcing it reduces latency (no decision-making overhead).

### No Tools Mode

Temporarily disable tools:

| Mode                 | Behavior                               |
| -------------------- | -------------------------------------- |
| `tool_choice="none"` | Respond using only the LLM's knowledge |

**Use case:** Testing, comparison, or when you want pure LLM responses.

---

## 🧩 Combining Multiple Tools

The real power emerges when agents orchestrate multiple tools:

### Sequential Tool Use

```
Query: "Get me NVIDIA's stock price and analyst recommendations"

Agent Execution:
1. Call get_current_stock_price("NVDA") → $XXX.XX
2. Call get_analyst_recommendations("NVDA") → {buy: 30, hold: 5, sell: 2}
3. Synthesize both results into response
```

### Conditional Tool Use

```
Query: "What's the stock price of AtliQ?"

Agent Reasoning:
1. "AtliQ" — I don't recognize this ticker
2. Use get_stock_symbol("AtliQ") → "MSFT"
3. Now use get_current_stock_price("MSFT") → $XXX.XX
4. Respond with result
```

### Parallel Tool Use (Advanced)

Some frameworks support calling multiple tools simultaneously:

```
Query: "Compare NVIDIA, AMD, and Intel stock prices"

Parallel Execution:
├── get_current_stock_price("NVDA")
├── get_current_stock_price("AMD")
└── get_current_stock_price("INTC")

Then: Synthesize all results into comparison table
```

---

## 🛠️ Best Practices for Custom Tools

### 1. Single Responsibility

Each tool should do **one thing well**:

| ❌ Bad                       | ✅ Good                                                             |
| ---------------------------- | ------------------------------------------------------------------- |
| `analyze_stock_everything()` | `get_stock_price()`, `get_stock_fundamentals()`, `get_stock_news()` |

Why? The LLM can precisely select what it needs.

### 2. Clear Naming

Tool names should be **self-explanatory**:

| ❌ Bad       | ✅ Good                        |
| ------------ | ------------------------------ |
| `do_thing()` | `calculate_portfolio_risk()`   |
| `helper()`   | `convert_currency()`           |
| `process()`  | `extract_financial_entities()` |

### 3. Comprehensive Docstrings

The docstring is the tool's **user manual for the LLM**:

| Docstring Element | Purpose                               |
| ----------------- | ------------------------------------- |
| **Description**   | When and why to use this tool         |
| **Args**          | What each parameter means and expects |
| **Returns**       | What the tool gives back              |
| **Examples**      | (Optional) Sample usage               |

### 4. Graceful Error Handling

Tools should handle edge cases:

| Scenario             | Good Tool Behavior              |
| -------------------- | ------------------------------- |
| Invalid input        | Return error message, not crash |
| Data not found       | Return "not found" indicator    |
| External API failure | Return error with details       |

---

## 📈 Model Selection for Tool-Heavy Agents

When agents use many tools, model choice matters more:

| Factor                | Small Models (8B)             | Large Models (32B+) |
| --------------------- | ----------------------------- | ------------------- |
| **Tool selection**    | May choose wrong tools        | Better judgment     |
| **Argument accuracy** | May pass wrong arguments      | More precise        |
| **Multi-tool chains** | Struggles with complex chains | Handles well        |
| **Speed**             | Very fast                     | Slower              |
| **Cost**              | Low                           | Higher              |

**Rule of thumb:** More tools = larger model needed.

---

## 🎯 Key Takeaways

1. **Custom tools make agents specialists** — Generic agents are limited; specialized agents are powerful
2. **Docstrings are critical** — The LLM reads them to understand when and how to use tools
3. **Tool choice modes control behavior** — Auto for flexibility, forced for predictability
4. **Single responsibility principle** — One tool, one job
5. **Model size matters for tool orchestration** — Complex tool chains need smarter models

---

## 📖 Next Steps

→ [03-reasoning-agent-basic.md](03-reasoning-agent-basic.md) — Learn about reasoning models that can think through complex problems step-by-step
