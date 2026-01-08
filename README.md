# 🤖 Step Into Generative AI

A structured, hands-on learning repository for mastering Generative AI fundamentals. From understanding LLMs to building RAG applications, this project provides comprehensive documentation and practical implementations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What You'll Learn

| Module                                       | Topics                                                                       | Difficulty         |
| -------------------------------------------- | ---------------------------------------------------------------------------- | ------------------ |
| Introduction to Generative AI and Agentic AI | GenAI fundamentals, Text/Image/Audio/Video models, Agentic AI                | ⭐ Beginner        |
| Gen AI: Foundation                           | LLM internals, Model parameters, Vector DBs & RAG, Tech stack, App lifecycle | ⭐⭐ Intermediate  |
| Gen AI: Vector Database                      | Vector DBs, Embeddings, Similarity metrics, ChromaDB, CRUD, Filtering        | ⭐⭐ Intermediate  |
| Agentic AI: Basics                           | AI Agents, Tools, Reasoning models, Multimodal agents, Agno framework        | ⭐⭐ Intermediate  |
| Agentic AI: Architecture and MCP             | Agent architecture, MCP protocol, Building MCP servers, Integration patterns | ⭐⭐⭐ Advanced    |
| Agentic AI: Multi Agent System               | Multi-agent patterns, Coordinator teams, Router teams, Agent communication   | ⭐⭐⭐ Advanced    |
| Agentic AI: Evaluation                       | Functional, Safety, Operational evaluation, Metrics, Guardrails              | ⭐⭐⭐ Advanced    |
| Fine Tuning                                  | Quantization (int8, NF4), LoRA, QLoRA, Unsloth, Model export                 | ⭐⭐⭐ Advanced    |
| Ethics in Gen AI                             | Bias, Privacy, Hallucinations, Safety, IP, Environment, Governance           | ⭐⭐⭐ Advanced    |

---

## 📁 Repository Structure

