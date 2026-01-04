# Finance Data Extractor

A production-ready Streamlit application that uses LangChain and Groq to **extract structured financial data** (revenue and EPS, actual vs expected) from plain-text earnings reports.

---

## Why This App?

Earnings announcements are typically written in prose:

> "Acme Corp reported quarterly revenue of $12.3 billion versus $11.9 billion expected. Adjusted earnings came in at $1.23 per share, compared with analysts' estimates of $1.10."

Manually extracting numbers from dozens of such paragraphs is tedious and error-prone. This app **automates the extraction** and returns a clean table you can download as CSV.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit UI (main.py)                 │
│  ┌───────────┐  ┌────────────┐  ┌────────────────────────┐  │
│  │  Sidebar  │  │ Text Input │  │  Result Table + CSV    │  │
│  │ (settings)│  │ / Upload   │  │  Download + History    │  │
│  └───────────┘  └─────┬──────┘  └────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│              extract(paragraph, **settings)                  │
│                       │                                      │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               data_extractor.py                             │
│  ┌────────────────┐    ┌────────────────┐                   │
│  │ PromptTemplate │───▶│   ChatGroq     │                   │
│  │   (schema +    │    │  (LLM call)    │                   │
│  │    article)    │    └───────┬────────┘                   │
│  └────────────────┘            │                            │
│                                ▼                            │
│                   ┌────────────────────┐                    │
│                   │ JsonOutputParser + │                    │
│                   │ Pydantic Validation│                    │
│                   └────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## File Breakdown

### `data_extractor.py`

| Component                    | Purpose                                                  |
| ---------------------------- | -------------------------------------------------------- |
| `FinancialExtraction`        | Pydantic model defining the expected JSON schema         |
| `ExtractorConfig`            | Dataclass holding model name, temperature, timeout, etc. |
| `_require_groq_api_key()`    | Raises `MissingApiKeyError` if `GROQ_API_KEY` is unset   |
| `_build_llm(config)`         | Returns a cached `ChatGroq` instance                     |
| `_extract_json_object(text)` | Parses JSON from LLM output; falls back to regex         |
| `_coerce_to_schema(payload)` | Validates dict against `FinancialExtraction`             |
| `extract(...)`               | Main entry point; returns validated dict                 |

### `main.py`

| Component        | Purpose                                                         |
| ---------------- | --------------------------------------------------------------- |
| Sidebar settings | Model, temperature, max tokens, timeout, retries, currency hint |
| Input area       | Text area, "Use example" / "Clear" buttons, file upload         |
| Extraction logic | Calls `extract()`, handles errors, displays table               |
| Download button  | Exports result as CSV                                           |
| History section  | Stores last 25 extractions in `st.session_state`                |

---

## Pydantic Schema

```python
from pydantic import BaseModel, Field

class FinancialExtraction(BaseModel):
    revenue_actual: str = Field(..., description="Actual revenue with unit")
    revenue_expected: str = Field(..., description="Expected revenue with unit")
    eps_actual: str = Field(..., description="Actual EPS with currency")
    eps_expected: str = Field(..., description="Expected EPS with currency")
```

**Why Pydantic?**

1. **Validation:** If the LLM omits a key or returns the wrong type, you get a clear error instead of a silent bug.
2. **Documentation:** Field descriptions double as prompt hints.
3. **Serialization:** `.model_dump()` gives you a clean dict.

---

## Prompt Engineering

The prompt instructs the LLM to return **only** a JSON object with the four required keys:

```
You are a precise information extractor.

TASK
Extract revenue and EPS (actual vs expected/estimated) from the article.

OUTPUT RULES
Return ONLY a JSON object with exactly these keys:
revenue_actual, revenue_expected, eps_actual, eps_expected.
Each value must be a string that includes units (million/billion) and currency if present.
No markdown. No code fences. No extra keys. No explanations.

ARTICLE
=======
{article}
```

### Tips for Reliable Extraction

- **Be explicit:** "Return ONLY a JSON object" reduces hallucination.
- **Forbid extras:** "No markdown. No code fences." prevents ` ```json ` wrappers.
- **Include units:** Asking for units avoids ambiguity (is "12.3" billion or million?).

---

## Robust JSON Parsing

LLMs sometimes wrap JSON in markdown or add commentary. The parser handles this:

```python
def _extract_json_object(text: str) -> dict:
    # Try LangChain's JsonOutputParser first
    try:
        return JsonOutputParser().parse(text)
    except Exception:
        pass

    # Fallback: regex to find {...}
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise OutputParserException("Model did not return JSON.")

    return json.loads(match.group(0))
```

---

## Configuration Options

| Parameter       | Default                   | Description                               |
| --------------- | ------------------------- | ----------------------------------------- |
| `model_name`    | `llama-3.3-70b-versatile` | Groq model ID                             |
| `temperature`   | `0.0`                     | Lower = more deterministic                |
| `max_tokens`    | `256`                     | Max response length                       |
| `timeout`       | `30.0`                    | Seconds before timeout                    |
| `max_retries`   | `2`                       | Retry on transient errors                 |
| `currency_hint` | `None`                    | E.g., "USD" to bias output format         |
| `return_mode`   | `"dict"`                  | `"dict"` or `"raw"` (includes debug info) |

---

## Running the App

```bash
cd "Gen AI: LangChain and Prompting/finance data extractor"
streamlit run main.py
```

1. **Paste or upload** an earnings paragraph.
2. **Adjust settings** in the sidebar if needed.
3. Click **Extract**.
4. **Download CSV** or toggle **Show raw JSON** for debugging.

---

## Example

### Input

```
Acme Corp reported quarterly revenue of $12.3 billion versus $11.9 billion expected.
Adjusted earnings came in at $1.23 per share, compared with analysts' estimates of $1.10.
```

### Output Table

| Measure | Estimated     | Actual        |
| ------- | ------------- | ------------- |
| Revenue | $11.9 billion | $12.3 billion |
| EPS     | $1.10         | $1.23         |

### Raw JSON

```json
{
  "revenue_actual": "$12.3 billion",
  "revenue_expected": "$11.9 billion",
  "eps_actual": "$1.23",
  "eps_expected": "$1.10"
}
```

---

## Error Handling

| Error                   | Cause                          | Solution                                 |
| ----------------------- | ------------------------------ | ---------------------------------------- |
| `MissingApiKeyError`    | `GROQ_API_KEY` not set         | Add to `.env` and restart                |
| `OutputParserException` | LLM didn't return valid JSON   | Try a different model or rephrase input  |
| `ValidationError`       | JSON missing required keys     | Check if the paragraph contains all data |
| Timeout                 | Groq server slow or overloaded | Increase timeout or retry                |

---

## Extending the App

### Add More Fields

1. Update `FinancialExtraction` with new fields.
2. Update the prompt's `OUTPUT RULES`.
3. Update `_make_table()` in `main.py`.

### Support Other LLMs

Swap `ChatGroq` for `ChatOpenAI`, `ChatAnthropic`, or `ChatOllama`:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

### Batch Processing

Wrap `extract()` in a loop to process multiple paragraphs from a CSV or database.

---

## Further Reading

- [LangChain Output Parsers](https://python.langchain.com/docs/concepts/output_parsers)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
