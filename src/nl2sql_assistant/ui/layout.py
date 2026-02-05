"""
Shared layout helpers.

Why:
- Streamlit apps look messy when each page sets its own layout inconsistently.
- Centralizing layout keeps the product feel consistent and reviewable.
"""

from __future__ import annotations

import streamlit as st


def set_app_config() -> None:
    # Wide layout feels more "dashboard-like" and less like a notebook.
    st.set_page_config(
        page_title="NL2SQL Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_base_css() -> None:
    """
    Minimal CSS only for spacing/typography polish.
    Keep it small: Streamlit changes DOM often; heavy CSS becomes brittle.
    """
    st.markdown(
        """
        <style>
          /* Reduce top padding */
          .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
          /* Make headings a bit tighter */
          h1, h2, h3 { letter-spacing: -0.01em; }
          /* Cleaner code blocks */
          pre { border-radius: 10px !important; }
          /* Sidebar spacing */
          section[data-testid="stSidebar"] > div { padding-top: 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    """
    Standard header used across pages.
    """
    st.title(title)
    st.caption(subtitle)
    st.divider()
