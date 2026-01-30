from __future__ import annotations

from langchain_core.prompts import PromptTemplate

# JSON-only output makes downstream execution predictable + testable.
# IMPORTANT:
# - PromptTemplate treats { ... } as variables.
# - So any literal JSON braces must be escaped as {{ ... }}.
WRITE_SQL_PROMPT = PromptTemplate(
    input_variables=["context", "user_prompt"],
    template=(
        "You are a database assistant. The user wants to MODIFY the SQLite database.\n"
        "Use the provided context (schema + dictionary). Do NOT invent columns.\n"
        "Return ONLY valid JSON. No markdown.\n\n"
        "Context:\n{context}\n\n"
        "User request:\n{user_prompt}\n\n"
        "Return JSON:\n"
        "{{\n"
        '  "sql": "single write statement (INSERT/UPDATE/DELETE)",\n'
        '  "params": {{ "param_name": "value" }},\n'
        '  "safety_notes": ["string"]\n'
        "}}\n\n"
        "Rules:\n"
        "- For UPDATE/DELETE: include a WHERE clause.\n"
        "- Prefer parameterized SQL using named parameters (:param).\n"
        "- If request is ambiguous (missing identifiers), return sql as empty string\n"
        "  and explain what's missing in safety_notes.\n"
    ),
)
