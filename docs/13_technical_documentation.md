# Technical Documentation
## E-Commerce Customer Churn Prediction System

### Author
**Sravani Karnataka**

---

## 1. System Architecture

```mermaid
flowchart LR
A[Raw Transaction Data] --> B[Data Acquisition]
B --> C[Data Cleaning]
C --> D[Feature Engineering]
D --> E[Model Training]
E --> F[Model Selection & Evaluation]
F --> G[Model Export (.pkl)]
G --> H[Streamlit Web Application]
H --> I[End User Predictions]

2. Data Pipeline

This project simulates a real-world churn modeling pipeline using the UCI Online Retail II dataset.

Scripts & Responsibilities
Script	Purpose
01_data_acquisition.py	Loads and explores raw data
02_data_cleaning.py	Handles nulls, cancellations, outliers
03_feature_engineering.py	Builds RFM & behavioral features
04_model_preparation.py	Trains & evaluates ML models

** But here I have done all the .py files in one file called as data_aquisition**

Key Cleaning Steps

Removed rows with missing CustomerID

Removed cancelled invoices (InvoiceNo begins with C)

Removed negative/invalid quantities

Parsed invoice dates

Aggregated customer-level data

Achieved Retention ≈ 72%

3. Model Architecture

The model predicts whether a customer will churn based on historical purchasing patterns.

Algorithm

Random Forest Classifier

Reason for selection

✔ Handles non-linear relationships
✔ Robust to noise & missing data
✔ Performs well without heavy tuning

Input Features

Examples:
- Recency
- Frequency
- Monetary
- Total items purchased
- Unique products
- Avg days between orders
- Customer tenure
- Purchase span days

Output
Value	Meaning
0	Not churn
1	Churn

4. API Reference

The module app/predict.py provides reusable prediction functions.

predict(data)

Returns churn label (0/1)

predict_proba(data)

Returns probability of churn (0–1)

Input formats allowed
- Dict
- List of dicts
- Pandas DataFrame

5. Deployment Architecture

The solution supports two deployment modes

1️⃣ Cloud App Deployment
Streamlit Cloud
Public URL
No server cost
2️⃣ Container Deployment
Docker
Port mapping 8501
Reproducible environment

6. Troubleshooting Guide
Issue	Cause	Solution
App not loading	Port busy	Stop old container
Missing model file	Path wrong	Check /models/ folder
CSV upload error	Wrong columns	Use template CSV
Docker build timeout	Slow network	Retry / use VPN

7. Performance Summary:

Metric: ROC-AUC > 0.65
Model: Random Forest
Evaluation Strategy: Train-test split
The model achieves strong performance for business use.

8. Business Impact:
This application supports:

✔ retention strategy
✔ marketing targeting
✔ early churn detection
Businesses can reduce churn & improve lifetime value.

9. Security & Privacy:
Dataset anonymized
No personal identifiers stored
Only customer metrics processed

10. Future Improvements
🔹 Hyperparameter tuning
🔹 Gradient Boosting methods
🔹 Real-time data pipeline
🔹 Automated monitoring dashboard