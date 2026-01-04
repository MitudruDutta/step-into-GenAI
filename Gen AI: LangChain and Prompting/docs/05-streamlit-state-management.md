# Streamlit State Management

This document explains how Streamlit's execution model works and how to use `st.session_state` effectively—patterns used throughout the Finance Data Extractor app.

---

## How Streamlit Runs

**Key Insight:** Streamlit re-runs your entire script **from top to bottom** every time the user interacts with a widget (button click, slider change, text input, etc.).

```
User clicks button
       │
       ▼
┌──────────────────┐
│  main.py re-runs │  ◀── Every interaction triggers this
│  (top to bottom) │
└──────────────────┘
       │
       ▼
  UI updates
```

### Implications

1. **Variables reset** on every run unless stored in `st.session_state`.
2. **Expensive computations** (like LLM calls) should be cached or guarded.
3. **Widget state** (text inputs, sliders) persists automatically via their `key` parameter.

---

## st.session_state Basics

`st.session_state` is a **dictionary-like object** that persists across reruns for a single user session.

### Reading & Writing

```python
import streamlit as st

# Write
st.session_state["counter"] = 0

# Read
current = st.session_state.get("counter", 0)

# Increment
st.session_state["counter"] += 1
```

### Initializing State

Always check if a key exists before using it:

```python
if "history" not in st.session_state:
    st.session_state["history"] = []
```

Or use `.setdefault()`:

```python
history = st.session_state.setdefault("history", [])
```

---

## Widget State with `key`

When you give a widget a `key`, its value is automatically stored in `st.session_state`:

```python
# The text_area value is stored in st.session_state["paragraph"]
paragraph = st.text_area("Enter text", key="paragraph")

# You can also access it directly
print(st.session_state["paragraph"])
```

### Modifying Widget State

To programmatically change a widget's value, update the session state **before** the widget renders:

```python
def clear_input():
    st.session_state["paragraph"] = ""

st.button("Clear", on_click=clear_input)
st.text_area("Enter text", key="paragraph")
```

**Important:** Don't set `st.session_state["key"]` **after** the widget with that key—it causes a conflict.

---

## Patterns from This Project

### Pattern 1: Extraction History

Store a list of past extractions:

```python
def _append_history(paragraph: str, result: dict) -> None:
    history = st.session_state.setdefault("history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "input": paragraph,
        "result": result,
    })
    # Keep only last 25 items
    st.session_state["history"] = history[-25:]
```

Display history:

```python
history = st.session_state.get("history", [])
if not history:
    st.caption("No extractions yet.")
else:
    for item in reversed(history[-10:]):
        with st.expander(item["timestamp"]):
            st.code(item["input"])
            st.json(item["result"])
```

### Pattern 2: Button Callbacks

Use `on_click` to modify state before the rerun:

```python
def _set_paragraph(text: str) -> None:
    st.session_state["paragraph"] = text

st.button("Use example", on_click=_set_paragraph, args=(EXAMPLE_TEXT,))
st.button("Clear", on_click=_set_paragraph, args=("",))
```

This ensures the text area sees the updated value when it renders.

### Pattern 3: Conditional Execution

Only run expensive code when a button is clicked:

```python
if st.button("Extract"):
    # This block only runs when the button is clicked
    result = extract(paragraph)  # LLM call
    st.table(result)
```

### Pattern 4: Caching LLM Clients

Avoid recreating the LLM client on every rerun:

```python
# In data_extractor.py
_LLM_CACHE: dict[tuple, ChatGroq] = {}

def _build_llm(config):
    cache_key = (config.model_name, config.temperature, ...)
    if cache_key in _LLM_CACHE:
        return _LLM_CACHE[cache_key]
    llm = ChatGroq(...)
    _LLM_CACHE[cache_key] = llm
    return llm
```

Or use Streamlit's `@st.cache_resource`:

```python
@st.cache_resource
def get_llm(model_name: str, temperature: float):
    return ChatGroq(model_name=model_name, temperature=temperature)
```

---

## Common Pitfalls

### Pitfall 1: State Reset on Page Refresh

`st.session_state` is **per-session**. If the user refreshes the page, state is lost. For persistence, use a database or file.

### Pitfall 2: Widget Key Conflicts

If you use the same key for two widgets:

```python
st.text_input("A", key="input")
st.text_input("B", key="input")  # Error!
```

Each key must be unique.

### Pitfall 3: Modifying State After Widget

This causes a `StreamlitAPIException`:

```python
st.text_input("Input", key="my_input")
st.session_state["my_input"] = "new value"  # ❌ Error
```

Instead, use a callback:

```python
def update():
    st.session_state["my_input"] = "new value"

st.button("Update", on_click=update)
st.text_input("Input", key="my_input")  # ✅ Works
```

### Pitfall 4: File Uploader State

`st.file_uploader` returns a file object only on the run when a file is uploaded. To persist it:

```python
uploaded = st.file_uploader("Upload")
if uploaded is not None:
    st.session_state["uploaded_content"] = uploaded.read().decode("utf-8")

# Use the persisted content
content = st.session_state.get("uploaded_content", "")
```

---

## Debugging State

Print the entire session state:

```python
st.write(st.session_state)
```

Or use Streamlit's built-in state viewer (experimental):

```python
st.experimental_show(st.session_state)
```

---

## Summary

| Concept                    | Usage                                         |
| -------------------------- | --------------------------------------------- |
| Persist data across reruns | `st.session_state["key"] = value`             |
| Initialize with default    | `st.session_state.setdefault("key", default)` |
| Link widget to state       | `st.text_input(..., key="my_key")`            |
| Update state on button     | `st.button(..., on_click=callback)`           |
| Cache expensive objects    | `@st.cache_resource` or manual dict cache     |

---

## Further Reading

- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
- [Add Statefulness to Apps](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Widget Behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior)
- [Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
