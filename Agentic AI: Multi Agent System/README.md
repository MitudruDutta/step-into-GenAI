# 🤝 Agentic AI: Multi Agent System

## 📌 Overview

This module explores **Multi-Agent Systems (MAS)** — architectures where multiple specialized AI agents collaborate to solve complex problems. Instead of one monolithic agent trying to do everything, multi-agent systems divide responsibilities among specialized agents that work together as a team.

Using the **Agno** framework, we build agent teams that can coordinate, route queries, and collaborate to handle diverse tasks like customer support, research, and complex workflows.

---

## 🎯 What is a Multi-Agent System?

A **Multi-Agent System** is an architecture where multiple autonomous agents interact and collaborate to achieve goals that would be difficult for a single agent.

### Single Agent vs Multi-Agent

| Aspect | Single Agent | Multi-Agent System |
|--------|--------------|-------------------|
| **Complexity** | Handles everything | Divides responsibilities |
| **Specialization** | Jack of all trades | Expert specialists |
| **Scalability** | Limited | Highly scalable |
| **Maintainability** | Monolithic | Modular |
| **Failure Handling** | Single point of failure | Graceful degradation |

### Why Multi-Agent?

```
Single Agent Approach:
┌─────────────────────────────────────────┐
│           SUPER AGENT                    │
│  • Technical support                     │
│  • Sales queries                         │
│  • Inventory checks                      │
│  • Policy questions                      │
│  • General inquiries                     │
│  (Overwhelmed, inconsistent quality)     │
└─────────────────────────────────────────┘

Multi-Agent Approach:
┌─────────────────────────────────────────┐
│              COORDINATOR                 │
└────────────────────┬────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│  Tech   │   │  Sales  │   │ General │
│  Agent  │   │  Agent  │   │  Agent  │
│(Expert) │   │(Expert) │   │(Expert) │
└─────────┘   └─────────┘   └─────────┘
```

---

## 🏗️ Multi-Agent Patterns

### Pattern 1: Coordinator Pattern

A central coordinator delegates tasks to specialized agents.

```
┌─────────────────────────────────────────────────────────────────┐
│                    COORDINATOR PATTERN                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────────┐                         │
│                    │   COORDINATOR    │                         │
│                    │   (Team Lead)    │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              ▼              ▼              ▼                    │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │ Agent A  │   │ Agent B  │   │ Agent C  │               │
│       │(Research)│   │(Analysis)│   │(Writing) │               │
│       └──────────┘   └──────────┘   └──────────┘               │
│                                                                  │
│  Flow: User → Coordinator → Delegates → Agents → Coordinator    │
│        → Synthesized Response → User                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Use Case:** Complex tasks requiring multiple skills (research + analysis + writing)

### Pattern 2: Router Pattern

A router directs queries to the most appropriate agent.

```
┌─────────────────────────────────────────────────────────────────┐
│                      ROUTER PATTERN                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────────┐                         │
│                    │     ROUTER       │                         │
│                    │ (Query Analyzer) │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              ▼              ▼              ▼                    │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│       │  Tech    │   │  Sales   │   │ General  │               │
│       │  Agent   │   │  Agent   │   │  Agent   │               │
│       └──────────┘   └──────────┘   └──────────┘               │
│                                                                  │
│  Flow: User → Router → (Selects ONE agent) → Response → User    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Use Case:** Customer support with distinct query categories

### Pattern 3: Pipeline Pattern

Agents process sequentially, each adding value.

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE PATTERN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │ Agent 1  │──►│ Agent 2  │──►│ Agent 3  │──►│ Agent 4  │     │
│  │(Extract) │   │(Analyze) │   │(Validate)│   │(Format)  │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│                                                                  │
│  Flow: Input → A1 → A2 → A3 → A4 → Output                       │
│  Each agent transforms/enriches the data                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Use Case:** Document processing, data transformation pipelines

### Pattern 4: Debate Pattern

