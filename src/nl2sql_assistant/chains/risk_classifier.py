from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from nl2sql_assistant.llm.ollama_client import get_chat_model
from nl2sql_assistant.prompts.risk_prompt import RISK_PROMPT


@dataclass(frozen=True)
class RiskFlag:
    type: str
    message: str


@dataclass(frozen=True)
class RiskResult:
    """
    Structured result used by Streamlit.

    We parse JSON into this format so the UI doesn't depend on raw model output.
    """

    risk_level: str  # low | medium | high
    flags: list[RiskFlag]
    suggestions: list[str]
    raw: str  # store raw model output for debugging


def build_risk_chain() -> Runnable:
    """
    Chain:
      inputs -> risk prompt -> ChatOllama -> string output

    We keep this minimal and do JSON parsing ourselves for better control.
    """
    model = get_chat_model()
    return RISK_PROMPT | model | StrOutputParser()


def _coerce_risk_level(value: Any) -> str:
    v = str(value).strip().lower()
    return v if v in {"low", "medium", "high"} else "medium"


def parse_risk_json(raw: str) -> RiskResult:
    """
    Parse JSON safely. If model returns invalid JSON, we fallback to a safe default.
    """
    try:
        data = json.loads(raw)
        risk_level = _coerce_risk_level(data.get("risk_level", "medium"))

        flags_in = data.get("flags", []) or []
        flags: list[RiskFlag] = []
        for f in flags_in:
            # Defensive parsing: ensure keys exist
            flags.append(
                RiskFlag(type=str(f.get("type", "unknown")), message=str(f.get("message", "")))
            )

        suggestions_in = data.get("suggestions", []) or []
        suggestions = [str(s) for s in suggestions_in]

        return RiskResult(
            risk_level=risk_level,
            flags=flags,
            suggestions=suggestions,
            raw=raw,
        )
    except Exception:
        # Fallback: if parsing fails, mark medium risk to be safe.
        return RiskResult(
            risk_level="medium",
            flags=[RiskFlag(type="json_parse_error", message="Model did not return valid JSON.")],
            suggestions=["Review the SQL carefully before running."],
            raw=raw,
        )


def classify_risk(schema_text: str, question: str, sql: str) -> RiskResult:
    chain = build_risk_chain()
    raw = chain.invoke({"schema_text": schema_text, "question": question, "sql": sql})
    return parse_risk_json(raw)
