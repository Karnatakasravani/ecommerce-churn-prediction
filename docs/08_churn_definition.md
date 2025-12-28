\# Churn Definition



---



\## 1. Business Definition



Churned Customer  

➡ A customer who \*\*has not made a purchase in the last 90 days\*\* from their most recent transaction date.



Active Customer  

➡ A customer with \*\*at least one purchase within the last 90 days\*\*.



---



\## 2. Why 90 Days?



Reasoning:

\- Retail industry typical repeat cycle

\- Matches dataset seasonality

\- Avoids false churn during long gaps

\- Simple + explainable



---



\## 3. Technical Definition



Recency = days since last purchase

Churn = 1 if Recency > 90

Churn = 0 otherwise





---



\## 4. Impact on Model



| Area | Impact |

|------|--------|

| Label assignment | Direct |

| Churn rate | Controls class balance |

| Business ROI | Affects savings estimates |



---



\## 5. Assumptions

\- All customers have equal churn risk

\- Seasonality minimal beyond 90 days

\- Customers do not pause accounts



---



\## 6. Limitations

\- VIP customers may return later

\- Seasonal buyers unfairly marked churned



---



\## 7. Future Improvement

\- Segment-based thresholds

\- Probabilistic churn scoring

\- Time-to-churn modelling