Agents argue different perspectives, then synthesize.

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEBATE PATTERN                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│       ┌──────────┐           ┌──────────┐                       │
│       │ Agent A  │◄─────────►│ Agent B  │                       │
│       │  (Pro)   │  Debate   │  (Con)   │                       │
│       └────┬─────┘           └────┬─────┘                       │
│            │                      │                              │
│            └──────────┬───────────┘                              │
│                       ▼                                          │
│              ┌──────────────┐                                   │
│              │    JUDGE     │                                   │
│              │ (Synthesize) │                                   │
│              └──────────────┘                                   │
│                                                                  │
│  Flow: Question → Both agents argue → Judge synthesizes         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Use Case:** Decision making, balanced analysis, fact-checking

---

## 📚 What You'll Learn

| Topic | Description |
|-------|-------------|
| **Multi-Agent Fundamentals** | Why and when to use multiple agents |
| **Coordinator Teams** | Building teams that collaborate on complex tasks |
| **Router Teams** | Query routing to specialized agents |
| **Agent Communication** | How agents share context and results |
| **Team Orchestration** | Managing agent interactions with Agno |

---

## 🗂️ Module Contents

### 1. 🤝 Coordinator Team (E-commerce Support)

A multi-agent team where a coordinator delegates to specialized agents.

**Key Concepts:**
- Team coordination with `role="coordinate"`
- Combining FAQ and Inventory agents
- Parallel agent execution
- Response synthesis

📖 **[Read Full Documentation →](./docs/01-coordinator-team.md)**

---

### 2. 🔀 Router Team (Customer Care Chatbot)

A router that directs queries to the most appropriate specialized agent.

**Key Concepts:**
- Query routing with `role="route"`
- Technical, Sales, and General agents
- Automatic query classification
- Single-agent response selection

📖 **[Read Full Documentation →](./docs/02-router-team.md)**

---

### 3. 🏗️ Multi-Agent Architecture

Deep dive into designing and scaling multi-agent systems.

**Key Concepts:**
- Architecture patterns comparison
- Agent communication strategies
- Error handling in multi-agent systems
- Scaling considerations

📖 **[Read Full Documentation →](./docs/03-multi-agent-architecture.md)**

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Agno (Agent Framework) |
| **Models** | Groq (Qwen 32B) |
| **Tools** | DuckDuckGo, Custom Functions |
| **Language** | Python 3.10+ |

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install agno python-dotenv
```

### 2. Configure Environment

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

### 3. Run Coordinator Team

```bash
cd "Agentic AI: Multi Agent System/agents"
python multi_agents_agno.py
```

### 4. Run Router Team

```bash
python router_agent.py
```

---

## 📂 Project Structure

```
Agentic AI: Multi Agent System/
├── README.md                      # This file
├── docs/
│   ├── 01-coordinator-team.md     # Coordinator pattern docs
│   ├── 02-router-team.md          # Router pattern docs
│   └── 03-multi-agent-architecture.md  # Architecture deep dive
└── agents/
    ├── multi_agents_agno.py       # Coordinator team example
    └── router_agent.py            # Router team example
```

---

## 🎯 Key Takeaways

1. **Divide and conquer** — Split complex tasks among specialized agents
2. **Coordinator pattern** — Use when tasks need multiple agents collaborating
3. **Router pattern** — Use when queries need to go to ONE specific expert
4. **Specialization wins** — Focused agents outperform generalist agents
5. **Agno Teams** — Simple abstraction for multi-agent orchestration

---

## 📖 Further Reading

- [Agentic AI: Basics](../Agentic%20AI%3A%20Basics/) — Single agent fundamentals
- [Agno Documentation](https://docs.agno.com)
- [Multi-Agent Systems Research](https://arxiv.org/abs/2308.08155)

---

## 🔗 Related Modules

| Module | Focus |
|--------|-------|
| [Agentic AI: Basics](../Agentic%20AI%3A%20Basics/) | Single agent fundamentals |
| [Agentic AI: Architecture and MCP](../Agentic%20AI%3A%20Architecture%20and%20MCP/) | Agent architecture patterns |

---

## ⏭️ Next Steps

After completing this module, you'll be ready to:

- Design multi-agent architectures for complex workflows
- Choose between coordinator and router patterns
- Build scalable customer support systems
- Implement agent specialization strategies
