from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser

from nl2sql_assistant.llm.ollama_client import get_chat_model
from nl2sql_assistant.prompts.generic_sql_prompt import GENERIC_SQL_PROMPT


def generate_generic_sql(user_prompt: str, dialect: str, schema_text: str | None) -> str:
    """
    Generates SQL from natural language without requiring a local database.

    Important:
    - If schema_text is None/empty, output may use generic table names.
    - We keep it simple and return SQL-only string.
    """
    chain = GENERIC_SQL_PROMPT | get_chat_model() | StrOutputParser()
    schema = schema_text or ""  # empty schema is allowed here
    return chain.invoke(
        {"dialect": dialect, "user_prompt": user_prompt, "schema_text": schema}
    ).strip()
