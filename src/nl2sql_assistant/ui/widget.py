"""
Reusable UI widgets: status chips, risk banners, section headers.
"""

from __future__ import annotations

import streamlit as st


def status_row(*, mode: str, executable: bool, risk: str, validated: bool) -> None:
    """
    A consistent status row: mode, executable status, risk, validation.

    Safety note:
    - Showing 'validated' + 'executable' clearly is a key UX guardrail.
    - Recruiters love seeing safety signals in the UI, not just in code.
    """
    c1, c2, c3, c4 = st.columns([1.1, 1.2, 1.0, 1.0])
    c1.metric("Mode", mode)
    c2.metric("Executable", "Yes" if executable else "No")
    c3.metric("Risk", risk.upper())
    c4.metric("Validated", "Pass" if validated else "Fail")


def info_callout(title: str, body: str) -> None:
    st.info(f"**{title}**\n\n{body}")


def danger_callout(title: str, body: str) -> None:
    st.error(f"**{title}**\n\n{body}")


def section(title: str) -> None:
    st.subheader(title)
