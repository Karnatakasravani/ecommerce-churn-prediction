\# Data Cleaning Strategy



\## Objective

Describe the approach used to transform raw transactional data into a reliable modeling dataset while minimizing information loss.



---



\## 1. Data Sources

\- Raw dataset: Online Retail II (UCI)

\- Sheet: Year 2010–2011

\- Rows before cleaning: \[add]

\- Columns: \[add]



---



\## 2. Key Data Quality Issues Identified

1\. Missing Customer ID

2\. Cancelled orders (Invoice starting with “C”)

3\. Negative or zero quantities

4\. Duplicate rows

5\. Date format inconsistencies



---



\## 3. Cleaning Rules Applied



\### ✔ Rule 1 — Remove rows without Customer ID

Reason:

\- Customers cannot be identified

\- Prevents wrong grouping



Impact:

\- Rows removed: \[add]



---



\### ✔ Rule 2 — Remove cancelled orders

Condition:





Reason:

\- These represent returns / credit notes

\- Not actual purchases



Impact:

\- Rows removed: \[add]



---



\### ✔ Rule 3 — Remove negative or zero quantities

Reason:

\- Indicates reversal transactions

\- Unrealistic for purchase behavior



Impact:

\- Rows removed: \[add]



---



\### ✔ Rule 4 — Remove exact duplicate rows

Reason:

\- Prevents data leakage

\- Avoids overcounting



Impact:

\- Rows removed: \[add]



---



\## 4. Final Dataset Retained



| Stage | Rows |

|------|------:|

| Before cleaning | X |

| After cleaning | Y |

| % Retained | Z% |



---



\## 5. Assumptions

\- Missing Customer ID = guest user → excluded

\- Cancelled transactions = not purchases

\- Churn is determined based on last purchase recency

\- Only retail customers considered



---



\## 6. Risks \& Mitigation

| Risk | Impact | Mitigation |

|------|--------|-----------|

| Removing valid negative transactions | Medium | Manual review |

| Customer ID missing for VIPs | Low | Document decision |

| Seasonal gaps mistaken as churn | Medium | Use threshold 90 days |



---



\## 7. Validation Checks

\- No NULL in Customer ID

\- No duplicate rows

\- Quantity > 0 only

\- Date format = datetime

\- Churn logic verified



---



\## 8. Conclusion

The cleaned dataset is now:

\- Accurate

\- Consistent

\- Ready for feature engineering





