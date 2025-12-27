#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path
import json


# =========================================================
# CONFIG
# =========================================================
SHEET_NAME = "Year 2010-2011"   # <-- use same as acquisition

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

EXCEL_PATH = RAW_DIR / "online_retail_II.xlsx"
OUTPUT_PATH = PROCESSED_DIR / "clean_data_final.csv"
REPORT_PATH = PROCESSED_DIR / "cleaning_report.json"


# =========================================================
# MAIN CLEANING FUNCTION
# =========================================================
def clean_data():

    print(f"\nReading Excel from: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    rows_before = len(df)

    # ----------------------------------------------
    # 1. Remove customers with missing IDs
    # ----------------------------------------------
    df = df.dropna(subset=["Customer ID"])
    after_customer = len(df)

    # ----------------------------------------------
    # 2. Remove cancelled invoices (start with C)
    # ----------------------------------------------
    df = df[~df["Invoice"].astype(str).str.startswith("C")]
    after_cancel = len(df)

    # ----------------------------------------------
    # 3. Remove duplicates
    # ----------------------------------------------
    df = df.drop_duplicates()
    after_duplicates = len(df)

    # ----------------------------------------------
    # 4. Optional: Keep only positive quantities
    # ----------------------------------------------
    df = df[df["Quantity"] > 0]
    after_quantity = len(df)

    # ----------------------------------------------
    # Calculate retention
    # ----------------------------------------------
    retention = round((after_quantity / rows_before) * 100, 2)

    print("\n===== CLEANING SUMMARY =====")
    print(f"Rows before cleaning     : {rows_before}")
    print(f"After removing null IDs  : {after_customer}")
    print(f"After cancellations      : {after_cancel}")
    print(f"After duplicates         : {after_duplicates}")
    print(f"After invalid quantity   : {after_quantity}")
    print(f"Final retention %        : {retention}%")

    # ----------------------------------------------
    # Save cleaned dataset
    # ----------------------------------------------
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved cleaned dataset → {OUTPUT_PATH}")

    # ----------------------------------------------
    # Save report
    # ----------------------------------------------
    report = {
        "rows_before": rows_before,
        "after_customer_filter": after_customer,
        "after_cancellation_filter": after_cancel,
        "after_duplicates_filter": after_duplicates,
        "after_quantity_filter": after_quantity,
        "retention_percent": retention
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Cleaning report saved → {REPORT_PATH}")


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    clean_data()
