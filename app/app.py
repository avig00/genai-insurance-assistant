# import streamlit as st
# import sys
# from pathlib import Path
# import time
# import sqlparse
# import io

# # Add project root to path
# root_dir = Path(__file__).resolve().parent.parent
# sys.path.append(str(root_dir))

# from llm.text2sql_agent import generate_sql
# from backend.query_executor import run_sql_query

# # --------------------------
# # Page Config
# # --------------------------
# st.set_page_config(
#     page_title="GenAI SQL Assistant",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # --------------------------
# # Sidebar History
# # --------------------------
# with st.sidebar:
#     st.title("History")

#     if st.button("Start New Chat"):
#         st.session_state.history = []
#         st.session_state.generated_sql = None
#         st.session_state.query_result = None
#         st.session_state.view_mode = None
#         st.session_state.last_question = None

#     if "history" not in st.session_state:
#         st.session_state.history = []

#     if st.session_state.history:
#         for q, s in reversed(st.session_state.history[-10:]):
#             with st.expander(q):
#                 st.code(s, language="sql")
#     else:
#         st.write("No history yet.")

# # --------------------------
# # Custom Styling
# # --------------------------
# st.markdown(
#     """
#     <style>
#         .big-title {
#             font-size: 2.6rem;
#             font-weight: 700;
#             color: #29B5E8;
#             margin-bottom: 0.2em;
#         }
#         .subtext {
#             font-size: 1.15rem;
#             color: #4a4a4a;
#             margin-bottom: 2em;
#         }
#         .stTextInput input {
#             font-size: 1.1rem !important;
#             padding: 0.6em !important;
#         }
#         pre code {
#             font-family: 'Courier New', monospace;
#             font-size: 1rem;
#             line-height: 1.5;
#             background-color: #f8f9fa;
#             padding: 1em;
#             border-radius: 6px;
#             white-space: pre-wrap;
#             display: block;
#             overflow-x: auto;
#             color: #333;
#         }
#         div.stButton > button {
#             background-color: #29B5E8 !important;
#             color: white !important;
#             border: none !important;
#             border-radius: 6px;
#             padding: 0.5em 1.5em;
#             font-size: 1rem;
#             font-weight: 600;
#         }
#         div.stButton > button:hover {
#             background-color: #199FD6 !important;
#             transform: scale(1.02);
#             transition: 0.1s ease-in-out;
#         }
#         div.stButton > button:active {
#             background-color: #147BA7 !important;
#             transform: scale(0.98);
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # --------------------------
# # Header
# # --------------------------
# st.markdown('<div class="big-title">GenAI SQL Assistant for Insurance</div>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="subtext" style="color: white;">Ask a question in plain English. The assistant will generate SQL for your insurance dataset.</div>',
#     unsafe_allow_html=True
# )

# # --------------------------
# # Input Box
# # --------------------------
# question = st.text_input(
#     "Your Question",
#     placeholder="e.g., What is the average claim amount by line of business for closed claims?",
#     help="Ask a natural language question. The model will return SQL using your schema."
# )

# # --------------------------
# # SQL Generation with Caching
# # --------------------------
# if question:
#     if "last_question" not in st.session_state or st.session_state.last_question != question:
#         with st.spinner("Generating SQL..."):
#             time.sleep(0.5)
#             try:
#                 sql = generate_sql(question)
#                 st.success("Generated SQL:")
#                 formatted_sql = sqlparse.format(sql, reindent=True, keyword_case="upper")
#                 st.markdown(f"<pre><code class='language-sql'>{formatted_sql}</code></pre>", unsafe_allow_html=True)

#                 st.session_state.history.append((question, sql))
#                 st.session_state.generated_sql = sql
#                 st.session_state.last_question = question

#             except Exception as e:
#                 st.error(f"Error generating SQL: {str(e)}")
#                 if "model_pending_deploy" in str(e):
#                     st.info("The model is warming up. Please wait 1–2 minutes and try again.")
#     else:
#         sql = st.session_state.generated_sql
#         st.success("Generated SQL:")
#         formatted_sql = sqlparse.format(sql, reindent=True, keyword_case="upper")
#         st.markdown(f"<pre><code class='language-sql'>{formatted_sql}</code></pre>", unsafe_allow_html=True)

