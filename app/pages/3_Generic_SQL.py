import os

import streamlit as st

from nl2sql_assistant.chains.generic_sql_generator import generate_generic_sql
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "🌐 Generic SQL Generator",
    "Draft SQL queries for any dialect without connecting to a database. Perfect for learning and prototyping.",
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
st.session_state.setdefault("dialect", "SQLite")
st.session_state.setdefault("schema_optional", "")
st.session_state.setdefault("nl_request", "")
st.session_state.setdefault("generated_sql", "")

# --- Info banner ---
st.info(
    "💡 **Generic Mode**: Generate SQL for any dialect (SQLite, PostgreSQL, MySQL) without a connected database. "
    "Output is **not executed** - review and run in your own environment. Optionally provide schema for better accuracy."
)

st.markdown("<br>", unsafe_allow_html=True)

# Main layout
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### 1️⃣ Configure")

    st.selectbox(
        "SQL Dialect",
        ["SQLite", "PostgreSQL", "MySQL"],
        index=["SQLite", "PostgreSQL", "MySQL"].index(st.session_state["dialect"])
        if st.session_state["dialect"] in ["SQLite", "PostgreSQL", "MySQL"]
        else 0,
        key="dialect",
        help="Choose the SQL dialect you want to generate",
    )

    with st.expander("📋 Optional Schema (Recommended for Accuracy)", expanded=False):
        st.text_area(
            "Schema",
            key="schema_optional",
            height=140,
            placeholder="Example:\n\n"
            "CREATE TABLE customers (\n"
            "    customer_id INT PRIMARY KEY,\n"
            "    name VARCHAR(100),\n"
            "    email VARCHAR(100)\n"
            ");\n\n"
            "CREATE TABLE orders (\n"
            "    order_id INT PRIMARY KEY,\n"
            "    customer_id INT,\n"
            "    total DECIMAL(10,2)\n"
            ");",
            label_visibility="collapsed",
        )

    st.markdown("#### 2️⃣ Describe Your Query")
    st.text_area(
        "What would you like to query?",
        key="nl_request",
        height=100,
        placeholder="Example: Find top 5 products by revenue in the last 30 days",
        label_visibility="collapsed",
    )

    col_gen, col_clear = st.columns([2, 1])
    with col_gen:
        generate = st.button("🚀 Generate SQL", type="primary", use_container_width=True)
    with col_clear:
        clear = st.button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state["schema_optional"] = ""
        st.session_state["nl_request"] = ""
        st.session_state["generated_sql"] = ""
        st.rerun()

with right:
    st.markdown("#### 3️⃣ Generated SQL")
    st.caption(
        "⚠️ This SQL is **not executed**. Review and run it in your own database environment."
    )

    if not st.session_state["generated_sql"]:
        st.code("— Generate SQL to see the output here —", language="sql")
    else:
        st.code(st.session_state["generated_sql"], language="sql")

        # Download button
        st.download_button(
            "📥 Download SQL (.sql)",
            data=st.session_state["generated_sql"].encode("utf-8"),
            file_name=f"query_{st.session_state['dialect'].lower()}.sql",
            mime="text/sql",
            use_container_width=True,
        )

        # Copy to clipboard hint
        st.caption("💡 Tip: Click the copy button in the code block above to copy the SQL")

# Generation action
if generate:
    nl = st.session_state["nl_request"].strip()
    if not nl:
        st.warning("⚠️ Please enter a natural language request.")
    else:
        schema_text = st.session_state["schema_optional"].strip() or None

        with st.spinner(f"🔮 Generating {st.session_state['dialect']} SQL..."):
            res = generate_generic_sql(
                user_prompt=nl,
                dialect=st.session_state["dialect"],
                schema_text=schema_text,
            )
            st.session_state["generated_sql"] = res

        st.toast("✅ SQL generated!")
        st.rerun()
