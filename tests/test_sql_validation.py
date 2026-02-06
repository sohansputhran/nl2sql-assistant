from nl2sql_assistant.db.runner import validate_sql


def test_validate_sql_accepts_simple_select():
    sql = "SELECT * FROM orders"
    ok, msg = validate_sql(sql, mode="read")

    assert ok is True
    assert "Validation passed" in msg


def test_validate_sql_accepts_select_with_single_semicolon():
    sql = "SELECT id, name FROM customers;"
    ok, msg = validate_sql(sql, mode="read")

    assert ok is True
    assert "Validation passed" in msg


def test_validate_sql_rejects_non_select_statement():
    sql = "UPDATE orders SET status = 'shipped'"
    ok, msg = validate_sql(sql, mode="read")

    assert ok is False
    assert "Only SELECT queries are allowed" in msg


def test_validate_sql_rejects_multiple_statements():
    sql = "SELECT * FROM orders; SELECT * FROM customers;"
    ok, msg = validate_sql(sql, mode="read")

    assert ok is False
    assert "Multiple SQL statements" in msg


def test_validate_sql_rejects_invalid_semicolon_usage():
    sql = "SELECT * FROM orders; DROP TABLE users"
    ok, msg = validate_sql(sql, mode="read")

    assert ok is False
    assert "Invalid semicolon usage" in msg


def test_validate_sql_rejects_empty_sql():
    sql = "   "
    ok, msg = validate_sql(sql, mode="read")

    assert ok is False
    assert "SQL is empty" in msg


def test_validate_sql_blocks_write_mode():
    sql = "UPDATE orders SET status = 'shipped'"
    ok, msg = validate_sql(sql, mode="write")

    assert ok is False
    assert "Write queries must go through isolated Write Mode" in msg


def test_validate_sql_rejects_unknown_mode():
    sql = "SELECT * FROM orders"
    ok, msg = validate_sql(sql, mode="invalid-mode")

    assert ok is False
    assert "Unknown validation mode" in msg
