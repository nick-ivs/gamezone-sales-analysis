"""01_data_exploration.py
Initial data exploration for Gamezone orders dataset.
- Connects to BigQuery
- Loads Orders table
- Basic info(), head(), descriptive stats
"""

import os
import pandas as pd
from google.cloud import bigquery

# TODO: update this path to your JSON key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\path\to\service-account.json"

PROJECT_ID = "wise-bongo-476621-k6"  # change if needed
DATASET_ID = "Gamezone"
TABLE_ID = "Orders"

def load_orders(limit=None):
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        {f"LIMIT {limit}" if limit else ""}
    """
    df = client.query(query).to_dataframe()
    return df

if __name__ == "__main__":
    df = load_orders()
    print("Shape:", df.shape)
    print("\nDtypes:")
    print(df.dtypes)
    print("\nHead:")
    print(df.head())
