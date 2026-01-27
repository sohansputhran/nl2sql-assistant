from __future__ import annotations

import sqlite3
from pathlib import Path


def get_table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
    ).fetchall()
    return [r[0] for r in rows]


def get_table_columns(conn: sqlite3.Connection, table: str) -> list[dict[str, str]]:
    rows = conn.execute(f"PRAGMA table_info({table});").fetchall()
    # PRAGMA table_info: cid, name, type, notnull, dflt_value, pk
    cols = []
    for _cid, name, col_type, notnull, dflt_value, pk in rows:
        cols.append(
            {
                "name": str(name),
                "type": str(col_type),
                "notnull": str(bool(notnull)),
                "pk": str(bool(pk)),
                "default": "" if dflt_value is None else str(dflt_value),
            }
        )
    return cols


def schema_as_text(db_path: Path) -> str:
    with sqlite3.connect(db_path) as conn:
        tables = get_table_names(conn)
        lines: list[str] = []
        for t in tables:
            cols = get_table_columns(conn, t)
            lines.append(f"TABLE {t}:")
            for c in cols:
                flags = []
                if c["pk"] == "True":
                    flags.append("PK")
                if c["notnull"] == "True":
                    flags.append("NOT NULL")
                flag_str = f" ({', '.join(flags)})" if flags else ""
                lines.append(f"  - {c['name']} : {c['type']}{flag_str}")
            lines.append("")
        return "\n".join(lines).strip()
