\# Model Selection Report



---



\## 1. Goal

Select the best predictive model for customer churn.



---



\## 2. Models Evaluated

\- Logistic Regression

\- Random Forest



---



\## 3. Evaluation Metric

Primary metric:



✔ ROC-AUC  

Reason:

\- Handles imbalance

\- Measures ranking quality

\- Industry standard



Secondary metrics:

\- Recall

\- Precision

\- Accuracy

\- F1-score



---



\## 4. Cross-Validation

5-Fold Stratified



\- Ensures class balance per fold

\- Reduces variance



---



\## 5. Results Summary



| Model | ROC-AUC | Recall | Precision |

|------|--------:|--------:|-----------:|

| Logistic Regression | X.XX | X.XX | X.XX |

| Random Forest | \*\*X.XX\*\* | \*\*X.XX\*\* | \*\*X.XX\*\* |



---



\## 6. Final Model Chosen

\### ✅ Random Forest Classifier



Reasons:

\- Best ROC-AUC

\- Handles nonlinear patterns

\- Robust to outliers

\- Works well with tabular data



---



\## 7. Risk Controls

\- Class weighting used

\- Scaling applied where needed

\- Overfitting checked via CV



---



\## 8. Model Explainability

Top features:



1\. Recency  

2\. Frequency  

3\. Monetary  

4\. Tenure  

5\. Avg Order Value  



---



\## 9. Business Justification

\- Stable performance

\- High interpretability via feature ranking

\- Suitable for operational deployment



---



\## 10. Saved Artifacts

Stored in `models/`



\- best\_model.pkl  

\- scaler.pkl



