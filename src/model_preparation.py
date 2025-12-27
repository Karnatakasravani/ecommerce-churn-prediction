#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import joblib
import json


# =========================================================
# PATHS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = PROCESSED_DIR / "customer_features_final.csv"
REPORT_PATH = MODEL_DIR / "model_report.json"


# =========================================================
# TRAINING PIPELINE
# =========================================================
def train_models():

    print(f"\nLoading training data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # -------- Separate features & target --------
    X = df.drop(columns=["Customer ID", "Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------- Scale features --------
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # -------- Logistic Regression --------
    log_model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    log_model.fit(X_train_scaled, y_train)

    log_test_auc = roc_auc_score(
        y_test,
        log_model.predict_proba(X_test_scaled)[:, 1]
    )

    # -------- Random Forest --------
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=10,
        random_state=42,
        class_weight="balanced"
    )

    rf_model.fit(X_train, y_train)

    rf_test_auc = roc_auc_score(
        y_test,
        rf_model.predict_proba(X_test)[:, 1]
    )

    # -------- Save models --------
    joblib.dump(log_model, MODEL_DIR / "logistic_model.pkl")
    joblib.dump(rf_model, MODEL_DIR / "random_forest_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

    # -------- Save metrics --------
    report = {
        "logistic_regression_auc": float(round(log_test_auc, 4)),
        "random_forest_auc": float(round(rf_test_auc, 4)),
        "num_features": X.shape[1],
        "samples": len(df)
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print("\n===== Model Training Complete =====")
    print(report)
    print(f"\nModels saved in: {MODEL_DIR}")


if __name__ == "__main__":
    train_models()
