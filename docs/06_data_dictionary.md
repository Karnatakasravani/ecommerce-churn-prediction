\# Data Dictionary



This document describes all key fields used in the project.



---



\## 1. Original Dataset Fields



| Field | Description | Type | Example |

|------|-------------|------|--------|

| Invoice | Unique transaction ID | String | 536365 |

| StockCode | Product ID | String | 85123A |

| Description | Product name | String | WHITE HANGING HEART T-LIGHT HOLDER |

| Quantity | Units purchased | Integer | 6 |

| InvoiceDate | Transaction date \& time | Datetime | 2010-12-01 |

| Price | Total price | Float | 15.00 |

| Customer ID | Unique customer reference | Float | 17850 |

| Country | Customer country | String | United Kingdom |



---



\## 2. Engineered Features



| Feature | Meaning | Type |

|--------|--------|------|

| Recency | Days since last purchase | Integer |

| Frequency | Number of purchase occasions | Integer |

| Monetary | Total spend | Float |

| avg\_quantity\_per\_order | Avg units per purchase | Float |

| total\_items\_purchased | Total quantity bought | Integer |

| unique\_products | Number of distinct product codes | Integer |

| unique\_invoices | Distinct invoices | Integer |

| total\_revenue | Lifetime value | Float |

| avg\_order\_value | Average transaction spend | Float |

| std\_order\_value | Variability in spend | Float |

| active\_days | Active purchasing days | Integer |

| active\_months | Active months | Integer |

| customer\_tenure\_days | Days active as a customer | Integer |

| avg\_days\_between\_orders | Purchase interval | Float |

| order\_consistency | Frequency / tenure | Float |

| spend\_consistency | Avg spend relative to variance | Float |

| Churn | Target: 1 = churned | Binary |



---



\## 3. Target Definition

A customer is labeled \*\*Churned (1)\*\* if: Recency > 90 days





Otherwise \*\*Active (0)\*\*.



---



\## 4. Data Types Summary

\- Numerical: metrics + features

\- Categorical: none (after processing)

\- Datetime: InvoiceDate



---



\## 5. Notes

\- All monetary values are assumed GBP

\- Missing values handled during cleaning



