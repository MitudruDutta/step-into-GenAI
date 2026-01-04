# Getting Started

This guide walks you through setting up your environment to run LangChain-based LLM applications, including the Finance Data Extractor Streamlit app.

---

## Prerequisites

| Requirement       | Version | Notes                            |
| ----------------- | ------- | -------------------------------- |
| Python            | 3.10+   | 3.12 recommended                 |
| pip               | Latest  | `pip install --upgrade pip`      |
| Git               | Any     | For cloning the repo             |
| Groq API Key      | —       | Free at https://console.groq.com |
| (Optional) Ollama | Latest  | For local model inference        |

---

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/step-into-GenAI.git
cd step-into-GenAI
```

---

## 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate      # Windows
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Core Packages

| Package            | Purpose                                       |
| ------------------ | --------------------------------------------- |
| `langchain-groq`   | LangChain integration for Groq cloud LLMs     |
| `langchain-core`   | Core abstractions (prompts, chains, parsers)  |
| `langchain-ollama` | LangChain integration for local Ollama models |
| `pydantic`         | Data validation and schema enforcement        |
| `streamlit`        | Web UI framework                              |
| `python-dotenv`    | Load environment variables from `.env`        |
| `pandas`           | Tabular data manipulation                     |

---

## 4. Configure Your API Key

### Option A: `.env` File (Recommended)

Create a file named `.env` in the repository root:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

> **Security Tip:** The `.gitignore` already excludes `.env`, so your key won't be committed.

### Option B: Export in Shell

```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"
```

Add this line to your `~/.bashrc` or `~/.zshrc` to persist across sessions.

---

## 5. Verify the Setup

Run a quick sanity check:

```bash
python -c "from langchain_groq import ChatGroq; print('LangChain-Groq OK')"
```

If no errors appear, you're ready to go.

---

## 6. Run the Notebook

Open `notebooks/1_simple_llm_call.ipynb` in VS Code or JupyterLab:

```bash
jupyter lab notebooks/1_simple_llm_call.ipynb
# or in VS Code, just open the file
```

Execute the cells sequentially to:

1. Load the API key via `python-dotenv`.
2. Call a Groq-hosted model.
3. (Optional) Call a local Ollama model.

---

## 7. Launch the Streamlit App

```bash
cd "Gen AI: LangChain and Prompting/finance data extractor"
streamlit run main.py
```

Open http://localhost:8501 in your browser. You should see the **Financial Data Extractor** UI.

---

## Troubleshooting

| Issue                     | Solution                                                                    |
| ------------------------- | --------------------------------------------------------------------------- |
| `MissingApiKeyError`      | Ensure `.env` exists and contains `GROQ_API_KEY=...`, then restart the app. |
| `ModuleNotFoundError`     | Run `pip install -r requirements.txt` again.                                |
| Streamlit not found       | `pip install streamlit` or check your virtual environment is active.        |
| Ollama connection refused | Start the Ollama server with `ollama serve` in a separate terminal.         |

---

## Next Steps

- **[02-model-setup-groq-vs-ollama.md](02-model-setup-groq-vs-ollama.md)** – Deep dive into cloud vs local inference.
- **[03-finance-data-extractor.md](03-finance-data-extractor.md)** – Understand the extraction app architecture.
- **[04-langchain-key-concepts.md](04-langchain-key-concepts.md)** – Learn about chains, prompts, and parsers.
