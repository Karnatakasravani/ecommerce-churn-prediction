import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="E-commerce Churn Prediction",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL + SCALER
# --------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/random_forest_model.pkl")

@st.cache_resource
def load_scaler():
    return joblib.load("models/scaler.pkl")

model = load_model()
scaler = load_scaler()

# --------------------------------------------------
# FEATURE ORDER (VERY IMPORTANT)
# --------------------------------------------------
FEATURE_COLUMNS = [
    "Recency",
    "Frequency",
    "Monetary",
    "AvgDaysBetweenOrders",
    "TotalItemsPurchased",
    "UniqueProducts"
]

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Single Customer Prediction",
        "Batch Prediction",
        "Model Performance Dashboard",
        "About"
    ]
)

# --------------------------------------------------
# PAGE 1: HOME
# --------------------------------------------------
if page == "Home":
    st.title("📦 E-commerce Customer Churn Prediction")

    st.markdown("""
    ### Project Overview
    This application predicts whether an e-commerce customer is likely to **churn**
    based on historical purchasing behavior.

    **Dataset**: Online Retail II (UCI)  
    **Model**: Random Forest  
    **Goal**: Help businesses identify at-risk customers early.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Initial Records", "541,910")
    col2.metric("After Cleaning", "392,733")
    col3.metric("Retention %", "72.47%")

    st.info("Use the sidebar to navigate between prediction modes.")

# --------------------------------------------------
# PAGE 2: SINGLE CUSTOMER PREDICTION
# --------------------------------------------------
elif page == "Single Customer Prediction":
    st.title("👤 Single Customer Prediction")

    st.markdown("Enter customer features below:")

    col1, col2, col3 = st.columns(3)

    with col1:
        recency = st.number_input("Recency (days)", 0, 500, 30)
        frequency = st.number_input("Frequency", 1, 100, 5)

    with col2:
        monetary = st.number_input("Monetary Value", 0.0, 100000.0, 500.0)
        avg_days = st.number_input("Avg Days Between Orders", 0.0, 365.0, 30.0)

    with col3:
        total_items = st.number_input("Total Items Purchased", 1, 10000, 50)
        unique_products = st.number_input("Unique Products", 1, 1000, 10)

    if st.button("Predict Churn"):
        input_df = pd.DataFrame([[
            recency,
            frequency,
            monetary,
            avg_days,
            total_items,
            unique_products
        ]], columns=FEATURE_COLUMNS)

        input_scaled = scaler.transform(input_df)

        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]

        if prediction == 1:
            st.error(f"⚠️ Customer likely to CHURN (Probability: {probability:.2f})")
            st.markdown("**Recommendation:** Offer retention incentives or promotions.")
        else:
            st.success(f"✅ Customer NOT likely to churn (Probability: {probability:.2f})")

# --------------------------------------------------
# PAGE 3: BATCH PREDICTION
# --------------------------------------------------
elif page == "Batch Prediction":
    st.title("📂 Batch Prediction")

    st.markdown("Upload a CSV file containing customer features:")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("Preview")
        st.dataframe(df.head())

        missing = [c for c in FEATURE_COLUMNS if c not in df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            X = df[FEATURE_COLUMNS]
            X_scaled = scaler.transform(X)

            predictions = model.predict(X_scaled)
            probabilities = model.predict_proba(X_scaled)[:, 1]

            df["Churn_Prediction"] = predictions
            df["Churn_Probability"] = probabilities

            st.subheader("Prediction Results")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Results",
                csv,
                "churn_predictions.csv",
                "text/csv"
            )

# --------------------------------------------------
# PAGE 4: MODEL PERFORMANCE DASHBOARD
# --------------------------------------------------
elif page == "Model Performance Dashboard":
    st.title("📊 Model Performance Dashboard")

    try:
        X_test = pd.read_csv("data/processed/X_test.csv")
        y_test = pd.read_csv("data/processed/y_test.csv").values.ravel()

        X_test = X_test[FEATURE_COLUMNS]
        X_test_scaled = scaler.transform(X_test)

        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        metrics = {
            "Accuracy": round(accuracy_score(y_test, y_pred), 3),
            "Precision": round(precision_score(y_test, y_pred), 3),
            "Recall": round(recall_score(y_test, y_pred), 3),
            "F1 Score": round(f1_score(y_test, y_pred), 3),
            "ROC-AUC": round(roc_auc, 3)
        }

        cols = st.columns(len(metrics))
        for col, (k, v) in zip(cols, metrics.items()):
            col.metric(k, v)

        # Confusion matrix
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)

        fig = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale="Blues",
            labels=dict(x="Predicted", y="Actual"),
            x=["Not Churn", "Churn"],
            y=["Not Churn", "Churn"],
            title="Confusion Matrix"
        )
        st.plotly_chart(fig, use_container_width=True)

        # ROC curve
        st.subheader("ROC Curve")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                                  name=f"ROC Curve (AUC={roc_auc:.3f})"))
        fig2.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                                  name="Random Model",
                                  line=dict(dash="dash")))
        fig2.update_layout(xaxis_title="False Positive Rate",
                           yaxis_title="True Positive Rate")
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error("Could not load evaluation data.")
        st.code(str(e))

# --------------------------------------------------
# PAGE 5: ABOUT
# --------------------------------------------------
elif page == "About":
    st.title("📘 About This Application")

    st.markdown("""
    ### How to Use
    - Use **Single Prediction** for individual customers
    - Use **Batch Prediction** to upload CSV files
    - View metrics in **Model Dashboard**

    ### Features Used
    - Recency
    - Frequency
    - Monetary value
    - Purchase behavior metrics

    ### Contact
    **Student:** Venkata Naga Sravani Karnataka  
    **Project:** Global Placement Program – ML Deployment
    """)

    st.success("Thank you for reviewing this project!")
