# 🧾 Invoice Extractor API

Welcome to the **Invoice Extractor API**! This is a production-ready, highly robust backend service designed to parse data from unpredictable invoice formats (both digital PDFs and scanned images).

Instead of relying on brittle and rigid Regex rules that break every time a vendor changes their invoice layout, this system uses **OCR** combined with **Large Language Models (LLM)** to *understand* the layout, neighborhood context, and labels dynamically.

## 🚀 Features

- **Format Agnostic**: Accepts both text-based PDFs and scanned document images (`.pdf`, `.png`, `.jpg`).
- **Dynamic Layout Understanding**: Uses **Groq** model to intuitively identify and pair fields (like `seller_name`, `consignee_address`, `gst_amount`, etc.) based on visual and textual context rather than hard-coded coordinates or regex.
- **Smart OCR Fallbacks**: Uses `pdfplumber` for native digital PDFs, and intelligently falls back to `PyMuPDF` and `EasyOCR` to convert and read scanned images on-the-fly.
- **Database Persistence**: Fully integrated with PostgreSQL via SQLAlchemy to instantly store structured records of every extracted invoice.
- **Clean REST API**: Fast and scalable endpoints built on FastAPI.

---

## 🛠️ Prerequisites

Before you start, make sure you have:
- **Python 3.10+**
- **PostgreSQL** running locally or via a cloud provider (e.g., Neon, AWS RDS).
- A **Groq API Key** (Get one for free at [groq.com](https://groq.com)).

---

## ⚙️ Setup & Installation

**1. Clone the repository and navigate to the project:**
```bash
git clone https://github.com/sanchitkhthpalia/PerceptiveLabs_R2.git
cd invoice-extractor
```

**2. Set up a Virtual Environment (Recommended):**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
pip install pymupdf  # Ensure our OCR fallback is installed
```

**4. Environment Configuration:**
Rename `.env.example` to `.env` (or create a new `.env` file in the root directory) and add your credentials:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/invoice_db
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: FastAPI will automatically create the `invoice_data` table for you when you run the app!)*

---

## 🏃‍♂️ Running the Server

Start the FastAPI server with live-reloading:
```bash
uvicorn app.main:app --reload
```

The API will now be running at `http://localhost:8000`.

---

## 🧪 How to Use & Test

### Method 1: The Interactive Swagger UI (Browser)
FastAPI automatically generates a beautiful testing interface for you.
1. Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
2. Click the `POST /extract-llm` route.
3. Click **"Try it out"**.
4. Upload an invoice document (`.pdf` or `.png`) and click **"Execute"**.
5. Scroll down to see your cleanly structured JSON output!

### Method 2: Batch Processing Script
Have a whole folder full of invoices to process? We have a script for that.
1. Place all your invoices in the `invoices/` directory.
2. Make sure your FastAPI server is running in a separate terminal.
3. Run the batch script:
```bash
pip install requests
python batch_process.py
```
This script will loop through every file, hit the API, print the status, and save the resulting JSON for each invoice into a new `extracted_data/` folder.

---

## 🏗️ Architecture Flow

1. **Upload:** Client sends a document to `POST /extract-llm`.
2. **Text Extraction:** `ocr_service.py` evaluates the file type. It safely pulls raw text preserving lines and spatial flow.
3. **LLM Parsing:** The raw text is shipped to Groq (`llm_service.py`), strictly prompted to return a structured JSON object for your requested fields.
4. **Database Saving:** The FastAPI route maps the JSON output to the `InvoiceData` SQLAlchemy model and saves it.
5. **Response:** API returns the structured data alongside the Postgres UUID. 
