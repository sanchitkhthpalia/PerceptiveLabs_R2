import os
import pdfplumber
from pdf2image import convert_from_path
import easyocr

# Initialize EasyOCR reader (this might take a while on first run)
reader = easyocr.Reader(['en'])

def extract_text_from_file(file_path: str, file_extension: str) -> str:
    extracted_text = ""
    
    if file_extension == "pdf":
        # Try pdfplumber first
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        
        # If pdfplumber didn't find much text, it might be a scanned PDF
        if len(extracted_text.strip()) < 50:
            extracted_text = ""
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                for page in doc:
                    import tempfile
                    pix = page.get_pixmap(dpi=200)  # 200 dpi is good for OCR
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                        pix.save(temp_img.name)
                        result = reader.readtext(temp_img.name, detail=0)
                        extracted_text += " ".join(result) + "\n"
                    os.remove(temp_img.name)
            except Exception as e:
                print(f"Fallback OCR with PyMuPDF failed: {e}")

    elif file_extension in ["png", "jpeg", "jpg"]:
        result = reader.readtext(file_path, detail=0)
        extracted_text = " ".join(result)
        
    return extracted_text.strip()
