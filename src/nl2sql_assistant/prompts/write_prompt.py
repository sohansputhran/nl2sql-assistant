from langchain_core.prompts import PromptTemplate

# This prompt generates SQL patches (INSERT/UPDATE/DELETE) ONLY when user is in write mode.
WRITE_PROMPT = PromptTemplate(
    input_variables=["schema_text", "context", "instruction"],
    template=(
        "You are a database assistant for SQLite.\n"
        "Generate ONE safe SQL write operation (INSERT/UPDATE/DELETE) matching the instruction.\n"
        "Return ONLY SQL. No markdown.\n\n"
        "Rules:\n"
        "1) Must include a precise WHERE clause for UPDATE/DELETE using a primary key when possible.\n"
        "2) If the instruction does not identify target rows precisely, output a SELECT query that finds the target IDs instead.\n"
        "3) Use only tables/columns that exist in schema.\n\n"
        "Schema:\n{schema_text}\n\n"
        "Retrieved context (may include allowed fields, policies, and target row IDs):\n{context}\n\n"
        "Instruction:\n{instruction}\n\n"
        "SQL:"
    ),
)
