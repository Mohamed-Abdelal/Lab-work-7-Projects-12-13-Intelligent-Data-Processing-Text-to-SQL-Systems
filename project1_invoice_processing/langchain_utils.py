import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Define Pydantic models for structured output
class LineItem(BaseModel):
    description: str = Field(description="Description of the item or service", default="")
    quantity: float = Field(description="Quantity of the item", default=0.0)
    unit_price: float = Field(description="Price per unit of the item", default=0.0)
    total_price: float = Field(description="Total price for this line item", default=0.0)

class InvoiceData(BaseModel):
    invoice_number: str = Field(description="The unique identifier or number of the invoice", default="")
    date: str = Field(description="The date the invoice was issued (YYYY-MM-DD or as written)", default="")
    vendor_name: str = Field(description="The name of the company or person issuing the invoice", default="")
    vendor_address: str = Field(description="The address of the vendor, if available", default="")
    customer_name: str = Field(description="The name of the customer being billed", default="")
    line_items: List[LineItem] = Field(description="List of items or services billed in the invoice", default_factory=list)
    subtotal: float = Field(description="Subtotal amount before taxes", default=0.0)
    tax_amount: float = Field(description="Total tax amount applied, if any", default=0.0)
    total_amount: float = Field(description="The final total amount of the invoice", default=0.0)
    is_valid: bool = Field(description="True if all required fields are present and totals seem mathematically consistent, False otherwise", default=False)

def process_invoice_text(text: str, api_key: str, model_name: str = "llama-3.3-70b-versatile") -> InvoiceData:
    """
    Uses Groq and LangChain to extract structured financial data from raw invoice text.
    """
    if not api_key:
        raise ValueError("Groq API Key is required.")
        
    os.environ["GROQ_API_KEY"] = api_key

    # Initialize the LLM
    llm = ChatGroq(model=model_name, temperature=0.0)
    
    # Configure the structured output
    structured_llm = llm.with_structured_output(InvoiceData)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligent data extraction assistant. Your task is to extract structured financial information from the provided invoice text. "
                   "If you cannot find a specific field, do your best to infer it from context or use a default empty/zero value. "
                   "Ensure that the mathematical relationship between the line items, subtotal, tax, and total amount is consistent. "
                   "If the document does not appear to be a valid invoice, try to extract what you can and set is_valid to false."),
        ("human", "Here is the raw text extracted from an invoice documents:\n\n{text}\n\nExtract the requested invoice data.")
    ])

    chain = prompt | structured_llm

    result = chain.invoke({"text": text})
    if isinstance(result, dict):
        return InvoiceData(**result)
    return result
