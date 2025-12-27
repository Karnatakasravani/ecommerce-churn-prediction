"""
Prediction Module

This module exposes production-ready API-style functions for churn prediction.

Required Functions
------------------
1. load_model()      -> loads trained ML model
2. load_scaler()     -> loads scaler (if used) – optional
3. preprocess_input() -> validates & prepares input data
4. predict()         -> returns churn label (0/1)
5. predict_proba()   -> returns churn probability

Supports:
- single record
- batch (CSV / dataframe)

Handles:
- missing columns
- wrong types
- invalid input

Author: Sravani Karnataka
"""

import joblib
import pandas as pd
import numpy as np
import json
import os


# -----------------------------
# Model + Scaler Loaders
# -----------------------------

def load_model():
    """Loads trained churn model"""
    path = os.path.join("models", "random_forest_model.pkl")
    model = joblib.load(path)
    return model


def load_scaler():
    """
    Loads scaler if used during training
    If not used, return None
    """
    scaler_path = os.path.join("models", "scaler.pkl")

    if os.path.exists(scaler_path):
        return joblib.load(scaler_path)
    return None


# -----------------------------
# Input Preprocessing
# -----------------------------

REQUIRED_FEATURES = [
    "Recency",
    "Frequency",
    "Monetary",
    "avg_days_between_orders",
    "total_items_purchased",
    "unique_products"
]


def preprocess_input(data):
    """
    Accepts:
    - dict (single record)
    - list of dicts
    - pandas DataFrame

    Returns:
    - cleaned pandas DataFrame
    """

    # Convert dict → DataFrame
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    # Convert list → DataFrame
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # Ensure DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be dict, list or pandas DataFrame")

    # Check required cols
    missing = [c for c in REQUIRED_FEATURES if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    # Convert to numeric safely
    data = data[REQUIRED_FEATURES].apply(pd.to_numeric, errors="coerce")

    # Handle NaN
    if data.isnull().sum().sum() > 0:
        raise ValueError("Invalid / non-numeric values in input")

    return data


# -----------------------------
# Prediction Functions
# -----------------------------

def predict(data):
    """
    Returns churn label (0/1)
    """
    model = load_model()
    scaler = load_scaler()

    X = preprocess_input(data)

    if scaler is not None:
        X = scaler.transform(X)

    preds = model.predict(X)

    # Return int for single record
    if len(preds) == 1:
        return int(preds[0])

    return preds.tolist()


def predict_proba(data):
    """
    Returns churn probability (0–1)
    """
    model = load_model()
    scaler = load_scaler()

    X = preprocess_input(data)

    if scaler is not None:
        X = scaler.transform(X)

    probs = model.predict_proba(X)[:, 1]

    if len(probs) == 1:
        return float(probs[0])

    return probs.tolist()
