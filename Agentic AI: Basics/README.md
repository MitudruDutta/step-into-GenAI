# 🤖 Agentic AI: Basics

## 📌 Overview

This module provides hands-on exploration of **Agentic AI** — AI systems that go beyond simple content generation to autonomously plan, reason, and execute multi-step tasks. Using the **Agno** framework, we build agents that can search the web, analyze financial data, leverage reasoning capabilities, and process multimodal inputs.

---

## 🎯 What is Agency in AI?

**Agency in AI** is the ability of any AI system to:

- 🔍 **Detect its environment** — perceive and understand context
- 🛠️ **Access tools** — interact with external systems and APIs
- ⚡ **Perform independent actions** — make decisions and execute tasks autonomously

Through agency, AI applications can be classified into two broad categories:

| Category      | Description                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| **Workflows** | Built using LLMs but have **no agency** — fixed, predefined execution paths    |
| **Agents**    | Use LLMs along with **tools, knowledge, and memory** with some level of agency |

---

## 🧠 Reasoning Models

**Reasoning models** are advanced LLMs designed to perform **multi-step logical thinking**, not just pattern matching.

### Key Characteristics

| Aspect                         | Description                                                               |
| ------------------------------ | ------------------------------------------------------------------------- |
| **Specialized Training**       | Use reasoning tokens to break down complex problems into manageable steps |
| **Mathematical Logic**         | Excel at tasks involving calculations and logical deductions              |
| **Planning**                   | Can create and execute multi-step plans                                   |
| **Structured Problem Solving** | Approach problems systematically rather than reactively                   |
| **Interpretable Outputs**      | Generate more accurate, traceable, and explainable results                |

### Ideal Use Cases

- 💻 Coding assistants requiring step-by-step problem decomposition
- 📚 Tutoring systems that explain concepts progressively
- 📊 Decision support tools needing transparent reasoning chains

---

## 📚 What You'll Learn

| Topic                    | Description                                                |
| ------------------------ | ---------------------------------------------------------- |
| **Basic Agents**         | Creating simple agents with web search capabilities        |
| **Tool Integration**     | Equipping agents with custom tools and external APIs       |
| **Reasoning Agents**     | Leveraging reasoning models for complex problem-solving    |
| **Reasoning with Tools** | Combining reasoning capabilities with external tool access |
| **Multimodal Agents**    | Processing images and generating structured outputs        |

---

## 🗂️ Module Contents

### 1. 🚀 Basic Agent with Web Search

A foundational agent using Groq's Llama model with DuckDuckGo search capabilities.

**Key Concepts:**

- Agent initialization with the Agno framework
- Model configuration (Groq + Llama 3.1)
- Tool integration (DuckDuckGo web search)
- Markdown-formatted responses

📖 **[Read Full Documentation →](./docs/01-basic-agent.md)**

---

### 2. 🛠️ Agent with Custom Tools

A finance-focused agent demonstrating custom tool creation and multi-tool integration.

**Key Concepts:**

- Custom Python functions as agent tools
- YFinance integration for stock market data
- Tool choice configuration (`auto` mode)
- Combining built-in and custom tools

📖 **[Read Full Documentation →](./docs/02-agent-with-tools.md)**

---

### 3. 🧠 Reasoning Agent (Basic)

An agent leveraging reasoning capabilities for complex analytical tasks.

**Key Concepts:**

- Enabling reasoning mode in agents
- Using Gemini 2.5 Flash for reasoning
- Streaming responses for real-time output
- Handling complex multi-step problems

📖 **[Read Full Documentation →](./docs/03-reasoning-agent-basic.md)**

---

### 4. 🔬 Reasoning Agent with Tools

An advanced agent combining reasoning capabilities with external tool access for comprehensive analysis.

**Key Concepts:**

- ReasoningTools integration
- Combining reasoning with YFinance data
- Full reasoning chain visualization
- Streaming intermediate reasoning steps

📖 **[Read Full Documentation →](./docs/04-reasoning-agent-tools.md)**

---

### 5. 🖼️ Multimodal Agent (Image Categorization)

An agent that processes images and generates structured JSON outputs with tool-assisted categorization.

**Key Concepts:**

- Image input processing
- Structured JSON output generation
- Custom categorization tools
- Multi-image batch processing

📖 **[Read Full Documentation →](./docs/05-multimodal-agent.md)**

---

## 🛠️ Tech Stack

| Component     | Technology                            |
| ------------- | ------------------------------------- |
| **Framework** | Agno (Agent Framework)                |
| **Models**    | Groq (Llama 3.1, Qwen), Google Gemini |
| **Tools**     | DuckDuckGo, YFinance, Custom          |
| **Language**  | Python 3.10+                          |

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install agno python-dotenv
```

### 2. Configure Environment

Create a `.env` file with your API keys:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 3. Run Your First Agent

```bash
cd "Agentic AI: Basics/agents"
python basic_agent.py
```

---

## 📂 Project Structure

```
Agentic AI: Basics/
├── README.md
├── agents/
│   ├── basic_agent.py         # Simple agent with web search
│   ├── agent_with_tools.py    # Finance agent with custom tools
│   ├── agent_reasoning_1.py   # Basic reasoning agent
│   ├── agent_reasoning_2.py   # Reasoning agent with tools
│   ├── categorize.py          # Multimodal image categorization
│   └── Images/                # Sample images for categorization
└── docs/
    ├── 01-basic-agent.md
    ├── 02-agent-with-tools.md
    ├── 03-reasoning-agent-basic.md
    ├── 04-reasoning-agent-tools.md
    └── 05-multimodal-agent.md
```

---

## 🎯 Key Takeaways

1. **Agency** transforms static LLM applications into dynamic, autonomous systems
2. **Tools** extend agent capabilities beyond text generation to real-world interactions
3. **Reasoning models** enable systematic, multi-step problem solving
4. **Multimodal capabilities** allow agents to process and understand diverse input types
5. The **Agno framework** provides a clean abstraction for building production-ready agents

---

## 📖 Further Reading

- [Introduction to Agentic AI](../Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/06-agentic-ai.md)
- [Agno Framework Documentation](https://docs.agno.com)
- [Groq API Documentation](https://console.groq.com/docs)
- [Google Gemini Documentation](https://ai.google.dev/docs)
