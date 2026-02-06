import streamlit as st

from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "NL2SQL Assistant",
    "Production-oriented NL -> SQL with schema grounding, guardrails, and isolated Write Mode (RAG + human approval).",
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

# --- Recruiter-friendly summary ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Modes", "DB-aware + Generic")
c2.metric("Execution", "Read-only by default")
c3.metric("Write Safety", "Isolated + approval")
c4.metric("Models", "Open-source (Ollama)")

st.markdown(
    """
**What this is:** An open-source NL -> SQL system built with **Python + Streamlit + LangChain + Ollama**.
It supports **two capabilities**:

- **DB-aware NL -> SQL (Executable)**: converts NL to SQL for a known SQLite database using the *real schema* to reduce hallucinations.
- **Generic NL -> SQL (Non-executable)**: drafts SQL for multiple dialects without assuming a database.
**Safety-first design (core guarantees):**
- Default is **SELECT-only** execution with strict SQL validation.
- A separate **Write Mode** supports INSERT/UPDATE/DELETE with **JSON-only generation**, strict rules, and **human confirmation** before execution.
"""
)

st.divider()

# --- Pages overview (no links) ---
st.subheader("Pages Overview")
st.caption(
    "Use the sidebar to navigate. Each page is designed with consistent safety signals and validation steps."
)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### DB-aware NL -> SQL (Read Mode)")
    st.write(
        """
Ask questions about the connected SQLite database.  
The system grounds generation using the database schema, applies risk classification, and validates SQL strictly.
**Execution is SELECT-only by default.**
"""
    )

    st.markdown("### Generic NL -> SQL (Non-executable)")
    st.write(
        """
Convert natural language into SQL **without** connecting to a database.  
Supports selecting a SQL dialect (SQLite / PostgreSQL / MySQL) and optional schema input for accuracy.
**Outputs SQL only; never executes.**
"""
    )

with col_right:
    st.markdown("### Write Mode (Isolated + Human Approval)")
    st.write(
        """
Safely generate INSERT/UPDATE/DELETE using schema + data dictionary grounding via RAG.
Designed for production guardrails:
- intent detection (read vs write)
- **JSON-only** SQL generation
- strict allowlist validation
- human-in-the-loop confirmation
- transaction + rollback + database backup
"""
    )

st.divider()

# --- Why production-oriented (recruiter section) ---
st.subheader("Why this is production-oriented")

a, b = st.columns(2)
with a:
    st.markdown(
        """
**Reliability**
- Schema-grounded prompting to reduce hallucinations  
- Strict SQL validation and risk classification  
- Clear separation of read/write/generic logic  

**Maintainability**
- Clean repo structure and modular components  
- CI-safe design (tests don't require model downloads)
"""
    )

with b:
    st.markdown(
        """
**Safety**
- Read mode defaults to SELECT-only  
- Write mode is isolated and gated by approval  
- Transaction + rollback + backups for destructive operations  

**Open-source**
- Local LLMs via Ollama  
- LangChain PromptTemplates and chains
"""
    )

st.caption("Navigate using the sidebar to start with DB-aware Read Mode.")
