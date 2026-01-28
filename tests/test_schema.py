"""
test_schema.py
--------------
Purpose:
- Ensure schema extraction is stable and includes expected tables.
- This test protects us from accidental refactors that break the prompt schema format.

"""

from pathlib import Path

from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.schema import schema_as_text


def test_schema_extraction_contains_tables(tmp_path: Path):
    # Create a temporary DB for testing (doesn't pollute your local ./data folder)
    db_path = tmp_path / "sample.db"
    ensure_sample_db(db_path)

    text = schema_as_text(db_path)

    # Assert key tables exist in the schema output
    assert "TABLE customers:" in text
    assert "TABLE orders:" in text
    assert "TABLE order_items:" in text
    assert "TABLE products:" in text