```
step-into-GenAI/
│
├── 🧠 Introduction to Generative AI and Agentic AI/
│   ├── README.md                      # Module index
│   └── docs/
│       ├── 01-what-is-generative-ai.md    # GenAI fundamentals, modalities
│       ├── 02-text-models-llms.md         # GPT, Claude, Gemini, Llama
│       ├── 03-image-models.md             # DALL-E, Stable Diffusion, Midjourney
│       ├── 04-audio-models.md             # MusicLM, ElevenLabs, Suno
│       ├── 05-video-models.md             # Sora, Runway, Pika
│       └── 06-agentic-ai.md               # Autonomous agents, tool use
│
├── 🔬 Gen AI: Foundation/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-how-llms-work.md            # Transformers, autoregressive models
│   │   ├── 02-model-parameters-sampling.md # Temperature, Top-k, Top-p
│   │   ├── 03-vector-databases-rag.md     # Embeddings, RAG, grounding
│   │   ├── 04-genai-tech-stack.md         # LangChain, HuggingFace, platforms
│   │   └── 05-app-development-lifecycle.md # Build, deploy, monitor
│   └── notebooks/
│       └── key_params.ipynb           # 📓 LLM parameter exploration
│
├── 💾 Gen AI: Vector Database/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-what-is-vector-database.md  # Vector DB fundamentals, embeddings
│   │   ├── 02-similarity-metrics.md       # Euclidean, Cosine, Dot product
│   │   ├── 03-popular-vector-databases.md # ChromaDB, Pinecone, Milvus, Qdrant
│   │   ├── 04-chromadb-basics.md          # Getting started with ChromaDB
│   │   ├── 05-crud-operations.md          # Create, Read, Update, Delete
│   │   └── 06-metadata-filtering.md       # Advanced querying & filtering
│   └── notebooks/
│       ├── 1_chromadb_basics.ipynb        # 📓 ChromaDB fundamentals
│       ├── 2_add_update_delete.ipynb      # 📓 CRUD operations
│       └── 3_metadata_filtering.ipynb     # 📓 Advanced filtering
│
├── 🤖 Agentic AI: Basics/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-basic-agent.md              # Agent fundamentals, LLM + Tools
│   │   ├── 02-agent-with-tools.md         # Custom tools, docstrings, YFinance
│   │   ├── 03-reasoning-agent-basic.md    # Reasoning models, chain-of-thought
│   │   ├── 04-reasoning-agent-tools.md    # Reasoning + tools combination
│   │   └── 05-multimodal-agent.md         # Image processing, structured output
│   └── agents/
│       ├── basic_agent.py                 # Basic web search agent
│       ├── agent_with_tools.py            # Finance agent with tools
│       ├── agent_reasoning_1.py           # Basic reasoning agent
│       ├── agent_reasoning_2.py           # Reasoning with tools
│       └── categorize.py                  # Multimodal image categorization
│
├── 🏗️ Agentic AI: Architecture and MCP/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-agentic-architecture.md     # Layered architecture, memory systems
│   │   ├── 02-introduction-to-mcp.md      # MCP fundamentals, USB-C analogy
│   │   ├── 03-mcp-primitives.md           # Tools, Resources, Prompts
│   │   ├── 04-building-mcp-servers.md     # FastMCP, server development
│   │   └── 05-mcp-integration.md          # Integration patterns, security
│   └── mcp-server/
│       ├── README.md                      # MCP server documentation
│       ├── main.py                        # Leave Management MCP Server
│       └── pyproject.toml                 # Project configuration
│
├── 🤝 Agentic AI: Multi Agent System/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-coordinator-team.md         # Coordinator pattern, parallel agents
│   │   ├── 02-router-team.md              # Router pattern, query classification
│   │   └── 03-multi-agent-architecture.md # Architecture patterns, scaling
│   └── agents/
│       ├── multi_agents_agno.py           # Coordinator team example
│       └── router_agent.py                # Router team example
│
├── 🧪 Agentic AI: Evaluation/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-functional-evaluation.md    # Accuracy, metrics, LLM-as-judge
│   │   ├── 02-safety-evaluation.md        # Jailbreaks, guardrails, hallucinations
│   │   └── 03-operational-evaluation.md   # Performance, monitoring, logging
│   └── agents/
│       ├── inventory_agent.py             # Sample agent for evaluation
│       ├── agent_eval.py                  # Accuracy evaluation example
│       └── perf_eval.py                   # Performance evaluation example
│
├── 🔧 Fine Tuning/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-quantization-basics.md      # int8 and NF4 quantization
│   │   └── 02-finetuning-with-unsloth.md  # LoRA, QLoRA, Unsloth workflow
│   └── notebooks/
│       ├── quantization_basics.ipynb      # 📓 Quantization implementation
│       └── unsloth_finetuning.ipynb       # 📓 Fine-tuning Llama with Unsloth
│
├── ⚖️ Ethics in Gen AI/
│   ├── README.md                      # Module index
│   ├── docs/
│   │   ├── 01-bias-and-fairness.md        # Bias types, detection, mitigation
│   │   ├── 02-privacy-and-data-protection.md # PII, GDPR, differential privacy
│   │   ├── 03-hallucinations-and-misinformation.md # RAG, fact-checking
│   │   ├── 04-transparency-and-explainability.md # Model cards, XAI
│   │   ├── 05-content-moderation-and-safety.md # Guardrails, jailbreaks
│   │   ├── 06-intellectual-property-and-copyright.md # Fair use, licensing
│   │   ├── 07-environmental-impact-and-sustainability.md # Carbon footprint
│   │   └── 08-responsible-deployment-and-governance.md # Risk assessment
│   ├── biases/
│   │   ├── bias.py                        # Bias detection implementation
│   │   └── llm_helper.py                  # LLM helper utilities
│   ├── PII/
│   │   └── pii_and_privacy.ipynb          # 📓 PII detection and privacy
│   └── hallucination and misinformation/
│       ├── README.md                      # Setup and usage guide
│       ├── airline_chatbot.py             # RAG-based airline chatbot
│       ├── airline_faq.csv                # FAQ dataset (see README)
│       ├── ingest_data.py                 # Data ingestion for vector DB
│       ├── similarity_checker.py          # Check output similarity
│       ├── test_adversarial.py            # Adversarial testing
│       ├── test_functional.py             # Functional testing
│       └── test_files/
│           ├── test_adversarial.csv       # Adversarial test cases
│           └── test_functional.csv        # Functional test cases
│
└── README.md                          # You are here
```

