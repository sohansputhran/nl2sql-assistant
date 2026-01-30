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

get_rag_index()

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
- Repo structure
- Streamlit skeleton
- Ruff + Pytest
- GitHub Actions CI
"""
    )

st.info("When you see this page, Initial Stage is finished.")
