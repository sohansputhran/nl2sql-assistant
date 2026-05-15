import os

import streamlit as st

from nl2sql_assistant.ui.layout import inject_base_css, page_header, set_app_config

set_app_config()
inject_base_css()

page_header(
    "🔮 NL2SQL Assistant",
    "Transform natural language into SQL queries with schema awareness and safety guardrails.",
)


# Sidebar with API key input
with st.sidebar:
    st.markdown("### 🔑 HuggingFace API")
    
    # Check if running on Streamlit Cloud (secrets available) or locally
    if "HUGGINGFACE_API_TOKEN" in st.secrets:
        st.success("✓ API key configured")
        api_key_status = "configured"
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
            api_key_status = "configured"
        else:
            st.warning("⚠ API key required")
            api_key_status = "missing"
    
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

# --- Hero section ---
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h2 style='color: #8B5CF6; margin-bottom: 0.5rem;'>Three Ways to Generate SQL</h2>
        <p style='color: #6B7280; font-size: 1.1rem;'>Choose the mode that fits your workflow</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Feature cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 320px;'>
            <h3 style='color: white; margin-bottom: 1rem;'>📊 DB-Aware Query</h3>
            <p style='color: #E9D5FF; line-height: 1.6;'>
                Ask questions about your connected database. Schema-grounded generation 
                eliminates hallucinations and ensures accurate SQL.
            </p>
            <p style='color: white; font-weight: 600; margin-top: 1.5rem;'>
                ✓ Auto-validation<br>
                ✓ Risk assessment<br>
                ✓ SELECT-only execution
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 320px;'>
            <h3 style='color: white; margin-bottom: 1rem;'>✍️ Write Mode</h3>
            <p style='color: #FEE2E2; line-height: 1.6;'>
                Generate INSERT/UPDATE/DELETE with RAG-based context retrieval. 
                Human approval required before execution.
            </p>
            <p style='color: white; font-weight: 600; margin-top: 1.5rem;'>
                ✓ RAG grounding<br>
                ✓ Explicit confirmation<br>
                ✓ Auto backup option
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 320px;'>
            <h3 style='color: white; margin-bottom: 1rem;'>🌐 Generic SQL</h3>
            <p style='color: #DBEAFE; line-height: 1.6;'>
                Draft SQL for any dialect without a connected database. 
                Perfect for learning or prototyping.
            </p>
            <p style='color: white; font-weight: 600; margin-top: 1.5rem;'>
                ✓ Multi-dialect support<br>
                ✓ Optional schema input<br>
                ✓ No execution (safe)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- Quick stats ---
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("🎯 Model", "SQLCoder-7B-2")
m2.metric("🔒 Security", "Multi-layer")
m3.metric("⚡ Validation", "Automatic")
m4.metric("🚀 Deployment", "Cloud-ready")

st.markdown("---")

# --- Getting started ---
st.markdown(
    """
    ### 🚀 Getting Started
    
    1. **Set up your API key** in the sidebar (if not using Streamlit Cloud secrets)
    2. **Choose a mode** from the navigation
    3. **Enter your query** in natural language
    4. **Review and execute** the generated SQL
    
    <br>
    """,
    unsafe_allow_html=True,
)

# --- Footer note ---
st.info(
    "💡 **Tip**: Start with DB-Aware Query mode to explore the sample database, "
    "then try Write Mode for data modifications with safety guardrails."
)