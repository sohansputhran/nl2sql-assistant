from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


def run_query(db_path: Path, sql: str, limit: int = 200) -> tuple[list[str], list[tuple[Any, ...]]]:
    sql_clean = sql.strip().rstrip(";")
    # basic safety: only allow SELECT for now
    if not sql_clean.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this stage.")

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(f"{sql_clean} LIMIT {int(limit)};")
        colnames = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return colnames, rows