---

## 🛤️ Learning Path

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODULE 1: INTRODUCTION TO GENAI                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ What is      │   │ Text Models  │   │ Image, Audio │   │ Agentic AI  │  │
│  │ GenAI?       │──►│ (LLMs)       │──►│ Video Models │──►│ (Agents)    │  │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘  │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODULE 2: GEN AI FOUNDATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ How LLMs     │   │ Model        │   │ Vector DBs   │   │ Tech Stack  │  │
│  │ Work         │──►│ Parameters   │──►│ & RAG        │──►│ & Lifecycle │  │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘  │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODULE 3: VECTOR DATABASES                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ What is a    │   │ Similarity   │   │ ChromaDB     │   │ CRUD &      │  │
│  │ Vector DB?   │──►│ Metrics      │──►│ Basics       │──►│ Filtering   │  │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘  │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quick Start

1. **New to GenAI?** → Start with `Introduction to Generative AI and Agentic AI/docs/01-what-is-generative-ai.md`
2. **Know the basics?** → Jump to `Gen AI: Foundation/docs/01-how-llms-work.md`
3. **Ready to build?** → Go to `Gen AI: Foundation/docs/04-genai-tech-stack.md`
4. **Learning Vector DBs?** → Start with `Gen AI: Vector Database/docs/01-what-is-vector-database.md`
5. **Building Agents?** → Go to `Agentic AI: Basics/docs/01-basic-agent.md`
6. **Learning MCP?** → Go to `Agentic AI: Architecture and MCP/docs/02-introduction-to-mcp.md`

---

## 📓 Notebooks Overview

| Notebook                                                       | Module          | What You'll Learn                                       |
| -------------------------------------------------------------- | --------------- | ------------------------------------------------------- |
| `Gen AI: Foundation/notebooks/key_params.ipynb`                | Foundation      | Explore temperature, top-k, top-p effects on LLM output |
| `Gen AI: Vector Database/notebooks/1_chromadb_basics.ipynb`    | Vector Database | ChromaDB setup, collections, basic queries              |
| `Gen AI: Vector Database/notebooks/2_add_update_delete.ipynb`  | Vector Database | CRUD operations in ChromaDB                             |
| `Gen AI: Vector Database/notebooks/3_metadata_filtering.ipynb` | Vector Database | Advanced filtering and querying                         |
| `Fine Tuning/notebooks/quantization_basics.ipynb`              | Fine Tuning     | int8 and NF4 quantization implementation                |
| `Fine Tuning/notebooks/unsloth_finetuning.ipynb`               | Fine Tuning     | Fine-tuning Llama 3.2 with Unsloth and LoRA             |
| `Ethics in Gen AI/PII/pii_and_privacy.ipynb`                   | Ethics          | PII detection and privacy-preserving techniques         |

---

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- OpenAI API key (optional, for API examples)
- CUDA-capable GPU (optional, for local models)

### Installation

```bash
# Clone the repository
git clone https://github.com/MitudruDutta/step-into-GenAI.git
cd step-into-GenAI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Core Dependencies

| Package              | Purpose                          |
| -------------------- | -------------------------------- |
| streamlit            | Web app framework                |
| langchain-groq       | Groq LLM integration             |
| langchain-core       | LangChain core components        |
| pydantic             | Data validation                  |
| agno                 | Agentic AI framework             |
| chromadb             | Vector database                  |
| sentence-transformers| Embedding models                 |
| mcp                  | Model Context Protocol           |
| python-dotenv        | Environment variables            |
| pandas               | Data manipulation                |

### MCP Server Setup (Optional)

For the MCP server examples, you'll need `uv` package manager:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to MCP server
cd "Agentic AI: Architecture and MCP/mcp-server"

# Install and run
uv sync
uv run main.py
```

