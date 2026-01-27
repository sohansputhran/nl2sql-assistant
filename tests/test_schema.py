from pathlib import Path

from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.schema import schema_as_text


def test_schema_extraction_contains_tables(tmp_path: Path):
    db_path = tmp_path / "sample.db"
    ensure_sample_db(db_path)

    text = schema_as_text(db_path)
    assert "TABLE customers:" in text
    assert "TABLE orders:" in text
    assert "TABLE order_items:" in text
    assert "TABLE products:" in text
