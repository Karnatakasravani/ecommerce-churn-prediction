#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path


# =========================================================
# CONFIG
# =========================================================
CHURN_THRESHOLD = 90   # days

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INPUT_DATA = PROCESSED_DIR / "clean_data_final.csv"
OUTPUT_DATA = PROCESSED_DIR / "customer_features_final.csv"


# =========================================================
# FEATURE ENGINEERING
# =========================================================
def build_features():

    print(f"\nLoading cleaned data from: {INPUT_DATA}")
    df = pd.read_csv(INPUT_DATA)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # -------- RFM --------
    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (reference_date - x.max()).days,
        "Invoice": "nunique",
        "Price": "sum"
    }).reset_index()

    rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]

    # -------- Churn --------
    rfm["Churn"] = (rfm["Recency"] > CHURN_THRESHOLD).astype(int)

    # -------- Purchase features --------
    purchase = df.groupby("Customer ID").agg(
        avg_quantity_per_order=("Quantity", "mean"),
        max_quantity=("Quantity", "max"),
        min_quantity=("Quantity", "min"),
        std_quantity=("Quantity", "std"),
        total_items_purchased=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
        unique_invoices=("Invoice", "nunique")
    ).reset_index()

    purchase["std_quantity"] = purchase["std_quantity"].fillna(0)

    # -------- Monetary features --------
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

    monetary = monetary.drop(columns=["total_items"])

    # -------- Temporal features --------
    temporal = df.groupby("Customer ID").agg(
        first_purchase_date=("InvoiceDate", "min"),
        last_purchase_date=("InvoiceDate", "max"),
        active_days=("InvoiceDate", "nunique"),
        active_months=("InvoiceDate", lambda x: x.dt.to_period("M").nunique()),
        total_orders=("Invoice", "nunique")
    ).reset_index()

    temporal["customer_tenure_days"] = (
        temporal["last_purchase_date"] - temporal["first_purchase_date"]
    ).dt.days

    temporal["days_since_first_purchase"] = (
        reference_date - temporal["first_purchase_date"]
    ).dt.days

    temporal["purchase_span_days"] = (
        temporal["last_purchase_date"] - temporal["first_purchase_date"]
    ).dt.days

    temporal["avg_days_between_orders"] = (
        temporal["purchase_span_days"] /
        (temporal["total_orders"] - 1)
    ).fillna(0)

    temporal = temporal.drop(columns=[
        "first_purchase_date",
        "last_purchase_date",
        "total_orders"
    ])

    # -------- Merge all features --------
    final = (
        rfm
        .merge(purchase, on="Customer ID", how="left")
        .merge(monetary, on="Customer ID", how="left")
        .merge(temporal, on="Customer ID", how="left")
    )

    # -------- Extra engineered features --------
    final["order_consistency"] = (
        final["Frequency"] / final["customer_tenure_days"].replace(0, 1)
    )

    final["spend_consistency"] = (
        final["avg_order_value"] / (final["std_order_value"] + 1)
    )

    # -------- Save --------
    final.to_csv(OUTPUT_DATA, index=False)

    print("\nFeature engineering complete.")
    print(f"Saved → {OUTPUT_DATA}")
    print("Shape:", final.shape)


if __name__ == "__main__":
    build_features()
