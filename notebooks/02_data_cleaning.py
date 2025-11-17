"""02_data_cleaning.py
Cleaning pipeline for Gamezone Orders:
- Normalize text fields
- Convert timestamps
- Flag ship-before-purchase
- Save cleaned snapshot to parquet
"""

import os
import pandas as pd

INPUT_PARQUET = "data/orders_raw.parquet"
OUTPUT_PARQUET = "data/orders_clean.parquet"

NULL_TOKENS = {
    "", "none", "n/a", "na", "null", "unknown", "undefined",
    "not available", "not applicable"
}

def normalize_text_series(s: pd.Series) -> pd.Series:
    s = s.astype("string")
    out = s.str.strip()
    out = out.str.replace(r"\s+", " ", regex=True)
    out = out.str.lower()
    out = out.where(~out.isin(NULL_TOKENS), pd.NA)
    return out

def main():
    if not os.path.exists(INPUT_PARQUET):
        raise FileNotFoundError(f"{INPUT_PARQUET} not found. Export raw data first.")

    df = pd.read_parquet(INPUT_PARQUET)

    # Normalize selected text columns
    text_cols = [
        "PURCHASE_PLATFORM",
        "MARKETING_CHANNEL",
        "ACCOUNT_CREATION_METHOD",
        "COUNTRY_CODE",
        "PRODUCT_NAME",
    ]
    for col in text_cols:
        if col in df.columns:
            before = df[col].copy()
            after = normalize_text_series(before)
            changes = (before.astype("string").fillna("<NA>") != after.astype("string").fillna("<NA>")).sum()
            df[col] = after
            print(f"{col}: {changes} values normalized")

    # Convert timestamps
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce", utc=True)
    df["SHIP_TS_dt"] = pd.to_datetime(df["SHIP_TS"], errors="coerce", utc=True)
    df["SHIP_TS_DATE"] = df["SHIP_TS_dt"].dt.date

    # Flag ship-before-purchase
    mask_ship_before = df["SHIP_TS_dt"] < df["PURCHASE_TS"]
    df["FLAG_SHIP_BEFORE_PURCHASE"] = mask_ship_before
    print("Ship-before-purchase rows:", int(mask_ship_before.sum()))

    os.makedirs("data", exist_ok=True)
    df.to_parquet(OUTPUT_PARQUET)
    print("Saved cleaned data to", OUTPUT_PARQUET)

if __name__ == "__main__":
    main()
