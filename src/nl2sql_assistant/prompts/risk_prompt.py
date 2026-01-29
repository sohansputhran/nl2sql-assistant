from __future__ import annotations

from langchain_core.prompts import PromptTemplate

# We enforce JSON-only output so the UI and tests stay stable.
# This is a classic "LLM-as-a-critic" pattern to add guardrails.
RISK_PROMPT = PromptTemplate(
    input_variables=["schema_text", "question", "sql"],
    template=(
        "You are a careful SQL reviewer and data governance assistant.\n"
        "Your job: review the SQL query against the schema and the user's question.\n"
        "Return ONLY valid JSON. No markdown. No extra text.\n\n"
        "Schema:\n"
        "{schema_text}\n\n"
        "User question:\n"
        "{question}\n\n"
        "SQL:\n"
        "{sql}\n\n"
        "Return JSON with this exact schema:\n"
        "{{\n"
        '  "risk_level": "low" | "medium" | "high",\n'
        '  "flags": [\n'
        '    {{ "type": string, "message": string }}\n'
        "  ],\n"
        '  "suggestions": [string]\n'
        "}}\n\n"
        "Guidelines to flag:\n"
        "- If SQL uses columns not in schema -> high\n"
        "- If question implies a filter (e.g., last 30 days) but SQL lacks WHERE -> medium/high\n"
        "- If joins look suspicious or missing join condition -> high\n"
        "- If SELECT * used -> medium\n"
        "- If aggregation used without GROUP BY when needed -> medium/high\n"
        "- If ambiguous question -> medium with suggestion to clarify\n"
        "- Otherwise low\n"
    ),
)