### Verify Installation

```python
import langchain
import openai
print(f"LangChain: {langchain.__version__}")
print(f"OpenAI: {openai.__version__}")
```

---

## 📚 Module Details

### 1. Introduction to Generative AI and Agentic AI

Foundational concepts for understanding Generative AI:

| Document                                                                                                                 | Description                                             |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| [01-what-is-generative-ai.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/01-what-is-generative-ai.md) | GenAI fundamentals, modalities, GenAI vs Traditional AI |
| [02-text-models-llms.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/02-text-models-llms.md)           | GPT-4, Claude, Gemini, Llama, BERT                      |
| [03-image-models.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/03-image-models.md)                   | DALL-E, Stable Diffusion, Midjourney                    |
| [04-audio-models.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/04-audio-models.md)                   | MusicLM, ElevenLabs, Suno, voice synthesis              |
| [05-video-models.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/05-video-models.md)                   | Sora, Runway, Pika, temporal consistency                |
| [06-agentic-ai.md](Introduction%20to%20Generative%20AI%20and%20Agentic%20AI/docs/06-agentic-ai.md)                       | Autonomous agents, tool use, multi-step workflows       |

### 2. Gen AI: Foundation

Technical deep-dive into how GenAI systems work:

| Document                                                                                         | Description                                             |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| [01-how-llms-work.md](Gen%20AI%3A%20Foundation/docs/01-how-llms-work.md)                         | Transformers, autoregressive generation, training costs |
| [02-model-parameters-sampling.md](Gen%20AI%3A%20Foundation/docs/02-model-parameters-sampling.md) | Temperature, Top-k, Top-p, context windows              |
| [03-vector-databases-rag.md](Gen%20AI%3A%20Foundation/docs/03-vector-databases-rag.md)           | Embeddings, ANN algorithms, RAG architecture            |
| [04-genai-tech-stack.md](Gen%20AI%3A%20Foundation/docs/04-genai-tech-stack.md)                   | LangChain, HuggingFace, cloud platforms                 |
| [05-app-development-lifecycle.md](Gen%20AI%3A%20Foundation/docs/05-app-development-lifecycle.md) | Evaluation, deployment, monitoring                      |
| [key_params.ipynb](Gen%20AI%3A%20Foundation/notebooks/key_params.ipynb)                          | 📓 Interactive LLM parameter exploration                |

### 3. Gen AI: Vector Database

Comprehensive guide to vector databases for AI applications:

| Document                                                                                              | Description                                         |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [01-what-is-vector-database.md](Gen%20AI%3A%20Vector%20Database/docs/01-what-is-vector-database.md)   | Vector DB fundamentals, embeddings, semantic search |
| [02-similarity-metrics.md](Gen%20AI%3A%20Vector%20Database/docs/02-similarity-metrics.md)             | Euclidean, Cosine, Dot product metrics              |
| [03-popular-vector-databases.md](Gen%20AI%3A%20Vector%20Database/docs/03-popular-vector-databases.md) | ChromaDB, Pinecone, Milvus, Qdrant comparison       |
| [04-chromadb-basics.md](Gen%20AI%3A%20Vector%20Database/docs/04-chromadb-basics.md)                   | Getting started with ChromaDB                       |
| [05-crud-operations.md](Gen%20AI%3A%20Vector%20Database/docs/05-crud-operations.md)                   | Create, Read, Update, Delete operations             |
| [06-metadata-filtering.md](Gen%20AI%3A%20Vector%20Database/docs/06-metadata-filtering.md)             | Advanced querying and filtering                     |
| [1_chromadb_basics.ipynb](Gen%20AI%3A%20Vector%20Database/notebooks/1_chromadb_basics.ipynb)          | 📓 ChromaDB fundamentals notebook                   |
| [2_add_update_delete.ipynb](Gen%20AI%3A%20Vector%20Database/notebooks/2_add_update_delete.ipynb)      | 📓 CRUD operations notebook                         |
| [3_metadata_filtering.ipynb](Gen%20AI%3A%20Vector%20Database/notebooks/3_metadata_filtering.ipynb)    | 📓 Advanced filtering notebook                      |

