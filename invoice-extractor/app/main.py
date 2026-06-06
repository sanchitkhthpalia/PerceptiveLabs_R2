from fastapi import FastAPI
from app.routes import extract_llm
from app.database.db import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invoice Extraction API")

app.include_router(extract_llm.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Invoice Extraction API"}
