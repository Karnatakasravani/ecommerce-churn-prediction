#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import json
from pathlib import Path

RAW_DATA_PATH = Path(r"C:\Users\DELL\Desktop\GPP_task\GPP_Task3\data\online_retail_II.xlsx")


# In[8]:


import pandas as pd
print(pd.__version__)


# In[10]:


import pandas as pd
import json
from pathlib import Path

RAW_DATA_PATH = Path(r"C:\Users\DELL\Desktop\GPP_task\ecommerce-churn-prediction\data\raw\online_retail_II.xlsx")
OUTPUT_JSON = Path("data/raw/data_quality_summary.json")

print("Excel exists:", RAW_DATA_PATH.exists())


# In[12]:


import pandas as pd
import json
from pathlib import Path

RAW_DATA_PATH = Path(r"C:\Users\DELL\Desktop\GPP_task\ecommerce-churn-prediction\data\raw\online_retail_II.xlsx")
OUTPUT_JSON = Path("data/raw/data_quality_summary.json")

SHEET_NAME = "Year 2010-2011"  

raw_df = pd.read_excel(RAW_DATA_PATH, sheet_name=SHEET_NAME)
raw_df["financial_year"] = SHEET_NAME

raw_df.shape


# In[13]:


raw_df.head()
raw_df.info()
raw_df.isnull().sum()


# In[17]:


rows_before = raw_df.shape[0]

clean_df = raw_df.dropna(subset=["Customer ID"])

rows_after = clean_df.shape[0]

retention = (rows_after / rows_before) * 100

rows_before, rows_after, retention


# In[21]:


clean_df["Invoice"].astype(str).str.startswith("C").sum()


# In[23]:


clean_df = clean_df[~clean_df["Invoice"].astype(str).str.startswith("C")]


# In[24]:


rows_after_cancel = clean_df.shape[0]
retention_after_cancel = (rows_after_cancel / rows_before) * 100
rows_after_cancel, retention_after_cancel


# In[25]:


(clean_df["Quantity"] <= 0).sum()


# In[26]:


clean_df.duplicated().sum()


# In[27]:


clean_df = clean_df.drop_duplicates()


# In[28]:


rows_after_dup = clean_df.shape[0]
final_retention = (rows_after_dup / rows_before) * 100
rows_after_dup, final_retention


# In[29]:


reference_date = clean_df["InvoiceDate"].max() + pd.Timedelta(days=1)
reference_date


# ### RFM stands for:
# - Recency	-Days since last purchase
# - Frequency	-Number of purchases
# - Monetary	-Total spend

# In[39]:


rfm = clean_df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (reference_date - x.max()).days,
    "Invoice": "nunique",
    "Price": "sum"
}).reset_index()

rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]

rfm


# In[42]:


CHURN_THRESHOLD = 90

rfm["Churn"] = (rfm["Recency"] > CHURN_THRESHOLD).astype(int)

rfm["Churn"].value_counts()


# In[43]:


churned_customers = rfm["Churn"].sum()
total_customers = rfm.shape[0]

churn_rate = (churned_customers / total_customers) * 100
churn_rate


# In[40]:


rfm.describe()


# - avg_quantity_per_order -	Average units bought per transaction
# - max_quantity - Largest single-order quantity
# - min_quantity - Smallest purchase quantity
# - std_quantity - Purchase variability
# - total_items_purchased - Total items bought
# - unique_products -	Product diversity
# - unique_invoices -	Purchase frequency proxy

# In[46]:


purchase_features = clean_df.groupby("Customer ID").agg(
    avg_quantity_per_order=("Quantity", "mean"),
    max_quantity=("Quantity", "max"),
    min_quantity=("Quantity", "min"),
    std_quantity=("Quantity", "std"),
    total_items_purchased=("Quantity", "sum"),
    unique_products=("StockCode", "nunique"),
    unique_invoices=("Invoice", "nunique")
).reset_index()

purchase_features.head()


# In[49]:


purchase_features.isnull().sum()
purchase_features["std_quantity"] = purchase_features["std_quantity"].fillna(0)
purchase_features.isnull().sum()


# In[51]:


rfm = rfm.merge(purchase_features, on="Customer ID", how="left")


# In[52]:


rfm.shape
rfm.head()


# - total_revenue	- Lifetime value so far
# - avg_order_value -	Average spend per transaction
# - max_order_value -	Highest single purchase
# - min_order_value - Smallest purchase
# - std_order_value -	Spend variability
# - revenue_per_item - Price sensitivity

# In[55]:


