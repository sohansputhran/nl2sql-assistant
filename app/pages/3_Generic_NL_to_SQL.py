import streamlit as st

from nl2sql_assistant.chains.generic_sql_generator import generate_generic_sql
from nl2sql_assistant.db.runner import ollama_is_available
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "Generic NL -> SQL",
    "Converts any natural language request into SQL (not tied to your database). Output is SQL-only.",
)

# Sidebar framing (kept small & product-like)
with st.sidebar:
    st.markdown("### Navigation")
    st.caption("- DB-aware query \n- Write Mode (RAG + approval) \n- Generic SQL drafting")
    st.divider()
    st.markdown("### Safety posture")
    st.caption(
        "- Read mode is SELECT-only\n"
        "- Write mode requires explicit confirmation\n"
        "- Optional DB backup before execution"
    )

# Session state defaults
st.session_state.setdefault("dialect", "SQLite")
st.session_state.setdefault("schema_optional", "")
st.session_state.setdefault("nl_request", "")
st.session_state.setdefault("generated_sql", "")

# Header metrics (recruiter-friendly)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mode", "Generic")
m2.metric("Dialects", "SQLite / Postgres / MySQL")
m3.metric("Schema", "Optional")
m4.metric("Execution", "Never")

st.divider()

# Main layout: left (inputs), right (output)
left, right = st.columns([1.05, 1.25], gap="large")

with left:
    st.subheader("1) Configure")
    st.selectbox(
        "SQL dialect",
        ["SQLite", "PostgreSQL", "MySQL"],
        index=["SQLite", "PostgreSQL", "MySQL"].index(st.session_state["dialect"])
        if st.session_state["dialect"] in ["SQLite", "PostgreSQL", "MySQL"]
        else 0,
        key="dialect",
        help="Choose the SQL dialect you want the model to generate.",
    )

    with st.expander("Optional schema (recommended for higher accuracy)", expanded=False):
        st.text_area(
            "Schema",
            key="schema_optional",
            height=160,
            placeholder="Paste your schema here (tables, columns, relationships). Example:\n\n"
            "CREATE TABLE customers(customer_id INT, name TEXT);\n"
            "CREATE TABLE orders(order_id INT, customer_id INT, total NUMERIC);",
            label_visibility="collapsed",
        )

    st.subheader("2) Describe the query")
    st.text_area(
        "Natural language request",
        key="nl_request",
        height=120,
        placeholder="Example: Find top 5 products by revenue in the last 30 days...",
        label_visibility="visible",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        generate = st.button("Generate SQL", type="primary", use_container_width=True)
    with c2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state["schema_optional"] = ""
        st.session_state["nl_request"] = ""
        st.session_state["generated_sql"] = ""
        st.rerun()

with right:
    st.subheader("Generated SQL")
    st.caption("This output is not executed. Review and run it in your own database environment.")

    # Keep output visible even before generation
    if not st.session_state["generated_sql"]:
        st.code("— Generate SQL to see the output here —", language="sql")
    else:
        st.code(st.session_state["generated_sql"], language="sql")

        # Optional convenience: download as .sql (looks polished for recruiters)
        st.download_button(
            "Download SQL (.sql)",
            data=st.session_state["generated_sql"].encode("utf-8"),
            file_name="query.sql",
            mime="text/sql",
            use_container_width=True,
        )

# For deployed demo, show warning if Ollama not available
if not ollama_is_available():
    st.warning(
        "Ollama is not available in this environment. "
        "This deployed demo runs in UI-only mode. Run locally for full LLM features."
    )
    st.stop()

# Generation action (after layout so UI feels stable)
if generate:
    nl = st.session_state["nl_request"].strip()
    if not nl:
        st.warning("Please enter a natural language request.")
    else:
        schema_text = st.session_state["schema_optional"].strip() or None
        
        # Generic SQL is not validated/executed because there is no DB context.
        # This is intentional safety behavior.
        res = generate_generic_sql(
            user_prompt=nl,
            dialect=st.session_state["dialect"],
            schema_text=schema_text,
        )
        st.session_state["generated_sql"] = res
        st.toast("SQL generated")
