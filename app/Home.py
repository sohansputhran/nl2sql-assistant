import streamlit as st

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
