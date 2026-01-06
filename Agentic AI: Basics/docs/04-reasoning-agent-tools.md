# 🔬 Reasoning Agents with Tools

## 📌 Overview

This document explores the most powerful pattern in agentic AI: combining **reasoning capabilities** with **external tools**. This creates agents that can both think systematically AND access real-world data — essentially building an AI analyst that can research, reason, and report.

---

## 🎯 The Power of Combination

### The Limitation of Each Approach Alone

| Approach           | What It Can Do                  | What It Cannot Do                      |
| ------------------ | ------------------------------- | -------------------------------------- |
| **Reasoning Only** | Think deeply, analyze logically | Access current data, verify facts      |
| **Tools Only**     | Fetch real data, call APIs      | Plan what to fetch, synthesize meaning |

### The Synergy

When you combine reasoning with tools, you get:

```
Reasoning + Tools = Complete Analytical Workflow
```

The agent can:

1. **Plan** what information is needed
2. **Fetch** that information using tools
3. **Analyze** the data with systematic reasoning
4. **Synthesize** insights into coherent output

---

## 🧠 How Reasoning-with-Tools Works

### Phase 1: Planning (Reasoning)

Before making any tool calls, the reasoning agent thinks:

> "The user wants a report on NVIDIA. What does a complete stock report need?"
>
> - Current trading price
> - Company fundamentals
> - Analyst sentiment
> - Recent performance context
>
> "Which tools do I have that can provide this?"
>
> - get_current_stock_price → price data
> - get_company_info → fundamentals
> - get_analyst_recommendations → sentiment
>
> "Let me gather this data systematically."

This planning phase ensures the agent doesn't randomly call tools — it strategically selects what's needed.

### Phase 2: Execution (Tools)

The agent executes its plan:

| Tool Call                             | Returns                         |
| ------------------------------------- | ------------------------------- |
| `get_current_stock_price("NVDA")`     | Price, day change, volume       |
| `get_company_info("NVDA")`            | Sector, market cap, description |
| `get_analyst_recommendations("NVDA")` | Buy/hold/sell counts, consensus |

### Phase 3: Synthesis (Reasoning)

With data in hand, the agent reasons again:

> "Now I have all the data. Let me organize it meaningfully."
>
> - Price is $X — compare to historical average
> - Market cap is $Y trillion — context of industry
> - 30 buy ratings, 5 hold, 2 sell — strong bullish sentiment
>
> "What story does this data tell?"
>
> - Strong analyst confidence
> - Premium valuation
> - AI sector leadership
>
> "Let me present this in a clear report format."

---

## 📊 The ReasoningTools Concept

### What ReasoningTools Provide

ReasoningTools are a special category of tools that enhance the agent's thinking process:

| Capability                | Description                                      |
| ------------------------- | ------------------------------------------------ |
| **Structured Thinking**   | Guides the model through systematic analysis     |
| **Step Tracking**         | Records each reasoning step for transparency     |
| **Instruction Injection** | Automatically adds reasoning guidance to prompts |
| **Verification Hooks**    | Enables self-checking of reasoning quality       |

### How They Differ from Data Tools

| Data Tools (YFinance)      | ReasoningTools                      |
| -------------------------- | ----------------------------------- |
| Fetch external information | Enhance internal thinking           |
| Return facts/numbers       | Return structured thought processes |
| Called when data needed    | Called when analysis needed         |
| Output: data               | Output: reasoning chain             |

---

## 🔄 The Complete Execution Flow

### Step-by-Step Breakdown

```
User Query: "Write a comprehensive report on NVIDIA stock"
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    REASONING PHASE 1                        │
│                                                             │
│  "What does a comprehensive report need?"                   │
│  • Current price and trading info                           │
│  • Company profile and fundamentals                         │
│  • Analyst opinions and ratings                             │
│  • Context for interpretation                               │
│                                                             │
│  "I'll need multiple tool calls to gather this."            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      TOOL EXECUTION                         │
│                                                             │
│  → get_current_stock_price("NVDA")                          │
│    ← {price: 875.50, change: +2.3%, volume: 45M}            │
│                                                             │
│  → get_company_info("NVDA")                                 │
│    ← {sector: Technology, marketCap: 2.1T, employees: 30K}  │
│                                                             │
│  → get_analyst_recommendations("NVDA")                      │
│    ← {strongBuy: 25, buy: 10, hold: 5, sell: 2, strongSell: 0} │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    REASONING PHASE 2                        │
│                                                             │
│  "Let me analyze this data:"                                │
│  • Price at $875.50 with +2.3% — positive momentum          │
│  • $2.1T market cap — among largest tech companies          │
│  • 35 buy ratings vs 2 sell — overwhelming bullish sentiment│
│                                                             │
│  "Key insights:"                                            │
│  • Market leader in AI/GPU space                            │
│  • Analyst consensus strongly positive                      │
│  • Premium valuation reflects growth expectations           │
│                                                             │
│  "Now I'll format this into a professional report."         │
└─────────────────────────────────────────────────────────────┘
                           ↓
                 Formatted Markdown Report
```

---

## 🎯 Real-World Analogies

### Understanding the Pattern

