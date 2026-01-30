from __future__ import annotations

import re

WRITE_RE = re.compile(r"^\s*(insert|update|delete)\b", re.IGNORECASE)


def validate_write_sql(sql: str) -> None:
    """
    Hard guardrails for writes.

    Stage 5 policy:
    - Only allow INSERT/UPDATE/DELETE
    - Only one statement
    - UPDATE/DELETE must include WHERE
    """
    cleaned = sql.strip()
    if not cleaned:
        raise ValueError("Empty SQL. Nothing to execute.")

    if not WRITE_RE.match(cleaned):
        raise ValueError("Write SQL must start with INSERT/UPDATE/DELETE.")

    # Block multi-statement attempts.
    if cleaned.count(";") > 1:
        raise ValueError("Multiple SQL statements are not allowed.")

    lower = cleaned.lower()
    if lower.startswith("update") or lower.startswith("delete"):
        if " where " not in lower:
            raise ValueError("UPDATE/DELETE requires a WHERE clause.")
