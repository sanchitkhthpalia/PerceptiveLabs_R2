import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import InvoiceData
from app.services.ocr_service import extract_text_from_file
from app.services.llm_service import extract_invoice_data

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extract-llm")
async def extract_llm(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in ["pdf", "png", "jpeg", "jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    temp_file_name = f"{uuid.uuid4()}.{file_extension}"
    temp_file_path = os.path.join(UPLOAD_DIR, temp_file_name)

    try:
        # Step 2: Store temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 3: Extract text
        raw_text = extract_text_from_file(temp_file_path, file_extension)

        if not raw_text:
            raise HTTPException(status_code=400, detail="Could not extract text from document")

        # Step 4, 5, 6: Send to LLM and get structured JSON
        extracted_data = extract_invoice_data(raw_text)
        
        if "error" in extracted_data:
            raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {extracted_data['error']}")

        # Step 7: Store into PostgreSQL
        new_invoice = InvoiceData(
            file_name=file.filename,
            seller_name=extracted_data.get("seller_name"),
            seller_address=extracted_data.get("seller_address"),
            consignee_name=extracted_data.get("consignee_name"),
            consignee_address=extracted_data.get("consignee_address"),
            invoice_number=extracted_data.get("invoice_number"),
            invoice_date=extracted_data.get("invoice_date"),
            description=extracted_data.get("description"),
            vessel=extracted_data.get("vessel"),
            gst_number=extracted_data.get("gst_number"),
            quantity=str(extracted_data.get("quantity")) if extracted_data.get("quantity") is not None else None,
            rate=str(extracted_data.get("rate")) if extracted_data.get("rate") is not None else None,
            amount=str(extracted_data.get("amount")) if extracted_data.get("amount") is not None else None,
            gst_amount=str(extracted_data.get("gst_amount")) if extracted_data.get("gst_amount") is not None else None,
            total_amount=str(extracted_data.get("total_amount")) if extracted_data.get("total_amount") is not None else None,
            amount_in_words=extracted_data.get("amount_in_words"),
            raw_text=raw_text
        )
        
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

        # Step 8: Return response
        return {
            "status": "success",
            "invoice_id": str(new_invoice.id),
            "data": extracted_data
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
