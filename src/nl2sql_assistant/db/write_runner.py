from __future__ import annotations

import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from nl2sql_assistant.db.write_guard import validate_write_sql


def backup_db(db_path: Path) -> Path:
    """
    Creates a timestamped backup before executing writes.
    This is a simple and powerful safety feature for demos and real usage.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.with_name(f"{db_path.stem}_backup_{ts}{db_path.suffix}")
    shutil.copy2(db_path, backup_path)
    return backup_path


def execute_write(db_path: Path, sql: str, params: dict[str, Any]) -> int:
    """
    Executes a single write statement inside a transaction.
    Rolls back automatically on errors.
    """
    validate_write_sql(sql)
    sql_clean = sql.strip().rstrip(";")

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            conn.execute("BEGIN;")
            cur = conn.execute(sql_clean, params)
            conn.commit()
            return cur.rowcount
        except Exception:
            conn.rollback()
            raise