### 4. Agentic AI: Basics

Hands-on exploration of AI agents with the Agno framework:

| Document                                                                                 | Description                                              |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-basic-agent.md](Agentic%20AI%3A%20Basics/docs/01-basic-agent.md)                     | Agent fundamentals, LLM + Tools + Instructions           |
| [02-agent-with-tools.md](Agentic%20AI%3A%20Basics/docs/02-agent-with-tools.md)           | Custom tools, docstrings, tool selection                 |
| [03-reasoning-agent-basic.md](Agentic%20AI%3A%20Basics/docs/03-reasoning-agent-basic.md) | Reasoning models, chain-of-thought, specialized training |
| [04-reasoning-agent-tools.md](Agentic%20AI%3A%20Basics/docs/04-reasoning-agent-tools.md) | Reasoning + tools synergy, analytical workflows          |
| [05-multimodal-agent.md](Agentic%20AI%3A%20Basics/docs/05-multimodal-agent.md)           | Image processing, structured output, validation          |

### 5. Agentic AI: Architecture and MCP

Advanced exploration of agent architecture and the Model Context Protocol:

| Document                                                                                                         | Description                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-agentic-architecture.md](Agentic%20AI%3A%20Architecture%20and%20MCP/docs/01-agentic-architecture.md)         | Layered architecture, memory systems, execution patterns |
| [02-introduction-to-mcp.md](Agentic%20AI%3A%20Architecture%20and%20MCP/docs/02-introduction-to-mcp.md)           | MCP fundamentals, USB-C analogy, protocol overview       |
| [03-mcp-primitives.md](Agentic%20AI%3A%20Architecture%20and%20MCP/docs/03-mcp-primitives.md)                     | Tools, Resources, Prompts — the building blocks          |
| [04-building-mcp-servers.md](Agentic%20AI%3A%20Architecture%20and%20MCP/docs/04-building-mcp-servers.md)         | FastMCP framework, hands-on server development           |
| [05-mcp-integration.md](Agentic%20AI%3A%20Architecture%20and%20MCP/docs/05-mcp-integration.md)                   | Integration patterns, security, multi-server setups      |
| [mcp-server/README.md](Agentic%20AI%3A%20Architecture%20and%20MCP/mcp-server/README.md)                          | Leave Management MCP Server documentation                |

### 6. Agentic AI: Multi Agent System

Building multi-agent systems with coordinator and router patterns:

| Document                                                                                                         | Description                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-coordinator-team.md](Agentic%20AI%3A%20Multi%20Agent%20System/docs/01-coordinator-team.md)                   | Coordinator pattern, parallel agent execution            |
| [02-router-team.md](Agentic%20AI%3A%20Multi%20Agent%20System/docs/02-router-team.md)                             | Router pattern, query classification and routing         |
| [03-multi-agent-architecture.md](Agentic%20AI%3A%20Multi%20Agent%20System/docs/03-multi-agent-architecture.md)   | Architecture patterns, scaling, communication strategies |

### 7. Agentic AI: Evaluation

Comprehensive evaluation strategies for AI agents:

| Document                                                                                                         | Description                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-functional-evaluation.md](Agentic%20AI%3A%20Evaluation/docs/01-functional-evaluation.md)                     | Accuracy, metrics, LLM-as-judge evaluation               |
| [02-safety-evaluation.md](Agentic%20AI%3A%20Evaluation/docs/02-safety-evaluation.md)                             | Jailbreaks, guardrails, hallucination detection          |
| [03-operational-evaluation.md](Agentic%20AI%3A%20Evaluation/docs/03-operational-evaluation.md)                   | Performance, monitoring, logging, alerting               |

