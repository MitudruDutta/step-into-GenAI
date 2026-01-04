# LangChain Key Concepts

This document explains the core LangChain abstractions used throughout this project: **Chains**, **PromptTemplates**, **Output Parsers**, and how they compose together.

---

## What is LangChain?

LangChain is a Python (and JavaScript) framework for building applications powered by Large Language Models. It provides:

1. **Abstractions** – Unified interfaces for prompts, models, and outputs.
2. **Composability** – Chain components together with the `|` pipe operator.
3. **Integrations** – 100+ LLM providers, vector stores, tools, and more.

---

## 1. LangChain Chains (LCEL)

### The `|` Pipe Operator

LangChain Expression Language (LCEL) lets you compose components:

```python
chain = prompt | llm | parser
result = chain.invoke({"input": "Hello"})
```

This is equivalent to:

```python
prompt_value = prompt.invoke({"input": "Hello"})
llm_output = llm.invoke(prompt_value)
result = parser.invoke(llm_output)
```

### Why Chains?

| Benefit         | Explanation                                  |
| --------------- | -------------------------------------------- |
| **Readability** | Left-to-right data flow is intuitive         |
| **Reusability** | Swap components without rewriting logic      |
| **Streaming**   | LCEL chains support token-by-token streaming |
| **Async**       | Built-in `ainvoke()` for async execution     |

### Example from This Project

```python
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

prompt = PromptTemplate.from_template("Summarize: {text}")
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

chain = prompt | llm
response = chain.invoke({"text": "LangChain is a framework..."})
print(response.content)
```

---

## 2. PromptTemplate

### What It Does

`PromptTemplate` lets you define a prompt with **placeholders** that get filled in at runtime.

### Basic Usage

```python
from langchain_core.prompts import PromptTemplate

template = """
You are a helpful assistant.

User question: {question}

Answer concisely.
"""

prompt = PromptTemplate.from_template(template)
formatted = prompt.invoke({"question": "What is Python?"})
print(formatted.text)
```

**Output:**

```
You are a helpful assistant.

User question: What is Python?

Answer concisely.
```

### Multiple Variables

```python
template = "Translate '{text}' from {source_lang} to {target_lang}."
prompt = PromptTemplate.from_template(template)
prompt.invoke({
    "text": "Hello",
    "source_lang": "English",
    "target_lang": "Spanish"
})
```

### Partial Variables

Pre-fill some variables:

```python
prompt = PromptTemplate(
    template="Today is {date}. Question: {question}",
    partial_variables={"date": "2026-01-04"}
)
prompt.invoke({"question": "What day is it?"})
```

---

## 3. Chat Prompt Templates

For chat models, use `ChatPromptTemplate` with roles:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful financial analyst."),
    ("human", "{user_input}"),
])

messages = prompt.invoke({"user_input": "What is EPS?"})
```

This produces a list of messages:

```python
[
    SystemMessage(content="You are a helpful financial analyst."),
    HumanMessage(content="What is EPS?")
]
```

---

## 4. Output Parsers

### Problem

LLMs return **strings**. You often need **structured data** (dict, list, Pydantic model).

### Solution: Output Parsers

| Parser                           | Output Type    | Use Case                    |
| -------------------------------- | -------------- | --------------------------- |
| `StrOutputParser`                | `str`          | Just get the text           |
| `JsonOutputParser`               | `dict`         | Parse JSON from response    |
| `PydanticOutputParser`           | Pydantic model | Validate against schema     |
| `CommaSeparatedListOutputParser` | `list[str]`    | Parse comma-separated items |

### JsonOutputParser Example

```python
from langchain_core.output_parsers import JsonOutputParser

llm_output = '{"name": "Alice", "age": 30}'
parser = JsonOutputParser()
result = parser.parse(llm_output)
# {'name': 'Alice', 'age': 30}
```

### PydanticOutputParser Example

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

parser = PydanticOutputParser(pydantic_object=Person)

# Include format instructions in your prompt
prompt = PromptTemplate(
    template="Extract person info:\n{format_instructions}\n\nText: {text}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

### Handling Malformed Output

LLMs sometimes wrap JSON in markdown. Use fallback parsing:

````python
import re
import json

def safe_parse_json(text: str) -> dict:
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract JSON from markdown
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return json.loads(match.group(1))

    # Extract any {...} block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return json.loads(match.group(0))

    raise ValueError("No JSON found")
````

---

## 5. Putting It Together

Here's the pattern used in `data_extractor.py`:

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel

# 1. Define the schema
class FinancialExtraction(BaseModel):
    revenue_actual: str
    revenue_expected: str
    eps_actual: str
    eps_expected: str

# 2. Create the prompt
prompt = PromptTemplate.from_template("""
Extract revenue and EPS from this article.
Return JSON with keys: revenue_actual, revenue_expected, eps_actual, eps_expected.

Article: {article}
""")

# 3. Initialize the LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

# 4. Build the chain
chain = prompt | llm

# 5. Invoke and parse
response = chain.invoke({"article": "Acme Corp reported..."})
parser = JsonOutputParser()
data = parser.parse(response.content)

# 6. Validate with Pydantic
validated = FinancialExtraction.model_validate(data)
print(validated.model_dump())
```

---

## 6. Advanced: RunnablePassthrough and RunnableLambda

### RunnablePassthrough

Pass input through unchanged (useful for branching):

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough() | llm
# Input goes directly to llm
```

### RunnableLambda

Wrap any function:

```python
from langchain_core.runnables import RunnableLambda

def add_context(input_dict):
    input_dict["context"] = "You are an expert."
    return input_dict

chain = RunnableLambda(add_context) | prompt | llm
```

---

## 7. Streaming

LCEL chains support streaming out of the box:

```python
for chunk in chain.stream({"article": "..."}):
    print(chunk.content, end="", flush=True)
```

---

## Summary Table

| Concept         | Class                     | Purpose                         |
| --------------- | ------------------------- | ------------------------------- |
| Chain           | `prompt \| llm \| parser` | Compose components              |
| Prompt          | `PromptTemplate`          | Inject variables into prompts   |
| Chat Prompt     | `ChatPromptTemplate`      | Multi-turn / role-based prompts |
| String Parser   | `StrOutputParser`         | Extract plain text              |
| JSON Parser     | `JsonOutputParser`        | Extract dict from JSON          |
| Pydantic Parser | `PydanticOutputParser`    | Validate against schema         |

---

## Further Reading

- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/concepts/lcel)
- [Prompt Templates](https://python.langchain.com/docs/concepts/prompt_templates)
- [Output Parsers](https://python.langchain.com/docs/concepts/output_parsers)
- [Runnables](https://python.langchain.com/docs/concepts/runnables)
