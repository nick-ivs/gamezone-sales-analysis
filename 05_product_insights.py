"""05_product_insights.py
Product insights:
- Top products by revenue
- Monthly trend for top products
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/orders_clean.parquet"

def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run 02_data_cleaning.py first.")

    df = pd.read_parquet(DATA_PATH)
    df["USD_PRICE"] = pd.to_numeric(df["USD_PRICE"], errors="coerce")
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce", utc=True)
    df["month"] = df["PURCHASE_TS"].dt.to_period("M").dt.to_timestamp()

    product_sales = (
        df.groupby("PRODUCT_NAME")["USD_PRICE"]
        .sum()
        .reset_index(name="total_sales_usd")
        .sort_values("total_sales_usd", ascending=False)
    )

    print("Top 10 products by revenue:")
    print(product_sales.head(10))

    top_products = product_sales.head(5)["PRODUCT_NAME"].tolist()
    trends = (
        df[df["PRODUCT_NAME"].isin(top_products)]
        .groupby(["month", "PRODUCT_NAME"])["USD_PRICE"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))
    for name, group in trends.groupby("PRODUCT_NAME"):
        plt.plot(group["month"], group["USD_PRICE"], marker="o", label=name)
    plt.title("Monthly Sales Trend for Top Products")
    plt.xlabel("Month")
    plt.ylabel("Sales (USD)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
