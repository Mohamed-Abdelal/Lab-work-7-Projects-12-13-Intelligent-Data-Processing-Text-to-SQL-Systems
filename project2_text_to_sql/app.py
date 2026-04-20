import streamlit as st
import os
import pandas as pd
import sqlite3
from langchain_sql_utils import process_nl_to_sql

# --- Custom App Styling ---
st.set_page_config(page_title="Text-to-SQL System", layout="wide")

st.markdown("""
<style>
    .chat-bubble {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-bubble {
        background-color: #e3f2fd;
        border-left: 5px solid #1976d2;
    }
    .ai-bubble {
        background-color: #f5f5f5;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

st.title("Natural Language to Database Query System")
st.write("Ask questions in plain English, and watch LangChain translate them into SQL queries against the local Retail database.")

import tempfile

# Sidebar for Setup and API
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Groq API Key", type="password", help="Enter your Groq API key here.")
    
    st.markdown("---")
    st.header("Database Controls")
    uploaded_file = st.file_uploader("Upload Data Document (.csv, .db, .sqlite)", type=["csv", "db", "sqlite"])

    st.markdown("---")
    st.markdown("### Sample Questions")
    st.info("- How many customers do we have?\n"
            "- What is the total revenue from all orders?\n"
            "- Which product has the highest stock quantity?\n"
            "- List the first names of all customers who joined in 2023.\n"
            "- What is the total price of all order items for order ID 1?")

if uploaded_file is None:
    st.warning("Please upload a data document (.csv, .db, or .sqlite) from the sidebar to continue.")
else:
    # Save uploaded file to temp path
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        DB_PATH = tmp_file.name

    if file_ext == "csv":
        # Convert CSV to SQLite sample database dynamically
        try:
            df = pd.read_csv(uploaded_file)
            table_name = uploaded_file.name.split('.')[0].replace(" ", "_").lower()
            conn = sqlite3.connect(DB_PATH)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()
        except Exception as e:
            st.error(f"Failed to process CSV file into database: {e}")
            st.stop()
    else:
        # Save exact DB file to temp
        with open(DB_PATH, "wb") as f:
            f.write(uploaded_file.getvalue())
    # -----------------------------
    # Database Visualizer Expander
    # -----------------------------
    with st.expander("View Database Tables (Raw Data)"):
        conn = sqlite3.connect(DB_PATH)
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
        for table_name in tables['name'].tolist():
            if table_name != "sqlite_sequence":
                st.write(f"**Table: {table_name}**")
                df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)
                st.dataframe(df, use_container_width=True)
        conn.close()

    st.markdown("---")
    
    # -----------------------------
    # Query Interface
    # -----------------------------
    user_question = st.text_input("Ask a question about the Retail database:", placeholder="e.g., How many products are in the Electronics category?")

    if st.button("Generate & Run Query", type="primary"):
        if not api_key_input:
            st.error("Please provide a Groq API Key in the sidebar.")
        elif not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking... translating to SQL..."):
                sql_query, sql_result, final_answer, error_msg = process_nl_to_sql(
                    user_question, api_key_input, db_path=DB_PATH
                )

                if error_msg:
                    st.error(f"Error: {error_msg}")
                else:
                    # User Question
                    st.markdown(f"<div class='chat-bubble user-bubble'><b>You:</b> {user_question}</div>", unsafe_allow_html=True)
                    
                    # Layout for behind-the-scenes vs final answer
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("Generated SQL Query")
                        st.code(sql_query, language="sql")
                        
                        st.subheader("Raw Database Result")
                        st.write(sql_result)
                        
                    with col2:
                        st.subheader("Natural Language Response")
                        st.info(final_answer)
