"""
runner.py
---------
Purpose:
- Execute SELECT-only SQL queries against the SQLite database.

"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

SELECT_ONLY_RE = re.compile(r"^\s*select\b", re.IGNORECASE)


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
