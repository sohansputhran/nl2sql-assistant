from langchain_core.prompts import PromptTemplate

# LLM is used here ONLY for explanation — not decision making.
EXPLAIN_PROMPT = PromptTemplate(
    input_variables=["schema_text", "sql"],
    template=(
        "Explain what the following SQL query does in plain English.\n"
        "Do not mention SQL keywords explicitly unless needed.\n\n"
        "Schema:\n{schema_text}\n\n"
        "SQL:\n{sql}\n\n"
        "Explanation:"
    ),
)
