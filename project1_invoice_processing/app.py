import streamlit as st
import tempfile
import os
import pdfplumber
from langchain_utils import process_invoice_text

# --- Custom App Styling ---
st.set_page_config(page_title="Intelligent Invoice Processor", layout="wide")

st.markdown("""
<style>
    .result-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

st.title("Intelligent Invoice Processing System")
st.write("Upload an invoice document (PDF or Text), and our LangChain-powered system will extract structured financial data.")

# Sidebar for API Key and Settings
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Groq API Key", type="password", help="Enter your Groq API key here.")
    st.markdown("---")
    st.info("**Tip:** You can upload the included `sample_invoice.pdf` or `sample_invoice.txt` to test the system.")

uploaded_file = st.file_uploader("Choose an Invoice File", type=["pdf", "txt", "png", "jpg", "jpeg"])

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extr = page.extract_text()
            if extr:
                text += extr + "\n"
    return text

if uploaded_file is not None:
    if st.button("Process Invoice", type="primary"):
        if not api_key_input:
            st.error("Please provide a Groq API Key in the sidebar.")
        else:
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file to temp
                    with tempfile.NamedTemporaryFile(delete=False, suffix="."+uploaded_file.name.split('.')[-1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    raw_text = ""
                    if uploaded_file.name.lower().endswith(".pdf"):
                        raw_text = extract_text_from_pdf(tmp_path)
                    elif uploaded_file.name.lower().endswith(".txt"):
                        with open(tmp_path, "r", encoding="utf-8") as f:
                            raw_text = f.read()
                    elif uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
                        try:
                            import pytesseract
                            from PIL import Image
                            raw_text = pytesseract.image_to_string(Image.open(tmp_path))
                        except Exception as e:
                            st.error(f"Image text extraction failed. Please ensure Tesseract OCR is installed. Error: {e}")

                    # Process with LangChain
                    if not raw_text.strip():
                        st.error("Could not extract any text from the document. Please ensure it is a text-based PDF or TXT.")
                    else:
                        structured_data = process_invoice_text(raw_text, api_key_input)
                        
                        # Display Results
                        st.success("Invoice Processed Successfully!")
                        
                        # Validation Check
                        st.subheader("Extraction Summary")
                        if structured_data.is_valid:
                            st.success("**Validation:** The document appears to be a valid invoice, and data looks consistent.")
                        else:
                            st.warning("**Validation:** The document may be missing key fields or mathematically inconsistent.")

                        # Create columns for top level metrics
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Invoice Number", structured_data.invoice_number or "N/A")
                        col2.metric("Date", structured_data.date or "N/A")
                        col3.metric("Vendor", structured_data.vendor_name or "N/A")
                        col4.metric("Total Amount", f"${structured_data.total_amount:,.2f}" if structured_data.total_amount else "N/A")
                        
                        st.markdown("---")
                        
                        # Line Items
                        st.subheader("Line Items")
                        if structured_data.line_items:
                            import pandas as pd
                            # Convert pydantic line items to dict array
                            items_dict = [item.model_dump() for item in structured_data.line_items]
                            df = pd.DataFrame(items_dict)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("No line items detected.")
                        
                        # Raw JSON Output
                        with st.expander("View Raw JSON Output"):
                            st.json(structured_data.model_dump())

                    # Cleanup
                    os.unlink(tmp_path)
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")
