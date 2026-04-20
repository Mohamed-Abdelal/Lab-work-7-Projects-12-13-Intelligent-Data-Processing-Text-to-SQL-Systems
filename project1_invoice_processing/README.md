# Project 1: Intelligent Invoice Processing System

This project is an advanced LangChain application that processes invoices (PDF, Image, or Text) and extracts structured financial information (like invoice numbers, vendors, totals, and line items) using a Large Language Model (LLM) via Groq.

## Features
- Upload PDF, Image (PNG/JPG), or TXT invoices through a clean Streamlit interface.
- Extracts information reliably using LangChain's `with_structured_output` and Pydantic models.
- Robust dictionary fallback logic properly intercepts unstructured LLM generation arrays safely preventing 400 schema mismatch errors.
- Performs basic consistency checks (validates the outputs).
- Presents table layouts for line items and an expandable JSON view for raw data.

## Setup Instructions

1. **Prerequisites**
   - Python 3.8+ installed.
   - Tesseract-OCR installed on your system (Required for Image parsing).
   - A free Groq API key (get one from [Groq Console](https://console.groq.com/)).

2. **Install Dependencies**
   Open your terminal in this directory (`project1_invoice_processing`) and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Use Sample Data**
   We have included `sample_invoice.pdf` and `sample_invoice.txt` in the folder for you to quickly test the application.

## How to Run

Execute the Streamlit application:
```bash
streamlit run app.py
```

1. Open the provided Local URL in your browser.
2. In the sidebar, paste your Groq API Key.
3. Upload an invoice file.
4. Click **Process Invoice** and view the structured results.

## Example Inputs and Outputs

**Input:** A PDF containing Acme Corp billing John Doe for "Widget A" ($30), "Service B" ($100), and "Consulting" ($150).

**Output:**
```json
{
  "invoice_number": "INV-2023-001",
  "date": "2023-10-25",
  "vendor_name": "Acme Corp",
  "customer_name": "John Doe",
  "subtotal": 280.0,
  "tax_amount": 28.0,
  "total_amount": 308.0,
  "line_items": [
    {
      "description": "Widget A",
      "quantity": 2.0,
      "unit_price": 15.0,
      "total_price": 30.0
    },
    ...
  ],
  "is_valid": true
}
```
