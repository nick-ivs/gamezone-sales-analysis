# Gamezone Sales & Customer Behavior Analysis

This project is an end-to-end analytics case study built with **Python** and **BigQuery**.

It explores:

- Sales trends and the early-2021 drop
- Customer behavior and **Lifetime Value (LTV)**
- **Churn indicators** based on recency and frequency
- Product performance and co-purchase patterns
- Impact of **marketing channels** and **platforms** on revenue

## 📦 Dataset

Schema (BigQuery table `Gamezone.Orders`):

- `USER_ID` – unique customer identifier
- `ORDER_ID` – unique order identifier
- `PURCHASE_TS` – timestamp of purchase
- `SHIP_TS` – shipping date
- `PRODUCT_NAME` – name of purchased product
- `PRODUCT_ID` – product identifier
- `USD_PRICE` – purchase value in USD
- `PURCHASE_PLATFORM` – platform used (e.g. web, mobile app)
- `MARKETING_CHANNEL` – marketing/acquisition channel
- `ACCOUNT_CREATION_METHOD` – how the account was created
- `COUNTRY_CODE` – customer country (ISO-like code)

> Note: The live dataset sits in BigQuery. This repo focuses on **analysis code** and can use a small sample in `data/` if needed.

## 🛠 Tech Stack

- Python
- pandas
- matplotlib
- google-cloud-bigquery
- db-dtypes
- Jupyter Notebook

## 📚 Notebooks / Scripts

Suggested structure:

- `notebooks/01_data_exploration.py`  
  - Connect to BigQuery, load table, basic EDA  
- `notebooks/02_data_cleaning.py`  
  - Type conversions, text normalization, flagging issues  
- `notebooks/03_sales_and_ltv.py`  
  - Sales trends, LTV calculation, LTV segmentation  
- `notebooks/04_churn_indicators.py`  
  - Recency, frequency, churn threshold and segmentation  
- `notebooks/05_product_insights.py`  
  - Product performance, volatility, co-purchase analysis  

You can convert these scripts to `.ipynb` notebooks or use them directly in Jupyter.

## 🔍 Key Analytics Topics Covered

- Data cleaning:
  - Normalize text fields
  - Parse timestamps and compute shipping delays
  - Flag "ship before purchase" anomalies
- Sales analytics:
  - Daily and monthly revenue trends
  - Channel and platform breakdowns
- Customer analytics:
  - LTV per user
  - RFM-style features (recency, frequency, monetary)
  - Churn indicators based on inactivity windows
- Product analytics:
  - Top and bottom performers
  - Volatility and seasonality
  - Basic co-purchase analysis using composite orders (user + day)

## ▶️ How to Use

1. Install dependencies:

   - See `requirements.txt`

2. Set up BigQuery credentials:

   - Use a service account JSON key and set `GOOGLE_APPLICATION_CREDENTIALS`
   - Point to your GCP project and dataset in the code

3. Run the notebooks / scripts in `notebooks/` in order.

## 📅 Last Updated

- 2025-11-14
