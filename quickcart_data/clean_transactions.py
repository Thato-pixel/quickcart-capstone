import json
import pandas as pd
from pymongo import MongoClient
import re

# PASTE YOUR MONGODB ATLAS STRING HERE
MONGO_URI = "mongodb+srv://thatomatlali_db_user:DhT3CkFozsyoMd1m@quickcart.ndxjnxk.mongodb.net/?appName=quickcart"

def normalize_currency(val):
    """
    Standardizes: "$10.00", "10.00", and 1000 (cents) -> 10.00 (float)
    """
    if val is None or val == "":
        return None
    try:
        if isinstance(val, str):
            clean_str = re.sub(r'[^\d.]', '', val) # Remove symbols like $
            return float(clean_str)
        if isinstance(val, int):
            return val / 100.0 # Convert cents to dollars
        return float(val)
    except (ValueError, TypeError):
        return None

def process_data():
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client.quickcart_archive
    collection = db.raw_logs

    input_file = 'quickcart_data/raw_data.jsonl'
    clean_records = []
    raw_logs_for_mongodb = []

    print("Reading raw transaction logs...")
    with open(input_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            raw_logs_for_mongodb.append(record) # Prepare for archive

            # Extraction and Filtering
            # Navigate nested JSON structure
            txn = record.get('transaction', {})
            
            # 1. Filter out test/sandbox transactions
            if record.get('is_test') == 1 or record.get('environment') == 'sandbox':
                continue
            
            # 2. Normalize Currency
            amount_usd = normalize_currency(txn.get('amount'))
            order_id = txn.get('order_id')

            # 3. Drop records without valid amounts or identifiers
            if amount_usd is not None and order_id:
                clean_records.append({
                    'order_id': order_id,
                    'payment_id': txn.get('payment_id'),
                    'amount_usd': amount_usd,
                    'timestamp': record.get('timestamp')
                })

    # Deliverable: Archive to MongoDB
    if raw_logs_for_mongodb:
        collection.insert_many(raw_logs_for_mongodb)
        print(f"Archived {len(raw_logs_for_mongodb)} logs to MongoDB Atlas.")

    # Deliverable: Output clean CSV
    df = pd.DataFrame(clean_records)
    df.to_csv('clean_transactions.csv', index=False)
    print(f"Successfully created clean_transactions.csv with {len(df)} records.")

if __name__ == "__main__":
    process_data()