# Project 2: Natural Language to Database Query System (Text-to-SQL)

This application demonstrates a LangChain-powered Text-to-SQL architecture. It allows users to ask questions about a database in plain English. The system translates the question into an executable SQL query, runs it against a local SQLite database, and returns a natural language answer explaining the outcome.

## Features
- Interactive Streamlit Chat-style interface.
- Dynamically creates sample databases from uploaded flat files (.csv) or queries uploaded SQLite databases (.db/.sqlite).
- Read-only Query Validation to prevent destructive actions (DROP, DELETE).
- Robust SQL purification pipeline trims out chatty LLM prompts or trailing instructions to prevent SQLite syntax crashes.
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

3. **Upload your Database Document**
   You do not need hardcoded databases; just upload a `retail.csv` or standard `.db` to dynamically generate your tables over the Streamlit UI!

## How to Run

Execute the Streamlit application:
```bash
streamlit run app.py
```

1. Enter your Groq API key in the sidebar.
2. Upload your data document (`retail.csv` or `.db`) via the sidebar.
3. Review the generated raw data tables by clicking "View Database Tables".
4. Try asking a sample question based on your uploaded data!
5. View the generated SQL query, raw database result, and the conversational response side-by-side.

## Example Use Cases
- Non-technical managers asking: *"Show me the total sales from October 2023."*
- Support staff asking: *"Who are the top 3 customers by total amount spent?"*
