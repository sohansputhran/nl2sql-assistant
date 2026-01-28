"""
Schema Explorer (Streamlit page)
--------------------------------
Purpose:
- Show the database schema in a prompt-ready format.
- Allow running a small sample SELECT query and view results.

"""

from pathlib import Path

import pandas as pd
import streamlit as st

from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.runner import run_query
from nl2sql_assistant.db.schema import schema_as_text

st.set_page_config(page_title="Schema Explorer", page_icon="🗄️", layout="wide")

st.title("Schema Explorer")

# We keep the DB in ./data so it's easy to ignore in git and regenerate anytime.
DB_PATH = Path("data/sample.db")

# Ensure DB exists and has sample data (idempotent)
ensure_sample_db(DB_PATH)

st.caption(f"Database: `{DB_PATH.as_posix()}`")

# Show schema text in a code block: we will reuse this exact text in prompts later.
with st.expander("Schema (prompt-ready text)", expanded=True):
    st.code(schema_as_text(DB_PATH), language="text")

st.subheader("Try a sample query")

# Default query helps confirm joins and table relationships are correct.
default_sql = """
SELECT
  c.name AS customer,
  o.order_id,
  o.order_date,
  o.status
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC
""".strip()

sql = st.text_area("SQL (SELECT-only for now)", value=default_sql, height=160)

col1, col2 = st.columns([1, 1])
with col1:
    # UI limit prevents huge queries from taking too long
    limit = st.number_input("Row limit", min_value=1, max_value=1000, value=200, step=50)

run = st.button("Run query")

if run:
    try:
        cols, rows = run_query(DB_PATH, sql, limit=int(limit))
        df = pd.DataFrame(rows, columns=cols)
        st.success(f"Returned {len(df)} rows.")
        st.dataframe(df, width='stretch')
    except Exception as e:
        # Show a clean error for invalid SQL or non-SELECT queries
        st.error(str(e))
