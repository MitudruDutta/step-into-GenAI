# Gen AI: LangChain and Prompting

A hands-on guide to calling Large Language Models (LLMs) using **LangChain**, with working examples for both cloud (Groq) and local (Ollama) inference, plus a full **Streamlit** application that extracts structured financial data from plain-text earnings reports.

---

## 📁 Project Structure

```
Gen AI: LangChain and Prompting/
├── README.md                   # You are here
├── docs/
│   ├── 01-getting-started.md
│   ├── 02-model-setup-groq-vs-ollama.md
│   ├── 03-finance-data-extractor.md
│   ├── 04-langchain-key-concepts.md
│   └── 05-streamlit-state-management.md
├── notebooks/
│   └── 1_simple_llm_call.ipynb # Quick-start notebook for LLM calls
└── finance data extractor/
    ├── data_extractor.py       # Core extraction logic (Pydantic schema, Groq chain)
    └── main.py                 # Streamlit UI
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
# From the repo root
pip install -r requirements.txt
```

Key dependencies: `langchain-groq`, `langchain-core`, `pydantic`, `streamlit`, `python-dotenv`.

### 2. Set Your API Key

Create a `.env` file in the repo root (or export it in your shell):

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

> Groq offers a generous free tier—sign up at https://console.groq.com.

### 3. Run the Notebook (Optional)

Open `notebooks/1_simple_llm_call.ipynb` in VS Code or JupyterLab and run the cells to see:

- Loading API keys via `python-dotenv`
- Calling **Groq** models in the cloud (`ChatGroq`)
- Calling **Ollama** models locally (`ChatOllama`)

### 4. Launch the Streamlit App

```bash
cd "Gen AI: LangChain and Prompting/finance data extractor"
streamlit run main.py
```

Open http://localhost:8501 in your browser.

---

## 🛠️ Model Setup: Local vs. Cloud

| Provider   | Type  | Pros                                                       | Cons                             |
| ---------- | ----- | ---------------------------------------------------------- | -------------------------------- |
| **Groq**   | Cloud | Extremely fast inference, free tier, zero setup            | Requires internet & API key      |
| **Ollama** | Local | Full privacy, no network needed once models are downloaded | Requires local GPU/CPU resources |

### Groq (Cloud)

```python
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
llm.invoke("Explain LangChain in one sentence.")
```

### Ollama (Local)

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral", temperature=0)
llm.invoke("Explain LangChain in one sentence.")
```

> Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull mistral`).

---

## 💼 Finance Data Extractor

A real-world mini-app demonstrating **structured output extraction** with LangChain.

### Features

| Feature                 | Description                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| **Pydantic schema**     | Guarantees the LLM returns `revenue_actual`, `revenue_expected`, `eps_actual`, `eps_expected` |
| **Robust JSON parsing** | Falls back to regex extraction if the model wraps JSON in markdown                            |
| **Sidebar settings**    | Adjust model, temperature, max tokens, timeout, retries on the fly                            |
| **File upload**         | Drop a `.txt` or `.md` file instead of pasting                                                |
| **Download CSV**        | Export results with one click                                                                 |
| **Extraction history**  | Review your last 25 extractions in-app                                                        |

### Example Input

```
Acme Corp reported quarterly revenue of $12.3 billion versus $11.9 billion expected.
Adjusted earnings came in at $1.23 per share, compared with analysts' estimates of $1.10.
```

### Example Output

| Measure | Estimated     | Actual        |
| ------- | ------------- | ------------- |
| Revenue | $11.9 billion | $12.3 billion |
| EPS     | $1.10         | $1.23         |

---

## 📚 Key Concepts Covered

1. **LangChain Chains** – composing prompts and models with the `|` operator.
2. **PromptTemplate** – injecting variables into prompts cleanly.
3. **JsonOutputParser** – coercing LLM text into Python dicts.
4. **Pydantic validation** – enforcing schema on extracted data.
5. **Streamlit state management** – `st.session_state` for history and reactive UI.

---

## 🧪 Running Tests (Optional)

```bash
pytest -q
```

(Add your own tests under a `tests/` folder as the project grows.)

---

## 📝 License

This project is released under the [MIT License](../LICENSE).

---

## � Documentation

| Doc                                                                       | Description                                |
| ------------------------------------------------------------------------- | ------------------------------------------ |
| [01-getting-started.md](docs/01-getting-started.md)                       | Environment setup, dependencies, first run |
| [02-model-setup-groq-vs-ollama.md](docs/02-model-setup-groq-vs-ollama.md) | Cloud vs local LLM comparison              |
| [03-finance-data-extractor.md](docs/03-finance-data-extractor.md)         | App architecture, schema, prompt design    |
| [04-langchain-key-concepts.md](docs/04-langchain-key-concepts.md)         | Chains, prompts, parsers explained         |
| [05-streamlit-state-management.md](docs/05-streamlit-state-management.md) | Session state patterns                     |

---

## �🙏 Acknowledgements

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Groq Console](https://console.groq.com)
- [Ollama](https://ollama.com)
- Inspired by Codebasics GenAI course material.
