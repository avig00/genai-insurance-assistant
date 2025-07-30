import streamlit as st
import sys
from pathlib import Path
import time
import sqlparse




# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from llm.text2sql_agent import generate_sql

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="GenAI SQL Assistant",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --------------------------
# Sidebar History
# --------------------------
with st.sidebar:
    st.title("History")

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        for q, s in reversed(st.session_state.history[-10:]):
            with st.expander(q):
                st.code(s, language="sql")
    else:
        st.write("No history yet.")

# --------------------------
# Custom Styling (Light Theme, Fixes Applied)
# --------------------------
st.markdown(
    """
    <style>
        .big-title {
            font-size: 2.6rem;
            font-weight: 700;
            color: #29B5E8;
            margin-bottom: 0.2em;
        }
        .subtext {
            font-size: 1.15rem;
            color: #4a4a4a;
            margin-bottom: 2em;
        }
        .stTextInput input {
            font-size: 1.1rem !important;
            padding: 0.6em !important;
        }
        pre code {
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            line-height: 1.5;
            background-color: #f8f9fa;
            padding: 1em;
            border-radius: 6px;
            white-space: pre-wrap;
            display: block;
            overflow-x: auto;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Header
# --------------------------
st.markdown('<div class="big-title">GenAI SQL Assistant for Insurance</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Ask a question in plain English. The assistant will generate SQL for your insurance dataset.</div>', unsafe_allow_html=True)

# --------------------------
# Input Box
# --------------------------
question = st.text_input(
    "Your Question",
    placeholder="e.g., What is the average claim amount by line of business for closed claims?",
    help="Ask a natural language question. The model will return SQL using your schema."
)

# --------------------------
# SQL Generation
# --------------------------
if question:
    with st.spinner("Generating SQL..."):
        time.sleep(0.5)
        try:
            sql = generate_sql(question)
            st.success("Generated SQL:")
            formatted_sql = sqlparse.format(sql, reindent=True, keyword_case="upper")
            st.markdown(f"<pre><code class='language-sql'>{formatted_sql}</code></pre>", unsafe_allow_html=True)

            st.session_state.history.append((question, sql))

            
            
        except Exception as e:
            st.error(f"Error generating SQL: {str(e)}")
