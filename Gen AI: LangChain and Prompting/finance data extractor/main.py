import json
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

from data_extractor import MissingApiKeyError, extract


st.set_page_config(page_title="Financial Data Extractor", layout="centered")
st.title("Financial Data Extractor")

EXAMPLE_TEXT = (
    "Acme Corp reported quarterly revenue of $12.3 billion versus $11.9 billion expected. "
    "Adjusted earnings came in at $1.23 per share, compared with analysts' estimates of $1.10."
)


def _make_table(extracted_data: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for item in extracted_data:
        company = item.get("company", "")
        rows.append(
            {
                "Company": company,
                "Measure": "Revenue",
                "Estimated": item.get("revenue_expected", ""),
                "Actual": item.get("revenue_actual", ""),
            }
        )
        rows.append(
            {
                "Company": company,
                "Measure": "EPS",
                "Estimated": item.get("eps_expected", ""),
                "Actual": item.get("eps_actual", ""),
            }
        )
    return pd.DataFrame(rows)


def _append_history(paragraph: str, result: dict[str, Any]) -> None:
    history = st.session_state.setdefault("history", [])
    history.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "input": paragraph,
            "result": result,
        }
    )
    st.session_state["history"] = history[-25:]


def _set_paragraph(text: str) -> None:
    st.session_state["paragraph"] = text


with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Groq model", value="llama-3.3-70b-versatile")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.0, step=0.1)
    max_tokens = st.number_input("Max tokens", min_value=32, max_value=4096, value=256, step=16)
    timeout = st.number_input("Timeout (seconds)", min_value=5.0, max_value=120.0, value=30.0, step=5.0)
    max_retries = st.number_input("Retries", min_value=0, max_value=5, value=2, step=1)
    currency_hint = st.text_input("Currency hint (optional)", value="")
    show_raw = st.checkbox("Show raw JSON/debug", value=False)

    st.divider()
    st.caption("Tip: set GROQ_API_KEY in .env or environment.")


st.subheader("Input")

if "paragraph" not in st.session_state:
    st.session_state["paragraph"] = ""
if "uploaded_file_processed" not in st.session_state:
    st.session_state["uploaded_file_processed"] = False
if "last_uploaded_file_id" not in st.session_state:
    st.session_state["last_uploaded_file_id"] = None

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    st.button("Use example", on_click=_set_paragraph, args=(EXAMPLE_TEXT,))
with col_b:
    st.button("Clear", on_click=_set_paragraph, args=("",))
with col_c:
    uploaded = st.file_uploader("Or upload a text file", type=["txt", "md"], label_visibility="collapsed")

# Handle file upload: only read once per file to preserve user edits
if uploaded is not None:
    # Check if this is a new file (different from the last processed one)
    current_file_id = (uploaded.name, uploaded.size)
    if current_file_id != st.session_state["last_uploaded_file_id"]:
        # New file uploaded, reset the processed flag
        st.session_state["uploaded_file_processed"] = False
        st.session_state["last_uploaded_file_id"] = current_file_id
    
    # Only read the file if it hasn't been processed yet
    if not st.session_state["uploaded_file_processed"]:
        try:
            uploaded_text = uploaded.read().decode("utf-8")
            if uploaded_text.strip():
                st.session_state["paragraph"] = uploaded_text
            st.session_state["uploaded_file_processed"] = True
        except Exception:
            st.warning("Could not read uploaded file as UTF-8 text.")
else:
    # File was cleared/removed, reset the flags for future uploads
    st.session_state["uploaded_file_processed"] = False
    st.session_state["last_uploaded_file_id"] = None

paragraph = st.text_area(
    "Enter a financial paragraph",
    key="paragraph",
    height=180,
    placeholder="Paste an earnings blurb here...",
)

extract_clicked = st.button("Extract", type="primary")

if extract_clicked:
    if not paragraph or not paragraph.strip():
        st.warning("Please enter a paragraph to extract data from.")
    else:
        try:
            result = extract(
                paragraph,
                model_name=model_name.strip() or "llama-3.3-70b-versatile",
                temperature=float(temperature),
                max_tokens=int(max_tokens),
                timeout=float(timeout),
                max_retries=int(max_retries),
                currency_hint=currency_hint.strip() or None,
                return_mode="raw" if show_raw else "dict",
            )
            _append_history(paragraph, result)

            st.subheader("Result")
            companies = result["companies"] if show_raw else result
            df = _make_table(companies)
            st.table(df)

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv_bytes,
                file_name="extracted_financials.csv",
                mime="text/csv",
            )

            if show_raw:
                st.subheader("Raw JSON")
                st.code(json.dumps(result, indent=2), language="json")

        except MissingApiKeyError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Extraction failed: {e}")


st.subheader("History")
history = st.session_state.get("history", [])
if not history:
    st.caption("No extractions yet.")
else:
    latest = history[-1]
    st.caption(f"Latest: {latest['timestamp']}")

    if st.checkbox("Show history items", value=False):
        for item in reversed(history[-10:]):
            with st.expander(item["timestamp"], expanded=False):
                st.write("Input")
                st.code(item["input"], language="text")
                st.write("Result")
                st.code(json.dumps(item["result"], indent=2), language="json")
