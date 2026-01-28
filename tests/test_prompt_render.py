from nl2sql_assistant.prompts.sql_prompt import SQL_PROMPT


def test_prompt_renders():
    out = SQL_PROMPT.format(schema_text="TABLE t:\n  - id : INTEGER", question="Count rows")
    assert "Schema:" in out
    assert "Question:" in out
    assert "SQL:" in out
