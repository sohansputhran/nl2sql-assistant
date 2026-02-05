"""
Home.py
------------
Purpose:
- This is the home page of the Streamlit app for NL2SQL Assistant.
- It provides an overview of the app and its features.

"""

import streamlit as st

from nl2sql_assistant.ui.layout import set_app_config, inject_base_css, page_header

set_app_config()
inject_base_css()

page_header(
    "NL2SQL Assistant",
    "Production-oriented NL -> SQL with schema grounding, guardrails, and isolated Write Mode (RAG + human approval).",
)

# --- Top summary (recruiter-focused) ---
c1, c2, c3 = st.columns(3)
c1.metric("Execution", "DB-aware (Read-only default)")
c2.metric("Safety", "Validation + Risk Classification")
c3.metric("Models", "Open-source via Ollama")

st.markdown(
    """
**What this is:** An open-source NL → SQL system built with **Python + Streamlit + LangChain + Ollama**.  
It supports **two capabilities**:
- **DB-aware NL → SQL (Executable)** for a known SQLite DB (schema-grounded, validated, guarded)
- **Generic NL → SQL (Non-executable)** for drafting SQL across dialects (SQLite/Postgres/MySQL)

**Core safety design:**  
- Read mode defaults to **SELECT-only** and blocks unsafe SQL  
- Write mode is **isolated**, **JSON-only generation**, strict validation, **human confirmation**, and transactional execution (with rollback/backup)
"""
)

st.divider()

# --- Page cards ---
st.subheader("App Pages")
st.caption("Start here: pick the mode you want. Each page follows the same safety-first workflow.")

left, right = st.columns(2)

with left:
    st.markdown("### DB-aware NL -> SQL (Read Mode)")
    st.write(
        "Ask questions about the SQLite database. The system uses the real schema to reduce hallucinations, "
        "validates SQL strictly, and executes **SELECT-only** queries by default."
    )
    st.page_link("app/pages/2_DB_Aware_NL2SQL.py", label="Open DB-aware NL -> SQL")

    st.markdown("### Generic NL -> SQL (Non-executable)")
    st.write(
        "Convert natural language into SQL **without assuming a database**. Choose a dialect "
        "(SQLite / PostgreSQL / MySQL) and optionally provide a schema for higher accuracy. Output is **SQL only**."
    )
    st.page_link("app/pages/4_Generic_NL2SQL.py", label="Open Generic NL -> SQL")

with right:
    st.markdown("### Write Mode (Isolated + Human Approval)")
    st.write(
        "Safely generate INSERT/UPDATE/DELETE with schema + data dictionary grounding via RAG. "
        "Uses **JSON-only** SQL generation, strict allowlists, risk classification, and requires **explicit approval** "
        "before running inside a transaction (with rollback/backup)."
    )
    st.page_link("app/pages/3_Write_Mode.py", label="Open Write Mode")

st.divider()

# --- “Why this is production-grade” section ---
st.subheader("Why this is production-oriented")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
**Reliability**
- Schema-aware prompting and grounding
- Strict SQL validation before execution
- Risk classification + guardrails

**Maintainability**
- Clear separation: read / write / generic logic
- CI-safe architecture (tests don’t require model downloads)
"""
    )

with col2:
    st.markdown(
        """
**Safety**
- Default SELECT-only execution
- Write mode requires:
  - intent detection
  - JSON-only generation
  - human-in-the-loop confirmation
  - transaction + rollback + backup

**Open-source**
- Local models via Ollama
- LangChain PromptTemplates & chains
"""
    )

st.caption("Tip: Start with DB-aware Read Mode, then explore Write Mode for guarded updates.")
