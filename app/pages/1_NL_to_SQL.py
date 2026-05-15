import os
from pathlib import Path

import pandas as pd
import streamlit as st

from nl2sql_assistant.chains.risk_classifier import classify_risk
from nl2sql_assistant.chains.sql_generator import generate_sql
from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.runner import run_query, validate_sql
from nl2sql_assistant.db.schema import schema_as_text
from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "📊 DB-Aware Query",
    "Ask questions about your database in natural language. Auto-validated with schema grounding.",
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

# --- Session state defaults ---
st.session_state.setdefault("question", "Show completed orders with customer name, newest first.")
st.session_state.setdefault("generated_sql", "")
st.session_state.setdefault("risk", "unknown")
st.session_state.setdefault("risk_result", None)
st.session_state.setdefault("validated", False)
st.session_state.setdefault("executable", False)
st.session_state.setdefault("validation_msg", "")
st.session_state.setdefault("result_df", None)

# --- Info banner ---
st.info(
    "💡 **How it works**: Enter your question → SQL is generated with schema awareness → "
    "Automatic validation & risk check → Execute safely (SELECT-only)"
)

st.markdown("<br>", unsafe_allow_html=True)

DB_PATH = Path("data/sample.db")
ensure_sample_db(DB_PATH)

schema_text = schema_as_text(DB_PATH)

# --- Main layout ---
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### 1️⃣ Ask Your Question")
    st.text_area(
        "Question",
        key="question",
        placeholder="e.g., List top 10 customers by total spend in 2024",
        label_visibility="collapsed",
        height=100,
    )

    # Schema expander
    with st.expander("📋 View Database Schema", expanded=False):
        st.code(schema_text, language="sql")

    # Actions
    col_gen, col_clear = st.columns([2, 1])
    with col_gen:
        gen = st.button("🚀 Generate SQL", type="primary", width="stretch")
    with col_clear:
        clear = st.button("🗑️ Clear", width="stretch")

    if clear:
        st.session_state["generated_sql"] = ""
        st.session_state["risk"] = "unknown"
        st.session_state["validated"] = False
        st.session_state["executable"] = False
        st.session_state["validation_msg"] = ""
        st.session_state["result_df"] = None
        st.rerun()

    if gen:
        with st.spinner("🔮 Generating SQL..."):
            res = generate_sql(schema_text=schema_text, question=st.session_state["question"])
            st.session_state["generated_sql"] = res.sql
            st.session_state["notes"] = res.notes

        # Automatic validation
        with st.spinner("🔍 Validating SQL..."):
            ok, msg = validate_sql(sql=st.session_state["generated_sql"], mode="read")
            st.session_state["validated"] = ok
            st.session_state["executable"] = ok
            st.session_state["validation_msg"] = msg

        # Automatic risk check
        with st.spinner("🛡️ Running risk assessment..."):
            risk_result = classify_risk(
                schema_text=schema_text,
                question=st.session_state["question"],
                sql=st.session_state["generated_sql"],
            )
            
            # Extract risk level string from RiskResult object
            if hasattr(risk_result, 'risk'):
                # Direct attribute access
                risk_level = str(risk_result.risk)
            else:
                # Parse from string representation
                import re
                risk_str = str(risk_result)
                match = re.search(r"RISK_LEVEL='([^']+)'", risk_str)
                if match:
                    risk_level = match.group(1)
                else:
                    # Last resort: try to find risk level in string
                    risk_str_lower = risk_str.lower()
                    if 'low' in risk_str_lower:
                        risk_level = 'low'
                    elif 'medium' in risk_str_lower:
                        risk_level = 'medium'
                    elif 'high' in risk_str_lower:
                        risk_level = 'high'
                    else:
                        risk_level = 'unknown'
            
            st.session_state["risk"] = risk_level
            st.session_state["risk_result"] = risk_result

        st.rerun()

with right:
    st.markdown("#### 2️⃣ Review Generated SQL")

    # SQL editor
    st.session_state["generated_sql"] = st.text_area(
        "Generated SQL",
        value=st.session_state["generated_sql"],
        height=180,
        placeholder="Click 'Generate SQL' to create a query...",
        label_visibility="collapsed",
    )

    # Validation status
    if st.session_state["validation_msg"]:
        if st.session_state["validated"]:
            st.success(f"✅ {st.session_state['validation_msg']}")
        else:
            st.error(f"❌ {st.session_state['validation_msg']}")

    # Risk assessment display
    if st.session_state["risk"] != "unknown":
        # Get the full risk result object if available
        risk_result_obj = st.session_state.get("risk_result", None)
        
        # Try to extract clean risk level from the object
        risk_level = "unknown"
        flags = []
        suggestions = []
        
        if risk_result_obj:
            # If it's an object with 'risk' attribute
            if hasattr(risk_result_obj, 'risk'):
                risk_level = str(risk_result_obj.risk).lower()
            else:
                # It might be a string representation, try to parse it
                risk_str = str(risk_result_obj)
                if "RISK_LEVEL=" in risk_str:
                    # Extract from string like "RISKRESULT(RISK_LEVEL='MEDIUM', ...)"
                    import re
                    match = re.search(r"RISK_LEVEL='([^']+)'", risk_str)
                    if match:
                        risk_level = match.group(1).lower()
            
            # Try to extract flags
            if hasattr(risk_result_obj, 'flags') and risk_result_obj.flags:
                flags = risk_result_obj.flags
            
            # Try to extract suggestions  
            if hasattr(risk_result_obj, 'suggestions') and risk_result_obj.suggestions:
                suggestions = risk_result_obj.suggestions
        
        # Fallback: use the stored risk string
        if risk_level == "unknown" and st.session_state["risk"] != "unknown":
            risk_level = str(st.session_state["risk"]).lower()
        
        # Color coding
        risk_colors = {
            "low": ("🟢", "#10B981", "#ECFDF5"),
            "medium": ("🟡", "#F59E0B", "#FFFBEB"),
            "high": ("🔴", "#EF4444", "#FEF2F2"),
        }
        emoji, border_color, bg_color = risk_colors.get(risk_level, ("⚪", "#6B7280", "#F9FAFB"))
        
        # Create styled risk card
        st.markdown(
            f"""
            <div style='
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            '>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='font-size: 1.5rem;'>{emoji}</span>
                    <strong style='color: {border_color}; font-size: 1.1rem;'>Risk Level: {risk_level.upper()}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Execute button
    st.markdown("#### 3️⃣ Execute Query")
    execute_btn = st.button(
        "▶️ Execute (SELECT only)",
        width="stretch",
        type="primary",
        disabled=not st.session_state["validated"],
    )

    if execute_btn:
        with st.spinner("⚙️ Executing query..."):
            cols, rows = run_query(DB_PATH, st.session_state["generated_sql"], limit=200)
            df = pd.DataFrame(rows, columns=cols)
            st.session_state["result_df"] = df
        st.rerun()

st.markdown("---")

# --- Results area ---
st.markdown("#### 📊 Query Results")
if st.session_state["result_df"] is None:
    st.caption("Execute a validated query to see results here.")
else:
    st.dataframe(st.session_state["result_df"], width="stretch")
    
    # Download option
    csv = st.session_state["result_df"].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv",
    )