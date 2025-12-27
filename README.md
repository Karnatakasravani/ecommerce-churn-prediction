# 🛒 E-Commerce Customer Churn Prediction

This project focuses on predicting **customer churn** for an e-commerce business using transactional data.
It covers the **complete machine learning lifecycle** including data preprocessing, feature engineering,
model training, evaluation, deployment using **Streamlit**, and containerization with **Docker**.

---

## 🔗 Live Application
👉 **Streamlit App URL:**  
https://ecommerce-churn-prediction-gpp.streamlit.app/

---

## 📂 Project Structure
ecommerce-churn-prediction/
├── app.py # Streamlit web application
├── requirements.txt # Python dependencies
├── submission.json # Submission metadata
├── Dockerfile # Docker image configuration
├── docker-compose.yml # Docker service configuration
├── models/ # Trained ML models (.pkl files)
├── data/ # Dataset (raw & processed)
├── src/ # Data pipeline scripts (optional structure)
└── README.md # Project documentation


---

## 📊 Dataset Information

- **Dataset Name:** Online Retail II
- **Source:** UCI Machine Learning Repository
- **Initial Records:** 541,910
- **After Cleaning:** 392,733
- **Data Retention:** ~72.47%

The dataset contains historical purchase transactions including:
- Invoice details
- Product quantities
- Customer identifiers
- Purchase timestamps

---

## 🧹 Data Processing & Feature Engineering

### Data Cleaning
- Removed missing `CustomerID` values
- Removed invalid quantities and cancellations
- Filtered inconsistent records

### Feature Engineering
Customer-level features were created including:
- RFM features (Recency, Frequency, Monetary)
- Purchase behavior features
- Temporal activity features
- Order statistics

More than **25 meaningful features** were generated to model churn behavior.

---

## 🤖 Model Training & Evaluation

### Models Trained
- Logistic Regression
- Random Forest
- XGBoost

### Best Model
- **Random Forest Classifier**

### Evaluation Metrics
- ROC-AUC Score > 0.65
- Balanced churn classification
- Confusion matrix & ROC curve visualized in dashboard

---

## 🌐 Streamlit Web Application

The Streamlit app provides:

1. **Home / Overview**
   - Project summary and dataset statistics

2. **Single Customer Prediction**
   - Input customer features
   - Predict churn probability
   - Actionable recommendation

3. **Batch Prediction**
   - Upload CSV file
   - Download predictions

4. **Model Performance Dashboard**
   - Metrics
   - ROC curve
   - Confusion matrix

5. **Documentation Page**
   - Usage instructions
   - Feature explanations

---

## 🐳 Docker Setup

The project includes a complete Docker setup.

### Files:
- `Dockerfile`
- `docker-compose.yml`

### Run with Docker:
```bash
docker compose build
docker compose up

The application runs on: "http://localhost:8501"

🚀 Deployment
Platform: Streamlit Cloud
Access: Public URL (no login required)
The live deployment satisfies all evaluation requirements.

⚠️ Challenges Faced
Handling large datasets efficiently
Feature aggregation at customer level
Docker network and image pull issues in restricted environments
