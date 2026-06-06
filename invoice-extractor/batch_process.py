import os
import requests
import json

# Configuration
API_URL = "http://localhost:8000/extract-llm"
INVOICES_DIR = "invoices"
OUTPUT_DIR = "extracted_data"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_invoices():
    if not os.path.exists(INVOICES_DIR):
        print(f"Directory '{INVOICES_DIR}' not found.")
        return

    # Get all files excluding .gitkeep
    files = [f for f in os.listdir(INVOICES_DIR) if os.path.isfile(os.path.join(INVOICES_DIR, f)) and f != ".gitkeep"]

    if not files:
        print(f"No files found in '{INVOICES_DIR}'.")
        return

    print(f"Found {len(files)} invoices. Starting processing...\n" + "="*50)

    for file_name in files:
        file_path = os.path.join(INVOICES_DIR, file_name)
        print(f"Processing: {file_name}...")

        try:
            # Send file via multipart/form-data
            with open(file_path, "rb") as f:
                files_payload = {"file": (file_name, f)}
                response = requests.post(API_URL, files=files_payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Invoice ID: {result.get('invoice_id')}")
                
                # Save structured output
                base_name = os.path.splitext(file_name)[0]
                output_file = os.path.join(OUTPUT_DIR, f"{base_name}.json")
                
                with open(output_file, "w", encoding="utf-8") as out_f:
                    json.dump(result, out_f, indent=4)
                    
                print(f"💾 Saved structured data to: {output_file}\n")
            else:
                print(f"❌ Failed. API returned Status Code: {response.status_code}")
                print(f"Response: {response.text}\n")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Error: Could not connect to {API_URL}. Is the FastAPI server running?\n")
            break
        except Exception as e:
            print(f"❌ Error processing {file_name}: {str(e)}\n")

if __name__ == "__main__":
    process_invoices()
