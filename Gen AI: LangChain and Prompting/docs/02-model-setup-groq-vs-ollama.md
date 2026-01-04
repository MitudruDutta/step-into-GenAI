# Model Setup: Groq (Cloud) vs Ollama (Local)

This document explains the two primary ways to run Large Language Models (LLMs) in this project: **Groq** for blazing-fast cloud inference and **Ollama** for fully offline, privacy-preserving local inference.

---

## Overview Comparison

| Aspect         | Groq (Cloud)                              | Ollama (Local)                     |
| -------------- | ----------------------------------------- | ---------------------------------- |
| **Deployment** | Hosted API                                | Runs on your machine               |
| **Speed**      | Extremely fast (custom LPU hardware)      | Depends on your GPU/CPU            |
| **Cost**       | Free tier available; pay-as-you-go beyond | Free (you pay for electricity)     |
| **Privacy**    | Data sent to Groq servers                 | Data never leaves your machine     |
| **Setup**      | Just an API key                           | Install Ollama + download models   |
| **Internet**   | Required                                  | Not required after model download  |
| **Models**     | Llama 3, Mixtral, Gemma, etc.             | Llama 3, Mistral, Phi, Gemma, etc. |

---

## Groq (Cloud)

### What is Groq?

Groq is an AI inference company that provides an API to run open-weight LLMs on their custom **Language Processing Unit (LPU)** hardware. The result is **sub-second latency** for most queries—often 10–50× faster than typical cloud providers.

### Getting an API Key

1. Visit https://console.groq.com and sign up.
2. Navigate to **API Keys** and create a new key.
3. Copy the key (starts with `gsk_...`).

### Configuration

Store the key in a `.env` file:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Or export it:

```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"
```

### LangChain Integration

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  # or "mixtral-8x7b-32768", "gemma2-9b-it", etc.
    temperature=0.0,      # 0 = deterministic, higher = more creative
    max_tokens=256,       # max response length
    timeout=30.0,         # seconds before timing out
    max_retries=2,        # retry on transient errors
)

response = llm.invoke("What is LangChain?")
print(response.content)
```

### Available Models (as of 2026)

| Model                     | Context Window | Notes                                |
| ------------------------- | -------------- | ------------------------------------ |
| `llama-3.3-70b-versatile` | 128k           | Great general-purpose model          |
| `llama-3.1-8b-instant`    | 128k           | Faster, smaller                      |
| `mixtral-8x7b-32768`      | 32k            | Mixture-of-experts, strong reasoning |
| `gemma2-9b-it`            | 8k             | Google's open model                  |

> Check https://console.groq.com/docs/models for the latest list.

### Rate Limits

Free tier typically allows:

- ~30 requests/minute
- ~14,400 requests/day

For production workloads, consider upgrading or implementing rate-limit handling.

---

## Ollama (Local)

### What is Ollama?

Ollama is an open-source tool that lets you **download and run LLMs locally** on macOS, Linux, or Windows. Models run entirely on your hardware—no internet required after the initial download.

### Installation

#### macOS / Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows

Download the installer from https://ollama.com/download.

### Downloading Models

```bash
ollama pull mistral          # 7B params, fast
ollama pull llama3.2         # Meta's Llama 3.2
ollama pull phi3             # Microsoft's small model
ollama pull gemma2:9b        # Google's Gemma 2
```

List installed models:

```bash
ollama list
```

### Starting the Server

Ollama runs as a background service. If it's not already running:

```bash
ollama serve
```

By default, it listens on `http://localhost:11434`.

### LangChain Integration

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="mistral",
    temperature=0.0,
    num_predict=256,   # equivalent to max_tokens
)

response = llm.invoke("What is LangChain?")
print(response.content)
```

### Recommended Models by Use Case

| Use Case           | Model          | VRAM Required |
| ------------------ | -------------- | ------------- |
| Fast prototyping   | `phi3`         | ~4 GB         |
| General chat       | `mistral`      | ~6 GB         |
| Advanced reasoning | `llama3.2`     | ~8 GB         |
| Long context       | `mistral-nemo` | ~12 GB        |

### GPU vs CPU

- **GPU (NVIDIA/AMD/Apple Silicon):** Much faster; Ollama auto-detects.
- **CPU-only:** Works but slower; use smaller models like `phi3`.

Check GPU usage:

```bash
ollama ps
```

---

## Choosing Between Groq and Ollama

| Scenario                 | Recommendation                   |
| ------------------------ | -------------------------------- |
| Quick experiments, demos | **Groq** – instant setup, fast   |
| Sensitive/private data   | **Ollama** – data stays local    |
| Offline environments     | **Ollama** – no internet needed  |
| Production with SLAs     | **Groq** (or other managed API)  |
| Learning/cost-sensitive  | **Groq free tier** or **Ollama** |

---

## Hybrid Approach

You can use both in the same project. For example, develop locally with Ollama for privacy, then switch to Groq for deployment:

```python
import os
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

USE_LOCAL = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"

if USE_LOCAL:
    llm = ChatOllama(model="mistral", temperature=0)
else:
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

response = llm.invoke("Hello!")
```

---

## Troubleshooting

| Issue                         | Solution                                        |
| ----------------------------- | ----------------------------------------------- |
| `GroqError: api_key not set`  | Check `.env` or `export GROQ_API_KEY`           |
| `Connection refused` (Ollama) | Run `ollama serve` first                        |
| `Model not found` (Ollama)    | Run `ollama pull <model>`                       |
| Slow Ollama responses         | Use a smaller model or ensure GPU is detected   |
| Rate limit exceeded (Groq)    | Wait, reduce request frequency, or upgrade plan |

---

## Further Reading

- [Groq Documentation](https://console.groq.com/docs)
- [Ollama Documentation](https://ollama.com/library)
- [LangChain ChatGroq](https://python.langchain.com/docs/integrations/chat/groq)
- [LangChain ChatOllama](https://python.langchain.com/docs/integrations/chat/ollama)
