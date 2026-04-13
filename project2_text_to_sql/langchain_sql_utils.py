import os
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def get_database(db_path: str = "sqlite:///retail.db") -> SQLDatabase:
    """Initializes and returns the SQLDatabase object."""
    return SQLDatabase.from_uri(db_path)

def process_nl_to_sql(question: str, api_key: str, model_name: str = "llama-3.3-70b-versatile", db_path: str = "retail.db"):
    """
    Takes a natural language question, converts it to SQL, runs it, and explains the result.
    Returns: (sql_query, sql_result, natural_language_explanation, error_msg)
    """
    if not api_key:
        return None, None, None, "Groq API Key is required."
        
    os.environ["GROQ_API_KEY"] = api_key
    
    if not os.path.exists(db_path):
        return None, None, None, f"Database file {db_path} not found. Please run setup_db.py first."

    llm = ChatGroq(model=model_name, temperature=0.0)
    db = get_database(f"sqlite:///{db_path}")

    # Step 1: Generate SQL Query
    # Using the standard LangChain sql query chain
    generate_query = create_sql_query_chain(llm, db)
    
    try:
        # Generate the raw sql
        sql_query = generate_query.invoke({"question": question})
        # Sometimes LLMs wrap SQL in markdown, clean it
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        # Basic query validation (Prevent destructive operations)
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "GRANT"]
        if any(keyword in sql_query.upper() for keyword in dangerous_keywords):
            return sql_query, None, None, "Generated query contains forbidden operations for this read-only application."

        # Step 2: Execute the Query
        try:
            sql_result = db.run(sql_query)
        except Exception as query_exec_err:
             return sql_query, None, None, f"Error executing query: {str(query_exec_err)}"

        # Step 3: Answer Synthesis
        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result, answer the user question in a natural, conversational way.
            If the SQL result is empty, say that no relevant information was found.
            
            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            
            Answer: """
        )
        
        answer_chain = (
            answer_prompt 
            | llm 
            | StrOutputParser()
        )
        
        final_answer = answer_chain.invoke({
            "question": question,
            "query": sql_query,
            "result": sql_result
        })

        return sql_query, sql_result, final_answer, None
        
    except Exception as e:
        return None, None, None, f"An unexpected error occurred pipeline: {str(e)}"
