# 🚀 Basic Agent with Web Search

## 📌 Overview

This document explains the fundamentals of **AI agents** — systems that combine language models with external tools to perform tasks autonomously. We explore how a simple news reporter agent works and the core concepts that make it possible.

---

## 🎯 What is an AI Agent?

An **AI agent** is fundamentally different from a simple chatbot or LLM call. While a basic LLM responds to prompts with generated text, an agent can:

| Capability     | Description                                                           |
| -------------- | --------------------------------------------------------------------- |
| **Perceive**   | Understand the user's request and identify what information is needed |
| **Decide**     | Autonomously choose which tools to use and in what order              |
| **Act**        | Execute tool calls to gather real-world information                   |
| **Synthesize** | Combine gathered information into a coherent, useful response         |

This is the core distinction: **agents act, they don't just respond**.

---

## 🧠 The Agent Formula

Every agent, no matter how simple or complex, follows the same fundamental formula:

```
Agent = LLM + Tools + Instructions
```

### The LLM (Brain)

The language model serves as the agent's brain. It:

- Interprets user requests
- Decides when and which tools to use
- Processes tool outputs
- Generates final responses

**In our example:** We use Llama 3.1 8B via Groq — a fast, efficient model ideal for straightforward tasks.

### Tools (Capabilities)

Tools are functions the agent can call to interact with the world. Without tools, an agent is just a chatbot.

**In our example:** DuckDuckGo search allows the agent to access current web information.

### Instructions (Personality)

Instructions define how the agent behaves, its tone, and its approach to tasks.

**In our example:** "You are an enthusiastic news reporter with a flair for storytelling."

---

## 🔄 How the Agent Thinks

When you ask the agent "Tell me the latest news about India", here's what happens internally:

### Step 1: Request Analysis

The LLM analyzes your query and determines:

- **What is being asked?** → Latest news about India
- **What information do I need?** → Current news articles
- **Do I have this information?** → No, my training data is outdated
- **What tool can help?** → Web search

### Step 2: Tool Selection

The agent doesn't blindly call tools. It **reasons** about which tool is appropriate:

| Tool Available    | Relevance to Query | Decision   |
| ----------------- | ------------------ | ---------- |
| DuckDuckGo Search | High               | **Use it** |
| Calculator        | None               | Skip       |
| Code Executor     | None               | Skip       |

### Step 3: Tool Execution

The agent formulates a search query and executes the DuckDuckGo tool. This happens programmatically — the agent doesn't browse the web like a human; it calls an API.

### Step 4: Response Synthesis

The agent receives raw search results (titles, snippets, URLs) and must:

1. **Filter** — Remove irrelevant results
2. **Organize** — Group related stories
3. **Summarize** — Extract key information
4. **Format** — Present in readable Markdown with source links

---

## 🎭 The Role of Instructions

Instructions are more important than they appear. They fundamentally shape agent behavior:

### Without Instructions

```
Query: "Tell me about the economy"
Response: "The economy is a system of production, distribution, and consumption of goods and services. [Generic, textbook response]"
```

### With "News Reporter" Instructions

```
Query: "Tell me about the economy"
Response: "Breaking news! Markets are showing significant movement today as [current, engaging, story-driven response with sources]"
```

The same LLM, the same tools, but completely different output because of instructions.

---

## 🛠️ Understanding the Tool Layer

### What Tools Actually Are

Tools are **interfaces** between the agent and external systems. They're not magic — they're structured function calls with:

| Component        | Purpose                                       |
| ---------------- | --------------------------------------------- |
| **Name**         | How the LLM identifies the tool               |
| **Description**  | What the LLM reads to understand tool purpose |
| **Parameters**   | What inputs the tool expects                  |
| **Return Value** | What information comes back                   |

### DuckDuckGo Tools Explained

The DuckDuckGo tool provides:

| Capability      | What It Does                                               |
| --------------- | ---------------------------------------------------------- |
| **Web Search**  | Searches the general web, returns titles + snippets + URLs |
| **News Search** | Focuses on news sources, returns recent articles           |

**Key advantage:** No API key required. DuckDuckGo's public interface is used.

**Key limitation:** Results are limited compared to Google; some queries may return sparse data.

---

## ⚡ Why Groq + Llama 3.1?

### The Speed Factor

Groq is a hardware company that builds specialized chips for LLM inference. Their infrastructure delivers:

| Metric                  | Groq Performance | Typical Cloud LLM |
| ----------------------- | ---------------- | ----------------- |
| **Tokens/second**       | 100-500+         | 20-50             |
| **Time to first token** | ~100ms           | 500ms-2s          |
| **Latency**             | Sub-second       | 2-10 seconds      |

For agents, speed matters enormously. Each tool call requires the LLM to process results and decide next steps. Slow models create frustrating user experiences.

### Why 8B Parameters?

Model size is a trade-off:

| Model Size | Pros                                     | Cons                      |
| ---------- | ---------------------------------------- | ------------------------- |
| **8B**     | Fast, cheap, sufficient for simple tasks | Limited reasoning depth   |
| **70B**    | Strong reasoning, better quality         | Slower, more expensive    |
| **400B+**  | State-of-the-art performance             | Very slow, very expensive |

For a news search agent, 8B is optimal. The task doesn't require deep reasoning — it requires speed and coherent synthesis.

---

## 🔍 Agent Decision-Making Deep Dive

### How Does the LLM Know to Use Tools?

When you configure an agent with tools, the framework does several things:

1. **Tool descriptions are injected into the system prompt** — The LLM "sees" what tools are available
2. **Special formatting is used** — Tools are described in a structured way the LLM understands
3. **The LLM is trained to recognize tool patterns** — Modern LLMs are fine-tuned to output tool calls in specific formats

### The Tool Call Format

Internally, when the LLM decides to use a tool, it outputs something like:

```
<tool_call>
  name: duckduckgo_search
  arguments: {"query": "latest news India January 2026"}
</tool_call>
```

The agent framework intercepts this, executes the actual search, and feeds results back to the LLM.

---

## 📊 Agent vs. Simple LLM Call

| Aspect           | Simple LLM Call                 | Agent                              |
| ---------------- | ------------------------------- | ---------------------------------- |
| **Knowledge**    | Limited to training data        | Can access live information        |
| **Capabilities** | Text generation only            | Can search, calculate, code, etc.  |
| **Accuracy**     | May hallucinate facts           | Grounds responses in real data     |
| **Complexity**   | Single prompt → single response | Multi-step reasoning and action    |
| **Use Case**     | Creative writing, simple Q&A    | Research, analysis, task execution |

---

## 🎯 Key Takeaways

1. **Agents are LLMs with agency** — They can perceive, decide, and act, not just respond
2. **Tools are the key differentiator** — Without tools, there's no agency
3. **Instructions shape personality** — The same agent can behave completely differently with different instructions
4. **Speed matters for agents** — Slow LLMs create poor agent experiences
5. **Choose model size wisely** — Bigger isn't always better; match the model to the task

---

## 📖 Next Steps

→ [02-agent-with-tools.md](02-agent-with-tools.md) — Learn how to create custom tools and combine multiple tool types
