from pathlib import Path

import pandas as pd
import streamlit as st

from nl2sql_assistant.chains.sql_generator import generate_sql
from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.runner import run_query, validate_select_only
from nl2sql_assistant.db.schema import schema_as_text

st.set_page_config(page_title="NL → SQL", layout="wide")

st.title("NL → SQL Generator")
st.caption("Uses an open-source LLM via Ollama. Output is SELECT-only and must be reviewed.")

DB_PATH = Path("data/sample.db")
ensure_sample_db(DB_PATH)

schema_text = schema_as_text(DB_PATH)

with st.expander("Schema (used for generation)", expanded=False):
    st.code(schema_text, language="text")

question = st.text_input(
    "Ask a question about the data (natural language)",
    value="Show completed orders with customer name, newest first.",
)

col1, col2 = st.columns([1, 1])

with col1:
    model_hint = st.info(
        "Local setup required: `ollama serve` and `ollama pull llama3.1` (or change model in code)."
    )

generate = st.button("Generate SQL")

if generate:
    try:
        res = generate_sql(schema_text=schema_text, question=question)
        st.session_state["generated_sql"] = res.sql
        st.session_state["notes"] = res.notes
        st.success("SQL generated.")
    except Exception as e:
        st.error(f"Generation failed: {e}")

sql = st.text_area(
    "Generated SQL (editable)",
    value=st.session_state.get("generated_sql", ""),
    height=180,
    placeholder="Click 'Generate SQL' to create a query...",
)

run = st.button("Validate & Run")

if run:
    try:
        validate_select_only(sql)
        cols, rows = run_query(DB_PATH, sql, limit=200)
        df = pd.DataFrame(rows, columns=cols)
        st.success(f"Returned {len(df)} rows.")
        st.dataframe(df, width='stretch')
    except Exception as e:
        st.error(str(e))

if st.session_state.get("notes"):
    st.caption(st.session_state["notes"])
