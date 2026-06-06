import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.db import Base

class InvoiceData(Base):
    __tablename__ = "invoice_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String)

    seller_name = Column(String)
    seller_address = Column(String)

    consignee_name = Column(String)
    consignee_address = Column(String)

    invoice_number = Column(String)
    invoice_date = Column(String)

    description = Column(String)
    vessel = Column(String)

    gst_number = Column(String)

    quantity = Column(String)
    rate = Column(String)
    amount = Column(String)

    gst_amount = Column(String)

    total_amount = Column(String)

    amount_in_words = Column(String)

    raw_text = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
