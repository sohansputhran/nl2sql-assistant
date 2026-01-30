import json

import streamlit as st

from nl2sql_assistant.app_state import get_db_path, get_rag_index
from nl2sql_assistant.chains.write_sql_generator import generate_write_sql
from nl2sql_assistant.db.write_runner import backup_db, execute_write
from nl2sql_assistant.rag.retriever_bm25 import retrieve

st.set_page_config(page_title="Write Mode (RAG)", layout="wide")

st.title("Write Mode (RAG)")
st.caption(
    "Generates INSERT/UPDATE/DELETE using retrieved context. Requires explicit confirmation."
)

db_path = get_db_path()
rag_index, schema_text = get_rag_index()

user_prompt = st.text_area(
    "Describe the database update you want to perform (natural language)",
    height=120,
    placeholder="Example: Set order status to completed for order_id 3",
)

# Stage 5: show retrieved context so user can verify the model is grounded.
if user_prompt.strip():
    context = retrieve(rag_index, user_prompt, k=3)
else:
    context = ""

with st.expander("Retrieved context (RAG)", expanded=False):
    st.code(context or "No context yet. Enter a write request above.", language="text")

generate = st.button("Generate Write SQL")

if generate:
    if not user_prompt.strip():
        st.warning("Please enter a write request first.")
    else:
        # IMPORTANT: We generate SQL but do NOT execute it automatically.
        res = generate_write_sql(context=context, user_prompt=user_prompt)
        st.session_state["write_sql_res"] = res

res = st.session_state.get("write_sql_res", None)

if res:
    st.subheader("Generated Write SQL (review carefully)")
    st.code(res.sql or "(empty)", language="sql")

    st.markdown("**Parameters (named)**")
    st.code(json.dumps(res.params, indent=2), language="json")

    if res.safety_notes:
        st.markdown("**Safety notes**")
        for note in res.safety_notes:
            st.write(f"- {note}")

    with st.expander("Raw model output (debug)", expanded=False):
        st.code(res.raw, language="json")

    st.divider()

    st.subheader("Execute (explicit confirmation required)")

    # Stage 5 safety pattern: require explicit acknowledgement.
    confirm = st.checkbox("I reviewed the SQL and understand this will modify the database.")

    backup_first = st.checkbox("Create DB backup before executing", value=True)

    execute = st.button("Execute Write")

    if execute:
        if not confirm:
            st.error("Confirmation required before executing.")
        elif not res.sql.strip():
            st.error("No executable SQL was generated.")
        else:
            try:
                if backup_first:
                    bkp = backup_db(db_path)
                    st.info(f"Backup created: {bkp.name}")

                affected = execute_write(db_path, res.sql, res.params)
                st.success(f"Write executed successfully. Rows affected: {affected}")
            except Exception as e:
                st.error(f"Execution failed: {e}")