### 8. Fine Tuning

Model fine-tuning techniques from quantization to practical training:

| Document                                                                                                         | Description                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-quantization-basics.md](Fine%20Tuning/docs/01-quantization-basics.md)                                        | int8 and NF4 quantization fundamentals                   |
| [02-finetuning-with-unsloth.md](Fine%20Tuning/docs/02-finetuning-with-unsloth.md)                                 | LoRA, QLoRA, Unsloth workflow, model export              |

### 9. Ethics in Gen AI

Comprehensive guide to ethical considerations in Generative AI:

| Document                                                                                                         | Description                                              |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [01-bias-and-fairness.md](Ethics%20in%20Gen%20AI/docs/01-bias-and-fairness.md)                                   | Bias types, detection methods, mitigation strategies     |
| [02-privacy-and-data-protection.md](Ethics%20in%20Gen%20AI/docs/02-privacy-and-data-protection.md)               | PII handling, data anonymization, regulatory compliance  |
| [03-hallucinations-and-misinformation.md](Ethics%20in%20Gen%20AI/docs/03-hallucinations-and-misinformation.md)   | Understanding model hallucinations, fact-checking, grounding |
| [04-transparency-and-explainability.md](Ethics%20in%20Gen%20AI/docs/04-transparency-and-explainability.md)       | Model interpretability, documentation, audit trails      |
| [05-content-moderation-and-safety.md](Ethics%20in%20Gen%20AI/docs/05-content-moderation-and-safety.md)           | Harmful content detection, guardrails, safety filters    |
| [06-intellectual-property-and-copyright.md](Ethics%20in%20Gen%20AI/docs/06-intellectual-property-and-copyright.md) | Training data rights, generated content ownership, fair use |
| [07-environmental-impact-and-sustainability.md](Ethics%20in%20Gen%20AI/docs/07-environmental-impact-and-sustainability.md) | Carbon footprint, sustainable AI practices, efficiency |
| [08-responsible-deployment-and-governance.md](Ethics%20in%20Gen%20AI/docs/08-responsible-deployment-and-governance.md) | Risk assessment, monitoring, incident response |

---

## 🗺️ Content Roadmap

### Currently Available ✅

**Module 1: Introduction to Generative AI and Agentic AI**

- [x] What is Generative AI?
- [x] Text Models (LLMs)
- [x] Image Models
- [x] Audio Models
- [x] Video Models
- [x] Agentic AI

**Module 2: Gen AI Foundation**

- [x] How LLMs Work
- [x] Model Parameters & Sampling
- [x] Vector Databases & RAG
- [x] GenAI Tech Stack
- [x] App Development Lifecycle
- [x] Key Parameters Notebook

**Module 3: Gen AI Vector Database**

- [x] What is a Vector Database?
- [x] Similarity Metrics
- [x] Popular Vector Databases
- [x] ChromaDB Basics
- [x] CRUD Operations
- [x] Metadata Filtering
- [x] ChromaDB Notebooks

**Module 4: Agentic AI Basics**

- [x] Basic Agent with Web Search
- [x] Agent with Custom Tools
- [x] Reasoning Agent (Basic)
- [x] Reasoning Agent with Tools
- [x] Multimodal Agent (Image Categorization)

**Module 5: Agentic AI Architecture and MCP**

- [x] Agentic Architecture Patterns
- [x] Introduction to MCP
- [x] MCP Server Primitives
- [x] Building MCP Servers
- [x] MCP Integration Patterns
- [x] Leave Management MCP Server

**Module 6: Agentic AI Multi Agent System**

- [x] Coordinator Team Pattern
- [x] Router Team Pattern
- [x] Multi-Agent Architecture Patterns

**Module 7: Agentic AI Evaluation**

