"""04_churn_indicators.py
Churn analysis using simple RFM-style features:
- Recency (days since last purchase)
- Frequency (number of orders)
- Monetary (total spend)
- Churn flag based on inactivity threshold
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/orders_clean.parquet"
CHURN_THRESHOLD_DAYS = 90

def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run 02_data_cleaning.py first.")

    df = pd.read_parquet(DATA_PATH)
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce", utc=True)

    snapshot_date = df["PURCHASE_TS"].max()
    print("Snapshot date:", snapshot_date)

    rfm = (
        df.groupby("USER_ID").agg(
            last_purchase=("PURCHASE_TS", "max"),
            frequency=("ORDER_ID", "nunique"),
            monetary_value=("USD_PRICE", "sum"),
        )
    ).reset_index()

    rfm["recency_days"] = (snapshot_date - rfm["last_purchase"]).dt.days
    rfm["churned"] = (rfm["recency_days"] > CHURN_THRESHOLD_DAYS).astype(int)

    print("Sample RFM rows:")
    print(rfm.head())

    plt.figure(figsize=(8, 5))
    rfm["recency_days"].plot.hist(bins=50)
    plt.axvline(CHURN_THRESHOLD_DAYS, color="red", linestyle="--", label="Churn threshold")
    plt.title("Recency Distribution")
    plt.xlabel("Days Since Last Purchase")
    plt.ylabel("Number of Customers")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
