import json
import os
import re
from dataclasses import asdict, dataclass
from typing import Any, Literal

from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field, ValidationError

load_dotenv()


class FinancialCompany(BaseModel):
    company: str = Field(..., description="Company name")
    revenue_actual: str = Field(..., description="Actual revenue with unit, e.g. '12.3 billion USD'")
    revenue_expected: str = Field(
        ..., description="Expected/estimated revenue with unit, e.g. '11.9 billion USD'"
    )
    eps_actual: str = Field(..., description="Actual EPS with unit/currency, e.g. '$1.23'")
    eps_expected: str = Field(..., description="Expected/estimated EPS with unit/currency, e.g. '$1.10'")


@dataclass(frozen=True)
class ExtractorConfig:
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.0
    max_tokens: int | None = 256
    timeout: float = 30.0
    max_retries: int = 2


class MissingApiKeyError(RuntimeError):
    pass


_LLM_CACHE: dict[tuple[str, float, int | None, float, int], ChatGroq] = {}


def _require_groq_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise MissingApiKeyError(
            "GROQ_API_KEY is not set. Put it in a .env file or export GROQ_API_KEY before running."
        )
    return api_key


def _build_llm(config: ExtractorConfig) -> ChatGroq:
    _require_groq_api_key()
    cache_key = (
        config.model_name,
        float(config.temperature),
        config.max_tokens,
        float(config.timeout),
        int(config.max_retries),
    )
    cached = _LLM_CACHE.get(cache_key)
    if cached is not None:
        return cached

    llm = ChatGroq(
        model_name=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        timeout=config.timeout,
        max_retries=config.max_retries,
    )
    _LLM_CACHE[cache_key] = llm
    return llm


def _extract_json_object(text: str) -> dict[str, Any]:
    """Best-effort JSON extraction from a model response."""
    parser = JsonOutputParser()
    try:
        return parser.parse(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise OutputParserException("Model did not return JSON.")

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise OutputParserException(f"Invalid JSON returned by model: {e}")


def _coerce_to_schema(payload: Any) -> list[dict[str, str]]:
    if not isinstance(payload, list):
        raise OutputParserException(
            "Expected a JSON array of company objects."
        )

    validated: list[dict[str, str]] = []
    errors: list[str] = []
    for idx, item in enumerate(payload):
        try:
            entry = FinancialCompany.model_validate(item)
            validated.append(entry.model_dump())
        except ValidationError as e:
            errors.append(f"index {idx}: {e}")

    if errors:
        raise OutputParserException(
            "One or more company entries are invalid. "
            "Each entry must include company, revenue_actual, revenue_expected, eps_actual, eps_expected. "
            + " | ".join(errors)
        )

    if not validated:
        raise OutputParserException("No valid company entries found in JSON array.")

    return validated


def extract(
    article_text: str,
    *,
    model_name: str = "llama-3.3-70b-versatile",
    temperature: float = 0.0,
    max_tokens: int | None = 512,
    timeout: float = 30.0,
    max_retries: int = 2,
    currency_hint: str | None = None,
    return_mode: Literal["dict", "raw"] = "dict",
) -> list[dict[str, Any]]:
    """Extract revenue/EPS actual vs expected for one or more companies.

    return_mode:
      - "dict": returns a list of company dicts
      - "raw":  returns list plus debug fields
    """
    if not article_text or not article_text.strip():
        raise ValueError("article_text is empty")

    config = ExtractorConfig(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
    )

    schema_note = (
        "Return ONLY a JSON array. Each element is an object with exactly these keys: "
        "company, revenue_actual, revenue_expected, eps_actual, eps_expected. "
        "All values are strings that include units (million/billion) and currency if present. "
        "Do not invent companies; only return companies explicitly in the article."
    )
    if currency_hint:
        schema_note += f" Prefer currency/format consistent with: {currency_hint}."

    prompt = """
You are a precise information extractor.

TASK
Extract revenue and EPS (actual vs expected/estimated) for every company mentioned in the article.

OUTPUT RULES
{schema_note}
No markdown. No code fences. No extra keys. No explanations. Output must be valid JSON.

ARTICLE
=======
{article}
""".strip()

    pt = PromptTemplate.from_template(prompt)
    llm = _build_llm(config)

    chain = pt | llm
    response = chain.invoke({"article": article_text, "schema_note": schema_note})
    model_text = getattr(response, "content", str(response))

    payload = _extract_json_object(model_text)
    validated = _coerce_to_schema(payload)

    if return_mode == "raw":
        return {
            "companies": validated,
            "_debug": {
                "config": asdict(config),
                "payload": payload,
                "model_text": model_text,
            },
        }
    return validated