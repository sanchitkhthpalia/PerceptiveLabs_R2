import os
import json
from groq import Groq

def extract_invoice_data(text: str) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY is not set"}

    client = Groq(api_key=api_key)
    
    prompt = """You are an invoice data extraction system.

Extract the following fields from the invoice:

seller_name
seller_address
consignee_name
consignee_address
invoice_number
invoice_date
description
vessel
gst_number
quantity
rate
amount
gst_amount
total_amount
amount_in_words

Return ONLY valid JSON.

Do not return explanations.
Do not return markdown.
If a field is not present return null.

Invoice Text:

{{OCR_TEXT}}"""

    prompt = prompt.replace("{{OCR_TEXT}}", text)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response"}
