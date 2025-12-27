#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path
import json


# =========================================================
# CONFIGURATION
# =========================================================
SHEET_NAME = "Year 2010-2011"          # <-- USE YOUR SHEET HERE
CHURN_THRESHOLD = 90                   # days

# Base project directory (works in Docker & local)
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

EXCEL_PATH = RAW_DIR / "online_retail_II.xlsx"
QUALITY_JSON = RAW_DIR / "data_quality_summary.json"
FINAL_FEATURES = PROCESSED_DIR / "customer_features_final.csv"


# =========================================================
# STEP 1 — LOAD RAW DATA
# =========================================================
def load_data():
    print(f"\nLoading Excel from: {EXCEL_PATH}")
    print("Exists:", EXCEL_PATH.exists())

    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    df["financial_year"] = SHEET_NAME
    return df


# =========================================================
# STEP 2 — DATA QUALITY REPORT
# =========================================================
def save_data_quality(df):
    report = {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "date_range": {
            "min": str(df["InvoiceDate"].min()),
            "max": str(df["InvoiceDate"].max())
        }
    }

    with open(QUALITY_JSON, "w") as f:
        json.dump(report, f, indent=4)

    print("\nData quality report saved.")


# =========================================================
# STEP 3 — CLEAN DATA
# =========================================================
def clean_data(df):

    rows_before = df.shape[0]

    # Remove missing customer IDs
    df = df.dropna(subset=["Customer ID"])

    # Remove cancellations
    df = df[~df["Invoice"].astype(str).str.startswith("C")]

    # Remove duplicates
    df = df.drop_duplicates()

    # Ensure datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    print(f"\nRows before cleaning: {rows_before}")
    print(f"Rows after cleaning: {df.shape[0]}")

    return df


# =========================================================
# STEP 4 — BUILD RFM
# =========================================================
def build_rfm(df):

    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (reference_date - x.max()).days,
        "Invoice": "nunique",
        "Price": "sum"
    }).reset_index()

    rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]

    rfm["Churn"] = (rfm["Recency"] > CHURN_THRESHOLD).astype(int)

    return rfm


# =========================================================
# STEP 5 — PURCHASE FEATURES
# =========================================================
def build_purchase_features(df):

    features = df.groupby("Customer ID").agg(
        avg_quantity_per_order=("Quantity", "mean"),
        max_quantity=("Quantity", "max"),
        min_quantity=("Quantity", "min"),
        std_quantity=("Quantity", "std"),
        total_items_purchased=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
        unique_invoices=("Invoice", "nunique")
    ).reset_index()

    features["std_quantity"] = features["std_quantity"].fillna(0)

    return features


# =========================================================
# STEP 6 — MONETARY FEATURES
# =========================================================
def build_monetary_features(df):

    monetary = df.groupby("Customer ID").agg(
        total_revenue=("Price", "sum"),
        avg_order_value=("Price", "mean"),
        max_order_value=("Price", "max"),
        min_order_value=("Price", "min"),
        std_order_value=("Price", "std"),
        total_items=("Quantity", "sum")
    ).reset_index()

    monetary["revenue_per_item"] = (
        monetary["total_revenue"] / monetary["total_items"]
    )

    monetary["std_order_value"] = monetary["std_order_value"].fillna(0)

    return monetary.drop(columns=["total_items"])


# =========================================================
# STEP 7 — TEMPORAL FEATURES
# =========================================================
def build_temporal_features(df):

    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    temp = df.groupby("Customer ID").agg(
        first_purchase_date=("InvoiceDate", "min"),
        last_purchase_date=("InvoiceDate", "max"),
        active_days=("InvoiceDate", "nunique"),
        active_months=("InvoiceDate", lambda x: x.dt.to_period("M").nunique()),
        total_orders=("Invoice", "nunique")
    ).reset_index()

    temp["customer_tenure_days"] = (
        temp["last_purchase_date"] - temp["first_purchase_date"]
    ).dt.days

    temp["days_since_first_purchase"] = (
        reference_date - temp["first_purchase_date"]
    ).dt.days

    temp["purchase_span_days"] = (
        temp["last_purchase_date"] - temp["first_purchase_date"]
    ).dt.days

    temp["avg_days_between_orders"] = (
        temp["purchase_span_days"] /
        (temp["total_orders"] - 1)
    ).fillna(0)

    return temp.drop(columns=["first_purchase_date", "last_purchase_date", "total_orders"])


# =========================================================
# STEP 8 — FINAL PIPELINE
# =========================================================
def run_pipeline():

    df = load_data()

    save_data_quality(df)

    df = clean_data(df)

    rfm = build_rfm(df)

    purchase = build_purchase_features(df)
    monetary = build_monetary_features(df)
    temporal = build_temporal_features(df)

    final = (
        rfm
        .merge(purchase, on="Customer ID", how="left")
        .merge(monetary, on="Customer ID", how="left")
        .merge(temporal, on="Customer ID", how="left")
    )

    final["order_consistency"] = (
        final["Frequency"] / final["customer_tenure_days"].replace(0, 1)
    )

    final["spend_consistency"] = (
        final["avg_order_value"] / (final["std_order_value"] + 1)
    )

    final.to_csv(FINAL_FEATURES, index=False)

    print("\nSaved features to:", FINAL_FEATURES)
    print("\nDataset shape:", final.shape)


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    run_pipeline()
