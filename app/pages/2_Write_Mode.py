import json
import os

import streamlit as st

from nl2sql_assistant.app_state import get_db_path, get_rag_index
from nl2sql_assistant.chains.write_sql_generator import generate_write_sql
from nl2sql_assistant.db.write_runner import backup_db, execute_write
from nl2sql_assistant.rag.retriever_bm25 import retrieve
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "✍️ Write Mode with RAG",
    "Generate INSERT/UPDATE/DELETE queries with retrieval-augmented context and explicit approval.",
)

# Sidebar with API key input
with st.sidebar:
    st.markdown("### 🔑 HuggingFace API")

    if "HUGGINGFACE_API_TOKEN" in st.secrets:
        st.success("✓ API key configured")
    else:
        api_key_input = st.text_input(
            "Enter API Token",
            type="password",
            help="Get your token from https://huggingface.co/settings/tokens",
            placeholder="hf_...",
        )

        if api_key_input:
            os.environ["HUGGINGFACE_API_TOKEN"] = api_key_input
            st.success("✓ API key set for session")
        else:
            st.warning("⚠ API key required")

    st.divider()

    st.markdown("### 🧭 Navigation")
    st.caption(
        "**DB-aware Query** - Ask questions about your database\n\n"
        "**Write Mode** - Insert/update/delete with RAG\n\n"
        "**Generic SQL** - Draft SQL for any dialect"
    )

    st.divider()

    st.markdown("### 🛡️ Safety")
    st.caption(
        "✓ Read queries are SELECT-only\n\n"
        "✓ Write operations require approval\n\n"
        "✓ Automatic schema validation"
    )

# Session state defaults
st.session_state.setdefault("write_prompt", "")
st.session_state.setdefault("retrieved_context", "")
st.session_state.setdefault("write_sql_res", None)
st.session_state.setdefault("confirm_execute", False)
st.session_state.setdefault("backup_first", True)

# Data / index
db_path = get_db_path()
rag_index, schema_text = get_rag_index()

# --- Info banner ---
st.info(
    "💡 **Write Mode**: Safely modify your database using RAG-grounded SQL generation. "
    "Uses schema + data dictionary retrieval for context-aware queries. **Explicit confirmation required** before execution."
)

st.markdown("<br>", unsafe_allow_html=True)

# Main layout
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### 1️⃣ Describe Your Update")
    st.text_area(
        "What would you like to insert, update, or delete?",
        key="write_prompt",
        height=120,
        placeholder="Example: Set order status to 'completed' for order_id 3",
    )

    # Retrieve context as user types (lightweight)
    if st.session_state["write_prompt"].strip():
        context = retrieve(rag_index, st.session_state["write_prompt"], k=3)
    else:
        context = ""

    st.session_state["retrieved_context"] = context

    with st.expander("🔍 Retrieved Context (RAG)", expanded=False):
        st.code(context or "No context yet. Enter a write request above.", language="text")

    col_gen, col_clear = st.columns([2, 1])
    with col_gen:
        generate = st.button("🚀 Generate Write SQL", type="primary", use_container_width=True)
    with col_clear:
        clear = st.button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state["write_prompt"] = ""
        st.session_state["retrieved_context"] = ""
        st.session_state["write_sql_res"] = None
        st.session_state["confirm_execute"] = False
        st.session_state["backup_first"] = True
        st.rerun()

    if generate:
        if not st.session_state["write_prompt"].strip():
            st.warning("⚠️ Please enter a write request first.")
        else:
            with st.spinner("🔮 Generating write SQL with RAG context..."):
                res = generate_write_sql(
                    context=st.session_state["retrieved_context"],
                    user_prompt=st.session_state["write_prompt"],
                )
                st.session_state["write_sql_res"] = res
                st.session_state["confirm_execute"] = False
            st.toast("✅ Write SQL generated. Review carefully before executing.")
            st.rerun()

with right:
    st.markdown("#### 2️⃣ Review & Approve")

    res = st.session_state.get("write_sql_res", None)

    if not res:
        st.info("👈 Generate Write SQL to review the query, parameters, and safety notes here.")
    else:
        st.markdown("**📝 Generated SQL**")
        st.code(res.sql or "(empty)", language="sql")

        st.markdown("**🔧 Parameters (Named)**")
        st.code(json.dumps(res.params, indent=2), language="json")

        if res.safety_notes:
            st.markdown("**⚠️ Safety Notes**")
            for note in res.safety_notes:
                st.warning(f"• {note}")

        with st.expander("🐛 Raw Model Output (Debug)", expanded=False):
            st.code(res.raw, language="json")

        st.markdown("---")

        st.markdown("#### 3️⃣ Execute (Confirmation Required)")

        # Gate 1: explicit acknowledgement
        st.checkbox(
            "✓ I reviewed the SQL and understand this will modify the database",
            key="confirm_execute",
        )

        # Gate 2: optional backup (recommended on by default)
        st.checkbox(
            "✓ Create database backup before executing (recommended)",
            key="backup_first",
        )

        # Execute button
        can_execute = bool(st.session_state["confirm_execute"]) and bool(
            res.sql and res.sql.strip()
        )
        execute = st.button(
            "▶️ Execute Write Operation",
            use_container_width=True,
            type="primary",
            disabled=not can_execute,
        )

        if execute:
            if not st.session_state["confirm_execute"]:
                st.error("❌ Confirmation required before executing.")
            elif not res.sql or not res.sql.strip():
                st.error("❌ No executable SQL was generated.")
            else:
                try:
                    if st.session_state["backup_first"]:
                        with st.spinner("💾 Creating backup..."):
                            bkp = backup_db(db_path)
                        st.success(f"✅ Backup created: {bkp.name}")

                    with st.spinner("⚙️ Executing write operation..."):
                        affected = execute_write(db_path, res.sql, res.params)

                    st.success(f"✅ Write executed successfully! Rows affected: {affected}")

                    # Reset confirmation after successful execution
                    st.session_state["confirm_execute"] = False

                except Exception as e:
                    st.error(f"❌ Execution failed: {e}")
