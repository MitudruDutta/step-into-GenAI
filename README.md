# 🤖 Step Into Generative AI

A structured, hands-on learning repository for mastering Generative AI fundamentals. From understanding LLMs to building RAG applications, this project provides comprehensive documentation and practical implementations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What You'll Learn

| Module                                       | Topics                                                                       | Difficulty        |
| -------------------------------------------- | ---------------------------------------------------------------------------- | ----------------- |
| Introduction to Generative AI and Agentic AI | GenAI fundamentals, Text/Image/Audio/Video models, Agentic AI                | ⭐ Beginner       |
| Gen AI: Foundation                           | LLM internals, Model parameters, Vector DBs & RAG, Tech stack, App lifecycle | ⭐⭐ Intermediate |
| Gen AI: Vector Database                      | Vector DBs, Embeddings, Similarity metrics, ChromaDB, CRUD, Filtering        | ⭐⭐ Intermediate |
| Agentic AI: Basics                           | AI Agents, Tools, Reasoning models, Multimodal agents, Agno framework        | ⭐⭐ Intermediate |

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

---

## 📓 Notebooks Overview

| Notebook                                                       | Module          | What You'll Learn                                       |
| -------------------------------------------------------------- | --------------- | ------------------------------------------------------- |
| `Gen AI: Foundation/notebooks/key_params.ipynb`                | Foundation      | Explore temperature, top-k, top-p effects on LLM output |
| `Gen AI: Vector Database/notebooks/1_chromadb_basics.ipynb`    | Vector Database | ChromaDB setup, collections, basic queries              |
| `Gen AI: Vector Database/notebooks/2_add_update_delete.ipynb`  | Vector Database | CRUD operations in ChromaDB                             |
| `Gen AI: Vector Database/notebooks/3_metadata_filtering.ipynb` | Vector Database | Advanced filtering and querying                         |

---

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- OpenAI API key (optional, for API examples)
- CUDA-capable GPU (optional, for local models)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/step-into-GenAI.git
cd step-into-GenAI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Core Dependencies

| Package          | Purpose                          |
| ---------------- | -------------------------------- |
| openai           | OpenAI API access                |
| langchain        | LLM application framework        |
| langchain-openai | OpenAI integration for LangChain |
| chromadb         | Vector database                  |
| transformers     | HuggingFace models               |
| torch            | Deep learning framework          |
| numpy            | Numerical computing              |
| pandas           | Data manipulation                |
| matplotlib       | Visualization                    |
| jupyter          | Interactive notebooks            |

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
