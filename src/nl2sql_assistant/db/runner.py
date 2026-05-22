"""
Strict SQL validation for NL → SQL execution.

Design goals:
- Prevent destructive or unsafe queries
- Enforce SELECT-only in read mode
- Ensure schema grounding (no hallucinated tables/columns)
- Block multi-statement, comments, and injections
- Return human-readable explanations (important for UI + audits)
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

# Use a proper SQL parser to determine statement type reliably.
import sqlglot

SELECT_ONLY_RE = re.compile(r"^\s*select\b", re.IGNORECASE)
ALLOWED_WRITE = {"insert", "update", "delete"}


def validate_sql(sql: str, *, mode: str = "read") -> tuple[bool, str]:
    """
    Validate SQL according to the execution mode.

    Design goals:
    - UI-safe: never raise, always return (ok, message)
    - Strict by default
    - Easy to extend with schema checks, allowlists, etc.

    Parameters
    ----------
    sql : str
        SQL query to validate.
    mode : str
        Execution mode: "read" or "write".

    Returns
    -------
    (bool, str)
        Validation status and human-readable message.
    """

    if not sql or not sql.strip():
        return False, "SQL is empty."

    try:
        if mode == "read":
            # Core guardrail: SELECT-only, single statement
            validate_select_only(sql)

            # Future extension points (intentionally explicit)
            # -----------------------------------------------
            # - validate_against_schema(sql, schema)
            # - block_select_star(sql)
            # - enforce_limit(sql)
            # -----------------------------------------------

            return True, "Validation passed (SELECT-only)."

        elif mode == "write":
            # Write mode should NEVER reach here unless already gated.
            # We fail fast to avoid accidental execution.
            return False, "Write queries must go through isolated Write Mode."

        else:
            return False, f"Unknown validation mode: {mode!r}"

    except ValueError as e:
        # Convert hard failure into UI-safe feedback
        return False, str(e)

    except Exception as e:
        # Catch-all safety net (never leak stack traces to UI)
        return False, f"Validation failed due to unexpected error: {e}"


def validate_single_statement(sql: str) -> str:
    parsed = sqlglot.parse_one(sql)
    stmt = parsed.key.lower()  # e.g. select/update/insert/delete
    return stmt


def validate_write(sql: str) -> None:
    stmt = validate_single_statement(sql)
    if stmt not in ALLOWED_WRITE:
        raise ValueError("Write mode allows only INSERT/UPDATE/DELETE.")


def validate_select_only(sql: str) -> None:
    """
    Minimal SQL safety guardrail for early stages.
    - Only allow SELECT queries.
    - Block obvious multi-statement attempts using ';'
    """
    cleaned = sql.strip()
    if not SELECT_ONLY_RE.match(cleaned):
        raise ValueError("Only SELECT queries are allowed.")

    # Block multi-statement patterns. One trailing semicolon is okay.
    semicolons = cleaned.count(";")
    if semicolons > 1:
        raise ValueError("Multiple SQL statements are not allowed.")

    if semicolons == 1 and not cleaned.rstrip().endswith(";"):
        raise ValueError("Invalid semicolon usage detected.")


def run_write(db_path: Path, sql: str) -> int:
    validate_write(sql)
    sql_clean = sql.strip().rstrip(";")

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        # Transactional safety
        with conn:
            cur = conn.execute(sql_clean)
            return cur.rowcount


def run_query(db_path: Path, sql: str, limit: int = 200) -> tuple[list[str], list[tuple[Any, ...]]]:
    """
    Run a SQL query (SELECT only) and return results.

    Parameters
    ----------
    db_path : Path
        Path to the SQLite database file.
    sql : str
        SQL query string (must start with SELECT).
    limit : int
        Defensive limit to avoid returning huge result sets.

    Returns
    -------
    (colnames, rows)
        colnames: List[str]
        rows: List[Tuple[Any,...]]
    """
    # Normalize input: strip spaces, remove trailing semicolons
    sql_clean = sql.strip().rstrip(";")

    # Basic safety gate: block non-SELECT statements
    if not sql_clean.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this stage.")

    with sqlite3.connect(db_path) as conn:
        # Add LIMIT defensively (even if user forgets)
        cur = conn.execute(f"{sql_clean} LIMIT {int(limit)};")

        # Extract column names from cursor metadata
        colnames = [d[0] for d in cur.description] if cur.description else []

        # Fetch all rows (bounded by limit)
        rows = cur.fetchall()

        return colnames, rows
