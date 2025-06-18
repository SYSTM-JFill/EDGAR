import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Path to /utils/
DATA_DIR = os.path.join(BASE_DIR, "..", "data")        # Adjusts to /data from project root

def save_tables(df, report_date, table_name):
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        safe_table_name = table_name.replace(" ", "_").replace("/", "_")
        # Sanitize report_date if needed (replace slashes etc)
        safe_report_date = str(report_date).replace("/", "-")

        filename = f"{safe_table_name}_{safe_report_date}.csv"
        filepath = os.path.join(DATA_DIR, filename)

        df.to_csv(filepath, index=False)
        print(f"[INFO] Saved CSV to {filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")
