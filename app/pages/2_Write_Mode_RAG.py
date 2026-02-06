import json

import streamlit as st

from nl2sql_assistant.app_state import get_db_path, get_rag_index
from nl2sql_assistant.chains.write_sql_generator import generate_write_sql
from nl2sql_assistant.db.write_runner import backup_db, execute_write
from nl2sql_assistant.rag.retriever_bm25 import retrieve
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "Write Mode with RAG",
    "Generates INSERT/UPDATE/DELETE using retrieved context. Requires explicit confirmation before execution.",
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
st.session_state.setdefault("write_prompt", "")
st.session_state.setdefault("retrieved_context", "")
st.session_state.setdefault(
    "write_sql_res", None
)  # stores dataclass/object returned by generate_write_sql
st.session_state.setdefault("confirm_execute", False)
st.session_state.setdefault("backup_first", True)

# Data / index
db_path = get_db_path()
rag_index, schema_text = get_rag_index()

# Header metrics row (recruiter-friendly)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mode", "Write (Isolated)")
m2.metric("Grounding", "RAG (schema + dictionary)")
m3.metric("Output", "SQL + named params")
m4.metric("Execution", "Approval-gated")

st.divider()

# Main layout: left (request + context + generate), right (review + approve + execute)
left, right = st.columns([1.05, 1.25], gap="large")

with left:
    st.subheader("1) Describe the update")
    st.text_area(
        "Describe the database update you want to perform (natural language)",
        key="write_prompt",
        height=140,
        placeholder="Example: Set order status to completed for order_id 3",
    )

    # Retrieve context as user types (lightweight)
    if st.session_state["write_prompt"].strip():
        context = retrieve(rag_index, st.session_state["write_prompt"], k=3)
    else:
        context = ""

    st.session_state["retrieved_context"] = context

    with st.expander("Retrieved context (RAG)", expanded=False):
        st.code(context or "No context yet. Enter a write request above.", language="text")

    c1, c2 = st.columns([1, 1])
    with c1:
        generate = st.button("Generate Write SQL", type="primary", use_container_width=True)
    with c2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state["write_prompt"] = ""
        st.session_state["retrieved_context"] = ""
        st.session_state["write_sql_res"] = None
        st.session_state["confirm_execute"] = False
        st.session_state["backup_first"] = True
        st.rerun()

    if generate:
        if not st.session_state["write_prompt"].strip():
            st.warning("Please enter a write request first.")
        else:
            # IMPORTANT: We generate SQL but do NOT execute automatically.
            res = generate_write_sql(
                context=st.session_state["retrieved_context"],
                user_prompt=st.session_state["write_prompt"],
            )
            st.session_state["write_sql_res"] = res
            st.session_state["confirm_execute"] = False  # reset confirmation on new generation
            st.toast("Write SQL generated. Review carefully before executing.")

with right:
    st.subheader("2) Review & approve")

    res = st.session_state.get("write_sql_res", None)

    if not res:
        st.info("Generate Write SQL to review the query, parameters, and safety notes here.")
    else:
        # Compact “status” area (simple but professional)
        # We keep it minimal since you already have guardrails in generation.
        s1, s2 = st.columns([1, 1])
        s1.metric("Ready to execute", "Yes" if (res.sql and res.sql.strip()) else "No")
        s2.metric("Backup recommended", "Yes" if st.session_state["backup_first"] else "No")

        st.markdown("### Generated SQL")
        st.code(res.sql or "(empty)", language="sql")

        st.markdown("### Parameters (named)")
        st.code(json.dumps(res.params, indent=2), language="json")

        if res.safety_notes:
            st.markdown("### Safety notes")
            for note in res.safety_notes:
                st.write(f"- {note}")

        with st.expander("Raw model output (debug)", expanded=False):
            st.code(res.raw, language="json")

        st.divider()

        st.subheader("3) Execute (explicit confirmation required)")

        # Gate 1: explicit acknowledgement
        st.checkbox(
            "I reviewed the SQL and understand this will modify the database.",
            key="confirm_execute",
        )

        # Gate 2: optional backup (recommended on by default)
        st.checkbox(
            "Create DB backup before executing",
            key="backup_first",
        )

        # Execute button is disabled until user checks confirmation + SQL exists
        can_execute = bool(st.session_state["confirm_execute"]) and bool(
            res.sql and res.sql.strip()
        )
        execute = st.button("Execute Write", use_container_width=True, disabled=not can_execute)

        if execute:
            # Safety checks again (defense in depth)
            if not st.session_state["confirm_execute"]:
                st.error("Confirmation required before executing.")
            elif not res.sql or not res.sql.strip():
                st.error("No executable SQL was generated.")
            else:
                try:
                    if st.session_state["backup_first"]:
                        bkp = backup_db(db_path)
                        st.info(f"Backup created: {bkp.name}")

                    affected = execute_write(db_path, res.sql, res.params)
                    st.success(f"Write executed successfully. Rows affected: {affected}")
                except Exception as e:
                    st.error(f"Execution failed: {e}")
