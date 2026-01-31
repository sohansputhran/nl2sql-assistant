from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from langchain_core.output_parsers import StrOutputParser

from nl2sql_assistant.llm.ollama_client import get_chat_model
from nl2sql_assistant.prompts.write_sql_prompt import WRITE_SQL_PROMPT


@dataclass(frozen=True)
class WriteSQLResult:
    sql: str
    params: dict[str, Any]
    safety_notes: list[str]
    raw: str


def generate_write_sql(context: str, user_prompt: str) -> WriteSQLResult:
    """
    Generates a single write statement (INSERT/UPDATE/DELETE) using retrieved context.
    IMPORTANT: We do NOT execute unless validated + user confirms.
    """
    chain = WRITE_SQL_PROMPT | get_chat_model() | StrOutputParser()
    raw = chain.invoke({"context": context, "user_prompt": user_prompt})

    try:
        data = json.loads(raw)
        return WriteSQLResult(
            sql=str(data.get("sql", "")).strip(),
            params=data.get("params", {}) or {},
            safety_notes=[str(s) for s in (data.get("safety_notes", []) or [])],
            raw=raw,
        )
    except Exception:
        # Fail safe: do not produce executable SQL if parsing fails.
        return WriteSQLResult(
            sql="",
            params={},
            safety_notes=["Model returned invalid JSON. No SQL generated."],
            raw=raw,
        )
