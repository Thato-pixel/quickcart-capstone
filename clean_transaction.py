import json
import csv
import re
import os
import urllib.parse
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv  # You may need to run 'pip install python-dotenv'

# 1. Load Secrets from .env file
load_dotenv()

# Get credentials from environment variables instead of hardcoding
db_user = os.getenv("MONGO_USER", "thatomatlali_db_user")
db_pass = os.getenv("MONGO_PASSWORD") # This stays hidden!

if not db_pass:
    print("⚠️ Warning: MONGO_PASSWORD not found in environment variables.")

# 2. MongoDB Setup with Encoded Password
encoded_password = urllib.parse.quote_plus(db_pass) if db_pass else ""
MONGO_URI = f"mongodb+srv://{db_user}:{encoded_password}@quickcart.ndxjnxk.mongodb.net/?appName=quickcart"

# Rest of your script follows...

# Use a timeout so it doesn't hang your terminal
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["quickcart_audit"]
logs_col = db["raw_logs"]

def normalize_amount(val):
    if val is None or val == "": return 0.0
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return float(val) / 100.0 if isinstance(val, int) else float(val)
    str_val = re.sub(r'[^\d.]', '', str(val))
    return float(str_val) if str_val else 0.0

def process_data():
    # Setup pathing to find the data in the subfolder
    script_dir = Path(__file__).parent.absolute()
    input_file = script_dir / "quickcart_data" / "raw_data.jsonl"
    output_file = script_dir / "clean_transactions.csv"

    print(f"🔍 Reading from: {input_file}")
    
    if not input_file.exists():
        print(f"❌ Error: Could not find {input_file}")
        return

    processed_count = 0
    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=["transaction_id", "amount_usd", "status"])
        writer.writeheader()

        for line in f_in:
            if not line.strip(): continue
            try:
                record = json.loads(line)
            except: continue
            
            # --- TARGET THE NESTED STRUCTURE ---
            # Extracting from record["data"]["object"]
            event_obj = record.get("event", {})
            data_obj = record.get("data", {}).get("object", {})
            
            txn_id = data_obj.get("id") or event_obj.get("id") or record.get("id")
            raw_amt = data_obj.get("amount") or record.get("amount")
            
            # Filter out test data
            if not txn_id or record.get("is_test") == True:
                continue

            writer.writerow({
                "transaction_id": txn_id,
                "amount_usd": normalize_amount(raw_amt),
                "status": data_obj.get("status") or "SUCCESS"
            })
            processed_count += 1
            
            # Batch archive to Mongo (optional - fails silently if no internet)
            if processed_count % 100 == 0:
                try: logs_col.insert_one(record)
                except: pass

    print(f"✅ SUCCESS! Created CSV with {processed_count} records.")

if __name__ == "__main__":
    process_data()