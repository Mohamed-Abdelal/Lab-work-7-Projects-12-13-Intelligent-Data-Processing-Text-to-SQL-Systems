# Intelligent Data Processing & Text-to-SQL Systems

This repository contains the deliverables for Lab 7 Projects 12 & 13. Below is the presentation breakdown detailing the system architecture, components, and challenges addressed during development.

---

## 1. System Architecture and Workflow

**Application 1 (Intelligent Invoice Processing System):**
*   **Workflow:** A user uploads an invoice (PDF or plain text) via the Streamlit GUI $\rightarrow$ The system uses `pdfplumber` to extract raw text $\rightarrow$ LangChain passes the text along with instructions to the Groq LLM (LLaMA-3) $\rightarrow$ The LLM utilizes `with_structured_output` to parse the text into strict predefined Pydantic schema formats $\rightarrow$ Streamlit displays the extracted JSON as a validated summary and formatted dataframe.
*   **Architecture Stack:** Streamlit (Frontend/UI) $\leftrightarrow$ LangChain Pipeline (Orchestration) $\leftrightarrow$ Pydantic (Data Validation & JSON enforcement) $\leftrightarrow$ Groq API (LLM Inference Engine).

**Application 2 (Natural Language to DB Query / Text-to-SQL):**
*   **Workflow:** A user inputs a plain English question via the Streamlit GUI $\rightarrow$ LangChain's `create_sql_query_chain` converts the question into valid SQL syntax tailored to the detected SQLite schema $\rightarrow$ The generated SQL script is audited for read-only safety (preventing `DROP`/`DELETE`) $\rightarrow$ It is executed against `retail.db` $\rightarrow$ The retrieved raw rows are passed back to the LLM to synthesize a natural conversational answer $\rightarrow$ Displayed to the user.
*   **Architecture Stack:** Streamlit (Frontend/UI) $\leftrightarrow$ SQLite DB (Data Storage) $\leftrightarrow$ LangChain Database Utilities (Orchestration & Context retrieval) $\leftrightarrow$ Groq API (LLM Inference Engine).

---

## 2. Key LangChain Components Used

*   **`ChatGroq`**: The core integration for utilizing Groq's high-speed, zero-latency inference models (`llama-3.3-70b-versatile`).
*   **`with_structured_output()`**: Crucial for the Invoice Processing system; it tightly constrains the LLM to return only fully formed JSON strings matching exact `Pydantic` models rather than raw conversational text.
*   **`SQLDatabase`**: Used in Application 2 to wrap the SQLite database connection out-of-the-box and allow LangChain to automatically inspect and read table schemas and indexes.
*   **`create_sql_query_chain`**: A built-in LangChain pipeline sequence in Application 2 that intelligently injects the database schema into the conversation prompt, ensuring the LLM generates context-aware and syntactically correct SQL.
*   **`ChatPromptTemplate`** & **`PromptTemplate`**: Used in both apps to inject robust system directives (like persona, error-handling instructions, and fallback formats).

---

## 3. Demonstration of Both Applications

*   **Demo 1 (Invoice Processing):** 
    Using a dummy PDF invoice containing different line items, totals, and vendors. We upload this PDF to our Streamlit UI and click "Process". The demonstration will actively show how unstructured text chunks are intelligently formatted into clear line-item tables and strict JSON trees, validating that the mathematical totals (Subtotal + Tax) align with the documents.
    
*   **Demo 2 (Text-to-SQL):** 
    After initiating `retail.db` using `setup_db.py`, we approach the query chat box with a business-centric request: *"What is the total revenue from all orders?*. Our UI visualizes the back-end workings—displaying the exact SQL query generated (`SELECT SUM(TotalAmount)...`) alongside the raw SQL output. Next to it, it dynamically presents the final LLM conversational wrap: *"The total revenue across all orders is $X."*

---

## 4. Challenges Faced and How They Were Solved

*   **Challenge:** *LLM output consistency in Invoice parsing.* Early plain text prompts often resulted in missing JSON keys, extra markdown, or hallucinated taxes.
    *   **Solution:** Transitioned the entire pipeline from basic string prompting to LangChain's `with_structured_output` coupled with `Pydantic`. This strictly enforced the schema, leaving no room for markdown errors.
*   **Challenge:** *PDF text extraction variability.* Depending on how PDFs are generated, the layout might throw line items across disparate formatting breaks before reaching the LLM.
    *   **Solution:** We pivoted to using the massive `llama-3.3-70b-versatile` model on Groq. Its higher reasoning capability cleanly organizes tangled text inputs without the heavy overhead of running slower OCR processes on the machine.
*   **Challenge:** *Preventing Destructive Queries in Text-to-SQL.* An LLM told to "generate a query" might unintentionally generate `DROP TABLE`, `UPDATE`, or `DELETE` statements if prompted maliciously by a user.
    *   **Solution:** We built a middleware validation layer into `langchain_sql_utils.py` that verifies the raw SQL string output, completely blocking the execution if any destructive operations are present, ensuring a Read-Only environment.

---

## 5. Example Use Cases

**Application 1: Intelligent Invoice Processing**
*   **Accounting Automation:** A bookkeeping department receives hundreds of inconsistent PDFs from different vendors weekly. This system acts as a standardizer, converting them all into a unified JSON schema for one-click entry into QuickBooks/SAP.
*   **Expense Claims:** Employees who submit travel receipts no longer need manual verifiers. The LLM immediately validates the existence of the vendor, subtotal, and total before saving the claim, rejecting unreadable blobs.

**Application 2: Text-to-SQL Database System**
*   **Non-Technical Business Dashboards:** A company's Marketing Director wants to know *"How many customers joined in October?"* or *"What is our top-selling product category?"* but doesn't know SQL. They can get up-to-the-second live data naturally, bypassing the engineering team.
*   **Inventory Auditing & Retail Operations:** Supervisors on a store floor can type queries like *"Which accessories are under 50 stock quantity?"* to get instantaneous data retrieval during audits without navigating complex software menus.
