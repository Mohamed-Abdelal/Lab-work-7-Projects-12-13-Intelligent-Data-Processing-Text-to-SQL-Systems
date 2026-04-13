# Project 2: Natural Language to Database Query System (Text-to-SQL)

This application demonstrates a LangChain-powered Text-to-SQL architecture. It allows users to ask questions about a database in plain English. The system translates the question into an executable SQL query, runs it against a local SQLite database, and returns a natural language answer explaining the outcome.

## Features
- Interactive Streamlit Chat-style interface.
- Automatically initializes a dummy SQLite Database (`retail.db`) with Customers, Products, Orders, and OrderItems.
- Read-only Query Validation to prevent destructive actions (DROP, DELETE).
- Visualizes the raw schema/tables for verification.
- Two-step LLM pipeline: (1) NLP to SQL and (2) SQL Results to Natural Language response.

## Setup Instructions

1. **Prerequisites**
   - Python 3.8+ installed.
   - A free Groq API key.

2. **Install Dependencies**
   Open your terminal in this directory (`project2_text_to_sql`) and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**
   You can either click the initialization button inside the Web UI, or run:
   ```bash
   python setup_db.py
   ```

## How to Run

Execute the Streamlit application:
```bash
streamlit run app.py
```

1. Enter your Groq API key in the sidebar.
2. Review the raw data tables by clicking "View Database Tables".
3. Try asking a sample question, such as: *"Which product has the highest stock quantity?"*
4. View the generated SQL query, raw database result, and the conversational response side-by-side.

## Example Use Cases
- Non-technical managers asking: *"Show me the total sales from October 2023."*
- Support staff asking: *"Who are the top 3 customers by total amount spent?"*
