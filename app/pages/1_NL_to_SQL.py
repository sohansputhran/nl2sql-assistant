from pathlib import Path

import pandas as pd
import streamlit as st

from nl2sql_assistant.chains.risk_classifier import classify_risk  # add this import at top

# from nl2sql_assistant.chains.sql_explainer import explain_sql  # import the explain_sql function
from nl2sql_assistant.chains.sql_generator import generate_sql
from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.runner import run_query, validate_sql
from nl2sql_assistant.db.schema import schema_as_text
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config
from nl2sql_assistant.ui.widget import status_row

set_app_config()
inject_base_css()

page_header(
    "NL -> SQL Generator",
    "DB-aware: SQL is generated for your SQLite schema and can be executed (SELECT-only by default).",
)

# --- Session state defaults ---
st.session_state.setdefault("question", "Show completed orders with customer name, newest first.")
st.session_state.setdefault("generated_sql", "")
st.session_state.setdefault("risk", "unknown")
st.session_state.setdefault("validated", False)
st.session_state.setdefault("executable", False)
st.session_state.setdefault("validation_msg", "")
st.session_state.setdefault("result_df", None)

# --- Small, recruiter-friendly summary row ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mode", "DB-aware (Read)")
m2.metric("Execution", "SELECT-only")
m3.metric("Models", "Ollama (local)")
m4.metric("Safety", "Validate + Risk Check")

st.divider()

DB_PATH = Path("data/sample.db")
ensure_sample_db(DB_PATH)

schema_text = schema_as_text(DB_PATH)

question = st.text_input(
    "Ask a question about the data (natural language)",
    value="Show completed orders with customer name, newest first.",
)

# --- Main layout ---
left, right = st.columns([1.05, 1.25], gap="large")

with left:
    st.subheader("1) Ask in natural language")
    st.text_input(
        "Question",
        key="question",
        placeholder="e.g., List top 10 customers by total spend in 2024",
        label_visibility="collapsed",
    )

    # Move "local setup" note to a compact sidebar-style info
    st.info(
        "Local setup: run `ollama serve` and ensure your model is available (e.g., `ollama pull llama3.1`)."
    )

    # Schema expander stays but visually cleaner
    with st.expander("Schema used for generation", expanded=False):
        st.code(schema_text, language="text")

    # Actions grouped: looks more product-like
    c1, c2 = st.columns([1, 1])
    with c1:
        gen = st.button("Generate SQL", type="primary", use_container_width=True)
    with c2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state["generated_sql"] = ""
        st.session_state["risk"] = "unknown"
        st.session_state["validated"] = False
        st.session_state["executable"] = False
        st.session_state["validation_msg"] = ""
        st.session_state["result_df"] = None
        st.rerun()

    if gen:
        res = generate_sql(schema_text=schema_text, question=question)
        st.session_state["generated_sql"] = res.sql
        st.session_state["notes"] = res.notes

        # After generation, make it "not validated" until user runs checks.
        st.session_state["validated"] = False
        st.session_state["executable"] = False
        st.session_state["risk"] = "unknown"
        st.session_state["validation_msg"] = (
            "Generated. Run validation + risk check before executing."
        )
        st.success("SQL generated.")

with right:
    st.subheader("2) Review SQL")
    st.caption("Edit if needed. Execution remains SELECT-only unless you switch to Write Mode.")

    # Make editor smaller by default; grow only when needed
    st.session_state["generated_sql"] = st.text_area(
        "Generated SQL",
        value=st.session_state["generated_sql"],
        height=220,  # key fix: reduce massive empty box
        placeholder="Click 'Generate SQL' to create a query…",
        label_visibility="collapsed",
    )

    # Status row (looks “enterprise”)
    status_row(
        mode="DB-aware (Read)",
        executable=bool(st.session_state["executable"]),
        risk=str(st.session_state["risk"]),
        validated=bool(st.session_state["validated"]),
    )

    # Guardrails + execution controls (kept together!)
    a1, a2, a3 = st.columns([1, 1, 1])
    with a1:
        run_risk = st.button("Run risk check", use_container_width=True)
    with a2:
        validate = st.button("Validate SQL", use_container_width=True)
    with a3:
        run = st.button(
            "Execute (SELECT only)",
            use_container_width=True,
            disabled=not st.session_state["validated"],
        )

    if run_risk:
        risk = classify_risk(
            schema_text=schema_text, question=question, sql=st.session_state["generated_sql"]
        )
        st.session_state["risk_result"] = risk
        st.success("Risk check completed.")
        st.session_state["risk"] = risk
        st.toast("Risk check complete")

    if validate:
        ok, msg = validate_sql(sql=st.session_state["generated_sql"], mode="read")
        st.session_state["validated"] = ok
        st.session_state["executable"] = ok
        st.session_state["validation_msg"] = msg

    if st.session_state["validation_msg"]:
        if st.session_state["validated"]:
            st.success(st.session_state["validation_msg"])
        else:
            st.error(st.session_state["validation_msg"])

    if run:
        cols, rows = run_query(DB_PATH, st.session_state["generated_sql"], limit=200)
        df = pd.DataFrame(rows, columns=cols)
        st.session_state["result_df"] = df

st.divider()

# --- Results area ---
st.subheader("3) Results")
if st.session_state["result_df"] is None:
    st.caption("Execute a validated query to see results here.")
else:
    st.dataframe(st.session_state["result_df"], use_container_width=True)

# Optional: keep “debug”/details hidden so UI stays clean for recruiters
with st.expander("Developer details (optional)", expanded=False):
    st.write("Put prompt, retrieved schema chunks, validator output, and trace info here.")
