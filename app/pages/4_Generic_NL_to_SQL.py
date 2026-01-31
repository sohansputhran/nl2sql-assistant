import streamlit as st

from nl2sql_assistant.chains.generic_sql_generator import generate_generic_sql

st.set_page_config(page_title="Generic NL → SQL", page_icon="🧾", layout="wide")

st.title("🧾 Generic NL → SQL")
st.caption("Converts any natural language into SQL (not tied to your database).")

dialect = st.selectbox("SQL dialect", ["SQLite", "PostgreSQL", "MySQL"], index=0)

schema_optional = st.text_area(
    "Optional schema (recommended for accuracy)",
    height=160,
    placeholder="Paste your schema here if you want the SQL to match your tables/columns...",
)

nl = st.text_area(
    "Natural language request",
    height=120,
    placeholder="Example: Find top 5 products by revenue in the last 30 days...",
)

generate = st.button("Generate SQL")

if generate:
    if not nl.strip():
        st.warning("Please enter a request.")
    else:
        # Stage note:
        # We do NOT validate or execute generic SQL because we do not know the user's DB.
        res = generate_generic_sql(
            user_prompt=nl,
            dialect=dialect,
            schema_text=schema_optional.strip() if schema_optional.strip() else None,
        )
        st.subheader("Generated SQL")
        st.code(res, language="sql")