| Component           | Human Equivalent                                           |
| ------------------- | ---------------------------------------------------------- |
| **Reasoning Only**  | An analyst with no market access — smart but blind         |
| **Tools Only**      | A Bloomberg terminal with no analyst — data but no insight |
| **Reasoning+Tools** | An analyst with full market access — complete capability   |

### The Research Analyst Model

A reasoning agent with tools behaves like a professional research analyst:

1. **Receives a request** — "Give me your analysis on NVIDIA"
2. **Plans research** — "I need price data, fundamentals, sentiment"
3. **Gathers data** — Pulls from various sources
4. **Analyzes** — Interprets what the data means
5. **Synthesizes** — Creates a coherent narrative
6. **Presents** — Formats into a professional report

---

## 📈 Visibility and Transparency

### Why Visibility Matters

One of the most powerful features of reasoning agents is **transparency**:

| Visibility Level       | What You See                          |
| ---------------------- | ------------------------------------- |
| **Basic**              | Final report only                     |
| **Intermediate steps** | Tool calls and returns                |
| **Full reasoning**     | Complete thought process + tool calls |

### Benefits of Full Visibility

| Benefit               | Explanation                                     |
| --------------------- | ----------------------------------------------- |
| **Debugging**         | See where reasoning went wrong                  |
| **Trust**             | Verify the agent's logic is sound               |
| **Learning**          | Understand how the agent approaches problems    |
| **Quality assurance** | Catch errors before they reach the final output |

### Production vs. Development

| Mode                 | Visibility Setting                  | Purpose               |
| -------------------- | ----------------------------------- | --------------------- |
| **Development**      | Full reasoning + intermediate steps | Debug and understand  |
| **Production**       | Final output only                   | Clean user experience |
| **Audit/Compliance** | Full reasoning (logged)             | Record-keeping        |

---

## 🧩 Designing Effective Prompts

### Report Generation Prompts

The quality of output depends heavily on instructions:

| Instruction Type   | Example                                 | Effect                       |
| ------------------ | --------------------------------------- | ---------------------------- |
| **Format**         | "Use tables to display data"            | Structured, scannable output |
| **Scope**          | "Focus on key metrics only"             | Concise, relevant content    |
| **Audience**       | "Explain for non-technical readers"     | Appropriate complexity       |
| **Output control** | "Only output the report, no other text" | Clean, professional result   |

### Common Prompt Patterns

| Pattern         | When to Use                |
| --------------- | -------------------------- |
| **Comparative** | "Compare X vs Y vs Z"      |
| **Analytical**  | "Analyze the trends in..." |
| **Evaluative**  | "Assess the risk of..."    |
| **Predictive**  | "What might happen if..."  |
| **Explanatory** | "Explain why X occurred"   |

---

## 🔧 Tool Orchestration Patterns

### Sequential Pattern

Tools are called one after another, each building on previous results:

```
Query → Tool 1 → Result 1 → Tool 2 (using Result 1) → Final
```

**Example:** "Get stock price, then calculate if it's overvalued based on P/E"

### Parallel Pattern

Multiple independent tool calls made simultaneously:

```
Query → [Tool 1, Tool 2, Tool 3] → [Result 1, Result 2, Result 3] → Synthesis
```

**Example:** "Get prices for NVDA, AMD, and INTC" — all three calls are independent

### Conditional Pattern

Tool calls depend on previous results:

```
Query → Tool 1 → If Result > X → Tool 2A, Else → Tool 2B
```

**Example:** "Get price. If it's up today, get analyst upgrades. If down, get analyst downgrades."

---

## 📊 Advanced Use Cases

### Multi-Stock Comparison

The agent can orchestrate complex multi-asset analysis:

| Capability                  | How It Works                                  |
| --------------------------- | --------------------------------------------- |
| **Parallel data gathering** | Fetch data for multiple stocks simultaneously |
| **Comparative analysis**    | Reason about differences and similarities     |
| **Ranked recommendations**  | Synthesize into actionable insights           |

### Scenario Analysis

The agent can explore multiple scenarios:

| Scenario Type | Agent Behavior                                       |
| ------------- | ---------------------------------------------------- |
| **Bull case** | Assumes positive developments, analyzes implications |
| **Bear case** | Assumes negative developments, analyzes implications |
| **Base case** | Assumes current trajectory continues                 |

### Historical Context

The agent can add temporal context:

| Context Type              | Value Added                                    |
| ------------------------- | ---------------------------------------------- |
| **Historical comparison** | "Price is X% above 52-week average"            |
| **Trend analysis**        | "Analyst sentiment has improved over 6 months" |
| **Cycle positioning**     | "Company is in growth phase of business cycle" |

---

## 🎯 Key Takeaways

1. **Reasoning + Tools = Complete Analysis Pipeline** — Neither alone is sufficient; together they're powerful
2. **Planning before execution** — Reasoning agents think about what data they need before fetching it
3. **Synthesis after gathering** — Data alone isn't valuable; interpretation creates insight
4. **Visibility is a feature** — Seeing the reasoning builds trust and enables debugging
5. **Prompts shape output** — Clear instructions produce professional results
6. **Tool orchestration patterns** — Sequential, parallel, and conditional patterns serve different needs

---

## 📖 Next Steps

→ [05-multimodal-agent.md](05-multimodal-agent.md) — Learn how agents can process images and generate structured outputs
