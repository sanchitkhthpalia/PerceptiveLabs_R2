import os
import pdfplumber
from pdf2image import convert_from_path
import easyocr

# Initialize EasyOCR reader (this might take a while on first run)
reader = easyocr.Reader(['en'])

def extract_text_from_file(file_path: str, mime_type: str) -> str:
    extracted_text = ""
    
    if mime_type == "application/pdf":
        # Try pdfplumber first
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        
        # If pdfplumber didn't find much text, it might be a scanned PDF
        if len(extracted_text.strip()) < 50:
            extracted_text = ""
            images = convert_from_path(file_path)
            for img in images:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                    img.save(temp_img.name, "PNG")
                    result = reader.readtext(temp_img.name, detail=0)
                    extracted_text += " ".join(result) + "\n"
                os.remove(temp_img.name)

    elif mime_type in ["image/png", "image/jpeg", "image/jpg"]:
        result = reader.readtext(file_path, detail=0)
        extracted_text = " ".join(result)
        
    return extracted_text.strip()
