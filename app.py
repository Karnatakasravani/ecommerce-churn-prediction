import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from sklearn.metrics import confusion_matrix, roc_curve, auc
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
# LOAD MODEL (CACHED)
# --------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/random_forest_model.pkl")

model = load_model()

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
        features = np.array([
            recency,
            frequency,
            monetary,
            avg_days,
            total_items,
            unique_products
        ]).reshape(1, -1)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

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

    st.markdown("Upload a CSV file containing customer features.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview")
        st.dataframe(df.head())

        try:
            predictions = model.predict(df)
            probabilities = model.predict_proba(df)[:, 1]

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
        except Exception as e:
            st.error("Invalid input format. Please check column names.")

# --------------------------------------------------
# PAGE 4: MODEL PERFORMANCE DASHBOARD
# --------------------------------------------------
elif page == "Model Performance Dashboard":
    st.title("📊 Model Performance Dashboard")

    st.markdown("These metrics are calculated from the real validation dataset.")

    # ------------------------------
    # Load test data
    # ------------------------------
    try:
        X_test = pd.read_csv("data/processed/X_test.csv")
        y_test = pd.read_csv("data/processed/y_test.csv").values.ravel()

        # Predict
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # ------------------------------
        # METRICS
        # ------------------------------
        roc_auc = auc(*roc_curve(y_test, y_prob)[:2])
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)

        metrics = {
            "Accuracy": round(accuracy, 3),
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1 Score": round(f1, 3),
            "ROC-AUC": round(roc_auc, 3),
        }

        cols = st.columns(len(metrics))
        for col, (k, v) in zip(cols, metrics.items()):
            col.metric(k, v)

        # ------------------------------
        # CONFUSION MATRIX
        # ------------------------------
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

        # ------------------------------
        # ROC CURVE
        # ------------------------------
        st.subheader("ROC Curve")

        fpr, tpr, _ = roc_curve(y_test, y_prob)

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"ROC Curve (AUC = {roc_auc:.3f})"
        ))

        fig2.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random Model",
            line=dict(dash="dash")
        ))

        fig2.update_layout(
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            width=800,
            height=500
        )

        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error("❌ Could not load evaluation data.")
        st.code(str(e))
        st.info("Make sure X_test.csv & y_test.csv exist in data/processed/")


# --------------------------------------------------
# PAGE 5: ABOUT / DOCUMENTATION
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
