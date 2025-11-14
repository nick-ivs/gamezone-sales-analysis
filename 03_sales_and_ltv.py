"""03_sales_and_ltv.py
Sales trend and LTV analysis:
- Sales over time
- Basic LTV per user
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/orders_clean.parquet"

def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run 02_data_cleaning.py first.")

    df = pd.read_parquet(DATA_PATH)
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce", utc=True)
    df["USD_PRICE"] = pd.to_numeric(df["USD_PRICE"], errors="coerce")

    # Daily sales
    df["purchase_date"] = df["PURCHASE_TS"].dt.date
    daily = (
        df.groupby("purchase_date")["USD_PRICE"]
        .sum()
        .reset_index(name="total_sales_usd")
        .sort_values("purchase_date")
    )

    plt.figure(figsize=(12, 5))
    plt.plot(daily["purchase_date"], daily["total_sales_usd"])
    plt.title("Daily Sales Trend (USD)")
    plt.xlabel("Date")
    plt.ylabel("Total Sales (USD)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

    # LTV per user
    ltv = (
        df.groupby("USER_ID")["USD_PRICE"]
        .sum()
        .reset_index(name="LTV_USD")
        .sort_values("LTV_USD", ascending=False)
    )
    print("Top 10 customers by LTV:")
    print(ltv.head(10))

if __name__ == "__main__":
    main()
