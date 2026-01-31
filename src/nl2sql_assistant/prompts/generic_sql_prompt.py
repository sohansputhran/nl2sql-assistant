from __future__ import annotations

from langchain_core.prompts import PromptTemplate

# This prompt is DB-agnostic, so it cannot guarantee table/column correctness unless schema is provided.
GENERIC_SQL_PROMPT = PromptTemplate(
    input_variables=["dialect", "user_prompt", "schema_text"],
    template=(
        "You are an expert SQL assistant.\n"
        "Generate a SQL query for the requested dialect.\n"
        "Output ONLY SQL (no markdown, no backticks, no commentary).\n\n"
        "Dialect: {dialect}\n\n"
        "Schema (may be empty):\n"
        "{schema_text}\n\n"
        "User request:\n"
        "{user_prompt}\n\n"
        "SQL:"
    ),
)