#     if "generated_sql" in st.session_state:
#         if st.button("Run Query"):
#             with st.spinner("Running SQL..."):
#                 try:
#                     df = run_sql_query(st.session_state.generated_sql)
#                     st.success("Query executed successfully!")
#                     st.dataframe(df, use_container_width=True, height=500)
#                     st.session_state.query_result = df

#                     st.markdown("### What would you like to do with the results?")
#                     col1, col2, col3 = st.columns(3)

#                     with col1:
#                         st.markdown("<div style='padding: 8px;'></div>", unsafe_allow_html=True)
#                         if st.button("📝 Submit Another Query"):
#                             st.session_state.followup_mode = True

#                     with col2:
#                         st.markdown("<div style='padding: 8px;'></div>", unsafe_allow_html=True)
#                         if st.button("📊 Visualize This Data"):
#                             st.session_state.view_mode = "visualize"

#                     with col3:
#                         st.markdown("<div style='padding: 16px;'></div>", unsafe_allow_html=True)
#                         if st.button("🤖 Train/Test ML Model"):
#                             st.session_state.view_mode = "ml_model"
#                 except Exception as e:
#                     st.error(f"❌ Query failed: {e}")

# # --------------------------
# # Follow-up Query Mode
# # --------------------------
# # if st.session_state.get("view_mode") == "ask_on_result":
# #     df = st.session_state.get("query_result")
# #     if df is not None:
# #         st.markdown("### Ask a follow-up question about the query result:")
# #         followup_question = st.text_input("Your Follow-up Question")

# #         if followup_question and st.button("Generate Follow-up SQL"):
# #             with st.spinner("Generating follow-up SQL..."):
# #                 try:
# #                     previous_sql = st.session_state.get("generated_sql", "")
# #                     followup_sql = generate_sql(followup_question, context_sql=previous_sql)

# #                     st.success("Follow-up SQL generated:")
# #                     formatted_sql = sqlparse.format(followup_sql, reindent=True, keyword_case="upper")
# #                     st.markdown(f"<pre><code class='language-sql'>{formatted_sql}</code></pre>", unsafe_allow_html=True)

# #                     st.session_state.history.append((followup_question, followup_sql))
# #                     st.session_state.generated_sql = followup_sql
# #                     st.session_state.last_question = followup_question
# #                 except Exception as e:
# #                     st.error(f"❌ Failed to generate follow-up SQL: {e}")

# #         if "generated_sql" in st.session_state:
# #             if st.button("Run Follow-up Query"):
# #                 with st.spinner("Running SQL..."):
# #                     try:
# #                         df = run_sql_query(st.session_state.generated_sql)
# #                         st.success("Follow-up query executed successfully!")
# #                         st.dataframe(df, use_container_width=True, height=500)
# #                         st.session_state.query_result = df
# #                         st.session_state.view_mode = None
# #                     except Exception as e:
# #                         st.error(f"❌ Follow-up query failed: {e}")

# # --------------------------
# # Follow-up Input Area
# # --------------------------
# if st.session_state.get("followup_mode") and st.session_state.get("query_result") is not None:
#     st.markdown("---")
#     st.markdown("### Ask a follow-up question about the query result:")
#     followup_question = st.text_input("Your Follow-up Question")

#     if followup_question and st.button("Generate Follow-up SQL"):
#         with st.spinner("Generating follow-up SQL..."):
#             try:
#                 previous_sql = st.session_state.get("generated_sql", "")
#                 followup_sql = generate_sql(followup_question, context_sql=previous_sql)

#                 st.success("Follow-up SQL generated:")
#                 formatted_sql = sqlparse.format(followup_sql, reindent=True, keyword_case="upper")
#                 st.markdown(f"<pre><code class='language-sql'>{formatted_sql}</code></pre>", unsafe_allow_html=True)

#                 st.session_state.history.append((followup_question, followup_sql))
#                 st.session_state.generated_sql = followup_sql
#                 st.session_state.last_question = followup_question
#             except Exception as e:
#                 st.error(f"❌ Failed to generate follow-up SQL: {e}")

#     if "generated_sql" in st.session_state:
#         if st.button("Run Follow-up Query"):
#             with st.spinner("Running SQL..."):
#                 try:
#                     df = run_sql_query(st.session_state.generated_sql)
#                     st.success("Follow-up query executed:")
#                     st.dataframe(df, use_container_width=True, height=500)
#                     st.session_state.query_result = df
#                     st.session_state.followup_mode = False  # ready for next turn
#                 except Exception as e:
#                     st.error(f"❌ Follow-up query failed: {e}")

