from langchain_core.output_parsers import StrOutputParser

from nl2sql_assistant.llm.ollama_client import get_chat_model
from nl2sql_assistant.prompts.explain_prompt import EXPLAIN_PROMPT


def explain_sql(schema_text: str, sql: str) -> str:
    """
    Returns a human-readable explanation of what the SQL does.
    This improves transparency and trust.
    """
    chain = EXPLAIN_PROMPT | get_chat_model() | StrOutputParser()
    return chain.invoke({"schema_text": schema_text, "sql": sql})
