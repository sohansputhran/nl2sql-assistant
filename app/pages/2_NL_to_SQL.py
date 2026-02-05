from pathlib import Path

import pandas as pd
import streamlit as st

from nl2sql_assistant.chains.risk_classifier import classify_risk  # add this import at top
from nl2sql_assistant.chains.sql_explainer import explain_sql  # import the explain_sql function
from nl2sql_assistant.chains.sql_generator import generate_sql
from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.runner import run_query, validate_select_only
from nl2sql_assistant.db.schema import schema_as_text

st.set_page_config(page_title="NL → SQL", layout="wide")


with st.sidebar:
    st.markdown("### Navigation")
    st.caption("DB-aware query, Write Mode (RAG + approval), or Generic SQL drafting.")
    st.divider()
    st.markdown("### Safety posture")
    st.caption("Read mode is SELECT-only. Write mode requires confirmation + rollback.")


st.title("NL -> SQL Generator")
st.caption(
    "DB-aware: SQL is generated specifically for your SQLite database schema and can be executed."
)

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

st.divider()
st.subheader("Guardrails & Risk Classification")

check_risk = st.button("Run risk check")

if check_risk:
    if not sql.strip():
        st.warning("Generate SQL first (or paste SQL) before running risk check.")
    else:
        try:
            risk = classify_risk(schema_text=schema_text, question=question, sql=sql)
            st.session_state["risk_result"] = risk
            st.success("Risk check completed.")
        except Exception as e:
            st.error(f"Risk classification failed: {e}")

risk = st.session_state.get("risk_result", None)
if risk:
    # Visual emphasis based on risk level
    if risk.risk_level == "high":
        st.error("Risk level: HIGH — this query may be wrong or unsafe. Review carefully.")
    elif risk.risk_level == "medium":
        st.warning("Risk level: MEDIUM — review the query before running.")
    else:
        st.info("Risk level: LOW — query looks reasonable given the schema and question.")

    if risk.flags:
        st.markdown("**Flags**")
        for f in risk.flags:
            st.write(f"- `{f.type}`: {f.message}")

    if risk.suggestions:
        st.markdown("**Suggestions**")
        for s in risk.suggestions:
            st.write(f"- {s}")

    with st.expander("Raw model output (debug)", expanded=False):
        st.code(risk.raw, language="json")

st.divider()
st.subheader("Run SQL")

run = st.button("Validate & Run SQL")

if run:
    try:
        validate_select_only(sql)

        # Optional hard stop for high risk:
        # We won't block by default, but we will warn loudly.
        risk = st.session_state.get("risk_result", None)
        if risk and risk.risk_level == "high":
            st.warning("You are running a HIGH risk query. Consider adjusting it first.")

        cols, rows = run_query(DB_PATH, sql, limit=200)
        df = pd.DataFrame(rows, columns=cols)
        st.success(f"Returned {len(df)} rows.")
        st.dataframe(df, width="stretch")
    except Exception as e:
        st.error(str(e))

with st.expander("What does this SQL do?", expanded=True):
    st.write(explain_sql(schema_text, sql))