monetary_features = clean_df.groupby("Customer ID").agg(
    total_revenue=("Price", "sum"),
    avg_order_value=("Price", "mean"),
    max_order_value=("Price", "max"),
    min_order_value=("Price", "min"),
    std_order_value=("Price", "std"),
    total_items=("Quantity", "sum")
).reset_index()

# Revenue per item
monetary_features["revenue_per_item"] = (
    monetary_features["total_revenue"] / monetary_features["total_items"]
)

# Handle NaN (customers with single order)
monetary_features["std_order_value"] = monetary_features["std_order_value"].fillna(0)

monetary_features.head()


# In[57]:


rfm = rfm.merge(monetary_features.drop(columns=["total_items"]), 
                on="Customer ID", how="left")


# In[58]:


rfm.shape
rfm.head()


# - customer_tenure_days -	How long customer stayed active
# - active_days - Engagement intensity
# - active_months -	Consistency over months
# - avg_days_between_orders - Purchase regularity
# - purchase_span_days - Lifecycle length

# In[69]:


# Ensure InvoiceDate is datetime
clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"])

temporal_features = clean_df.groupby("Customer ID").agg(
    first_purchase_date=("InvoiceDate", "min"),
    last_purchase_date=("InvoiceDate", "max"),
    active_days=("InvoiceDate", "nunique"),
    active_months=("InvoiceDate", lambda x: x.dt.to_period("M").nunique()),
    total_orders=("Invoice", "nunique")
).reset_index()

# Reference date already defined earlier
# reference_date = clean_df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Temporal calculations
temporal_features["customer_tenure_days"] = (
    temporal_features["last_purchase_date"] - temporal_features["first_purchase_date"]
).dt.days

temporal_features["days_since_first_purchase"] = (
    reference_date - temporal_features["first_purchase_date"]
).dt.days

temporal_features["purchase_span_days"] = (
    temporal_features["last_purchase_date"] - temporal_features["first_purchase_date"]
).dt.days

# Average gap between orders
temporal_features["avg_days_between_orders"] = (
    temporal_features["purchase_span_days"] /
    (temporal_features["total_orders"] - 1)
)

# Handle customers with only 1 order
temporal_features["avg_days_between_orders"] = (
    temporal_features["avg_days_between_orders"].fillna(0)
)

temporal_features.head()


# In[77]:


rfm = rfm.merge(
    temporal_features.drop(columns=[
        "first_purchase_date",
        "last_purchase_date",
        "total_orders"
    ]),
    on="Customer ID",
    how="left"
)


# In[81]:


rfm.info()


# In[80]:


# Feature 1: Order consistency
rfm["order_consistency"] = (
    rfm["Frequency"] / rfm["customer_tenure_days"].replace(0, 1)
)

# Feature 2: Spend consistency
rfm["spend_consistency"] = (
    rfm["avg_order_value"] / (rfm["std_order_value"] + 1)
)

# Quick check
rfm[["order_consistency", "spend_consistency"]].describe()


# In[83]:


rfm.to_csv("C:/Users/DELL/Desktop/GPP_task/ecommerce-churn-prediction/data/processed/customer_features_final.csv", index=False)


# In[85]:


clean_df.info()


# In[86]:


rfm.info()


# ## Modeling

# In[90]:


from sklearn.model_selection import train_test_split

# Separate features and target
X = rfm.drop(columns=["Customer ID", "Churn"])
y = rfm["Churn"]

X.shape, y.shape


# In[91]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train.shape, X_test.shape


# In[92]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# In[93]:


from sklearn.linear_model import LogisticRegression

log_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

log_model.fit(X_train_scaled, y_train)


# In[94]:


from sklearn.metrics import roc_auc_score

y_train_proba = log_model.predict_proba(X_train_scaled)[:, 1]
train_auc = roc_auc_score(y_train, y_train_proba)

train_auc


# In[95]:


y_test_proba = log_model.predict_proba(X_test_scaled)[:, 1]
test_auc = roc_auc_score(y_test, y_test_proba)

test_auc


# In[96]:


from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=10,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)


# In[97]:


rf_test_proba = rf_model.predict_proba(X_test)[:, 1]
rf_test_auc = roc_auc_score(y_test, rf_test_proba)

rf_test_auc


# In[99]:


import joblib
from pathlib import Path

MODEL_DIR = Path("C:/Users/DELL/Desktop/GPP_task/ecommerce-churn-prediction/models")
MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(log_model, MODEL_DIR / "logistic_model.pkl")
joblib.dump(rf_model, MODEL_DIR / "random_forest_model.pkl")
joblib.dump(scaler, MODEL_DIR / "scaler.pkl")


# In[103]:


def run_pipeline():
    # ALL your existing code stays here
    pass


if __name__ == "__main__":
    run_pipeline()


# In[ ]:





# In[ ]:




