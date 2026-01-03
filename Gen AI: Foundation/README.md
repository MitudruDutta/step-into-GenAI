# 🧠 Foundations of Generative AI

## 📌 Overview

This module provides a comprehensive exploration of the technical foundations that power modern Generative AI systems. From understanding how Large Language Models process and generate text to building production-ready AI applications, this guide covers the essential concepts every AI practitioner needs to know.

---

## 📚 What You'll Learn

| Topic                     | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| **LLM Internals**         | How autoregressive models and transformers work        |
| **Model Control**         | Parameters that shape AI behavior and output           |
| **Data & Retrieval**      | Vector databases and RAG architectures                 |
| **Tech Ecosystem**        | Frameworks, platforms, and models for building AI apps |
| **Development Lifecycle** | From evaluation to deployment and monitoring           |

---

## 🗂️ Module Contents

### 1. 🧠 How Large Language Models Work

Understanding the core mechanics behind LLMs — autoregressive generation, transformer architecture, and the massive scale of training.

**Key Concepts:**

- Autoregressive token prediction
- Transformer architecture and self-attention
- Training costs and computational requirements

📖 **[Read Full Documentation →](./docs/01-how-llms-work.md)**

---

### 2. ⚙️ Model Parameters & Sampling

Master the parameters that control LLM output — from deterministic precision to creative exploration.

**Key Concepts:**

- Context window and model memory
- Temperature: controlling creativity vs. consistency
- Top-k and Top-p sampling strategies

📖 **[Read Full Documentation →](./docs/02-model-parameters-sampling.md)**

---

### 3. 📂 Vector Databases & RAG

Learn how to augment LLMs with external knowledge through vector databases and Retrieval-Augmented Generation.

**Key Concepts:**

- Embeddings and vector representations
- Approximate Nearest Neighbor (ANN) algorithms
- RAG architecture for grounded responses
- Popular vector databases: Qdrant, ChromaDB, Pinecone, Milvus

📖 **[Read Full Documentation →](./docs/03-vector-databases-rag.md)**

---

### 4. 🛠️ The GenAI Tech Stack

Navigate the modern ecosystem of tools for building AI applications — frameworks, databases, platforms, and models.

**Key Concepts:**

- Development frameworks: LangChain, HuggingFace, PyTorch
- Vector databases for semantic search
- Cloud platforms: AWS Bedrock, Azure OpenAI, Google AI Studio
- Foundation models: GPT, Claude, Gemini, Llama, Mistral

📖 **[Read Full Documentation →](./docs/04-genai-tech-stack.md)**

---

### 5. 🚀 App Development Lifecycle

A structured approach to building GenAI applications — from initial evaluation to production monitoring.

**Key Concepts:**

1. Evaluate if GenAI is actually needed
2. Data collection and preparation
3. Choose model architecture
4. Training and evaluation
5. Optimization, deployment, and compliance
6. Monitoring and continuous feedback

📖 **[Read Full Documentation →](./docs/05-app-development-lifecycle.md)**

---

## 🎯 Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENAI FOUNDATIONS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  LLMs:        Transformers → Autoregressive → Token by Token   │
│  Control:     Temperature, Top-k, Top-p, Context Window        │
│  Retrieval:   Embeddings → Vector DB → RAG → Grounded Output   │
│  Stack:       LangChain + Vector DB + LLM + Cloud Platform     │
│  Lifecycle:   Evaluate → Data → Model → Deploy → Monitor       │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Additional Resources

| Resource                                                    | Description                               |
| ----------------------------------------------------------- | ----------------------------------------- |
| **[Notebooks](./notebooks/)**                               | Hands-on code examples and experiments    |
| **[Key Parameters Notebook](./notebooks/key_params.ipynb)** | Interactive exploration of LLM parameters |

---

## 📖 Recommended Learning Path

1. Start with **[How LLMs Work](./docs/01-how-llms-work.md)** to understand the fundamentals
2. Learn **[Model Parameters](./docs/02-model-parameters-sampling.md)** to control AI output
3. Explore **[Vector Databases & RAG](./docs/03-vector-databases-rag.md)** for knowledge augmentation
4. Study the **[Tech Stack](./docs/04-genai-tech-stack.md)** to choose your tools
5. Follow the **[Development Lifecycle](./docs/05-app-development-lifecycle.md)** to build production apps

---

_Last Updated: January 2026_
