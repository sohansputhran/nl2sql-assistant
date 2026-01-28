import pytest

from nl2sql_assistant.db.runner import validate_select_only


def test_validate_allows_select():
    validate_select_only("SELECT 1;")


@pytest.mark.parametrize(
    "bad_sql",
    [
        "DROP TABLE customers;",
        "UPDATE customers SET name='x';",
        "INSERT INTO customers(name) VALUES ('x');",
        "DELETE FROM customers;",
        "SELECT 1; DROP TABLE customers;",  # multi-statement
    ],
)
def test_validate_blocks_non_select(bad_sql: str):
    with pytest.raises(ValueError):
        validate_select_only(bad_sql)
