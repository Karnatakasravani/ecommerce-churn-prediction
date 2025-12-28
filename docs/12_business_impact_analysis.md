\# Business Impact Analysis



---



\## 1. Purpose

Translate churn model performance into financial terms.



---



\## 2. Confusion Matrix Interpretation

Based on test set of N customers:



| Term | Meaning |

|------|--------|

| TP | Correctly predicted churners |

| FP | Incorrectly flagged churners |

| TN | Correctly predicted active |

| FN | Missed churners |



---



\## 3. Assumptions

\- Retention campaign cost per customer: £10

\- Average customer lifetime value: £600

\- Churn Rate: X%



---



\## 4. Scenario — Without Model

Marketing contacts all customers.



Cost =  N × £10





Expected churn prevented = random



---



\## 5. Scenario — With Model

Marketing contacts only predicted churners.



Cost =  (TP + FP) × £10



Value saved =  TP × £600



ROI =  (Value Saved − Campaign Cost) ÷ Cost





---



\## 6. Expected Outcomes

1\. Lower churn

2\. Lower campaign cost

3\. Higher ROI



---



\## 7. Recommendations

\- Target customers with high churn probability

\- Prioritize high-value users

\- Use personalized offers

\- Continuously monitor results



---



\## 8. Risks

\- False positives increase cost

\- False negatives lose revenue

\- Model drift may occur



---



\## 9. Limitations

\- Static threshold

\- Assumes equal CLV

\- Seasonality not included



---



\## 10. Next Steps

\- A/B test campaigns

\- Automate scoring pipeline

\- Track uplift impact



