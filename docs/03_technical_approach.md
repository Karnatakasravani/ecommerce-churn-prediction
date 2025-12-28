\# Technical Approach



\## Data Source

Dataset:

Online Retail II (UCI)



Contains:

\- Invoices

\- Purchase timestamps

\- Unit prices

\- Customer IDs

\- Quantities

\- Cancellation flags



\## Churn Definition

A customer is considered \*\*churned\*\* if:

They have \*\*no purchases for more than 90 days\*\*.



\## Feature Engineering

\### RFM Features

\- Recency (days since last order)

\- Frequency (number of purchases)

\- Monetary value (total spend)



\### Behavioral Features

\- Purchase frequency

\- Order value patterns

\- Product diversity

\- Quantity statistics



\### Temporal Features

\- Active lifetime

\- Gaps between orders

\- Monthly engagement



\## Modeling

Algorithms tested:

\- Logistic Regression

\- Random Forest



Train-test split:

\- 80 / 20

\- Stratified



Scaling:

\- StandardScaler (where needed)



Evaluation Metrics:

\- ROC-AUC

\- Precision

\- Recall

\- F1-Score

\- Confusion Matrix



\## Deployment

\- Streamlit Web App

\- Batch CSV Upload

\- Docker container support

\- Streamlit Cloud hosting



