"""
Home.py
------------
Purpose:
- This is the home page of the Streamlit app for NL2SQL Assistant.
- It provides an overview of the app and its features.

"""

import streamlit as st

# Warm up cached resources so pages load fast and consistently.
from nl2sql_assistant.app_state import get_rag_index
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

get_rag_index()

set_app_config()
inject_base_css()
page_header(
    "NL2SQL Assistant",
    "Schema-aware NL → SQL with guardrails, RAG grounding, and isolated Write Mode.",
)


st.set_page_config(page_title="NL2SQL Assistant", page_icon="🧠", layout="wide")

st.title("NL2SQL Assistant")
st.write(
    """
This is the baseline Streamlit app with CI (ruff + pytest).

"""
)

with st.expander("Testing"):
    st.markdown(
        """
### Pages
- **Schema Explorer**: inspect DB schema and try sample queries.
- **NL → SQL (DB-aware)**: generate SQL for *this app’s database* and run it.
- **Write Mode (RAG)**: generate safe write SQL using retrieved context (human approval required).
- **Generic NL → SQL**: generate SQL for any request (not executed).
"""
    )

st.info("When you see this page, Initial Stage is finished.")
