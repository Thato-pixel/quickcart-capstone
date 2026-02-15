QuickCart Data Integrity & Reconciliation Capstone
📌 Project Overview
This project addresses a critical data discrepancy between QuickCart's internal transaction logs and bank settlement records. I developed a Python-based ETL pipeline to clean raw transaction data, archive it to a cloud database, and perform a financial reconciliation using SQL.

🛠️ Tech Stack
Language: Python 3.x

Database: MongoDB Atlas (Cloud NoSQL)

Data Format: JSONL (Raw) and CSV (Cleaned)

Analysis: SQL (Window Functions & CTEs)

Version Control: Git & GitHub

🚀 Features & Solutions
1. Data Cleaning Pipeline (clean_transactions.py)
The Problem: Raw logs used a deeply nested "Stripe-style" structure, causing traditional parsers to fail.

The Solution: Implemented a robust extraction logic that navigates data -> object nesting to retrieve Payment IDs and amounts.

Normalisation: Standardized currency from cents (integer) to USD (float).

Result: Successfully processed 74,472 records into a finalized clean_transactions.csv.

2. Cloud Archival
Automated the archival of raw event logs to MongoDB Atlas for long-term auditability.

Implemented URL-encoding for secure database authentication.

3. Financial Reconciliation (reconciliation.sql)
Deduplication: Used SQL Window Functions (ROW_NUMBER()) to handle duplicate success events and identify the most recent valid transaction per order.

Gap Analysis: Calculated the discrepancy_gap_usd to identify missing funds between internal sales and bank settlements.

📂 File Structure
quickcart_data/clean_transactions.py: Main ETL script.

quickcart_data/reconciliation.sql: SQL audit query.

quickcart_data/raw_data.jsonl: Original raw transaction logs.

clean_transactions.csv: Final cleaned dataset.

requirements.txt: Python dependencies.

🔧 Setup Instructions
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Add your MongoDB Atlas credentials to clean_transactions.py.

Run the pipeline: python quickcart_data/clean_transactions.py.