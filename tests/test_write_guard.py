import pytest

from nl2sql_assistant.db.write_guard import validate_write_sql


def test_allows_insert():
    validate_write_sql("INSERT INTO customers(name) VALUES ('X');")


def test_blocks_select():
    with pytest.raises(ValueError):
        validate_write_sql("SELECT * FROM customers;")


def test_update_requires_where():
    with pytest.raises(ValueError):
        validate_write_sql("UPDATE customers SET name='X';")


def test_blocks_multi_statement():
    with pytest.raises(ValueError):
        validate_write_sql("DELETE FROM customers WHERE customer_id=1; DROP TABLE customers;")