- [x] Functional Evaluation (Accuracy, Metrics)
- [x] Safety Evaluation (Jailbreaks, Guardrails)
- [x] Operational Evaluation (Performance, Monitoring)

**Module 8: Fine Tuning**

- [x] Quantization Basics (int8, NF4)
- [x] Fine-Tuning with Unsloth (LoRA, QLoRA)

**Module 9: Ethics in Gen AI**

- [x] Bias & Fairness
- [x] Privacy & Data Protection
- [x] Hallucinations & Misinformation
- [x] Transparency & Explainability
- [x] Content Moderation & Safety
- [x] Intellectual Property & Copyright
- [x] Environmental Impact & Sustainability
- [x] Responsible Deployment & Governance

---

## 📖 Recommended Resources

### Courses

- [DeepLearning.AI - Generative AI with LLMs](https://www.deeplearning.ai/courses/generative-ai-with-llms/) — Andrew Ng
- [Codebasics - GenAI](https://www.youtube.com/playlist?list=PLeo1K3hjS3uu0N_0W6giDXzZIcB07Ng_F) — YouTube series
- [LangChain Documentation](https://python.langchain.com/) — Official tutorials

### Books

- _Build a Large Language Model (From Scratch)_ by Sebastian Raschka
- _Generative Deep Learning_ by David Foster
- _Natural Language Processing with Transformers_ by Lewis Tunstall

### Practice

- [OpenAI Playground](https://platform.openai.com/playground) — Experiment with GPT models
- [Hugging Face](https://huggingface.co/) — Open-source models and datasets
- [LangChain Templates](https://templates.langchain.com/) — Production-ready templates
- [Kaggle](https://www.kaggle.com/) — Competitions and datasets

---

## 🔑 Key Concepts Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENAI QUICK REFERENCE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  GENERATIVE AI MODALITIES:                                     │
│  ├── Text    → LLMs (GPT, Claude, Gemini, Llama)               │
│  ├── Image   → Diffusion (DALL-E, Stable Diffusion, Midjourney)│
│  ├── Audio   → Synthesis (MusicLM, ElevenLabs, Suno)           │
│  └── Video   → Generation (Sora, Runway, Pika)                 │
│                                                                │
│  LLM PARAMETERS:                                               │
│  ├── Temperature   → 0.0 (deterministic) to 1.0+ (creative)    │
│  ├── Top-k         → Limit to k most probable tokens           │
│  ├── Top-p         → Sample from cumulative probability p      │
│  └── Context       → Model's memory (4K to 1M+ tokens)         │
│                                                                │
│  VECTOR DATABASES:                                             │
│  ├── Embeddings    → Numerical representations of data         │
│  ├── Similarity    → Cosine (text), Euclidean (images)         │
│  ├── Databases     → ChromaDB, Pinecone, Milvus, Qdrant        │
│  └── Operations    → Add, Query, Update, Delete, Filter        │
│                                                                │
│  RAG PIPELINE:                                                 │
│  Query → Embed → Vector Search → Retrieve → Augment → Generate │
│                                                                │
│  TECH STACK:                                                   │
│  ├── Frameworks    → LangChain, LlamaIndex, Agno, Semantic Kernel│
│  ├── Vector DBs    → Pinecone, ChromaDB, Qdrant, Milvus        │
│  ├── Platforms     → AWS Bedrock, Azure OpenAI, Google AI, Groq│
│  └── Models        → GPT-4, Claude 3, Gemini, Llama 3          │
│                                                                │
│  AGENTIC AI:                                                   │
│  ├── Agency        → Perceive, Decide, Act, Synthesize         │
│  ├── Tools         → Custom functions, APIs, integrations      │
│  ├── Reasoning     → Chain-of-thought, multi-step analysis     │
│  └── Multimodal    → Text + Images + Structured output         │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Open issues for bugs or suggestions
- Submit PRs to improve documentation
- Add new topics or notebooks
- Share your GenAI projects

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>The future is generative. Start building it today.</i> 🚀
</p>
