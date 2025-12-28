\# Feature Dictionary



This document explains the engineered features used for modeling customer churn.



---



\## 1. RFM Features



| Feature | Meaning | Business Interpretation |

|--------|--------|-------------------------|

| Recency | Days since last purchase | Higher = more likely churn |

| Frequency | Number of purchase occasions | Higher = loyal |

| Monetary | Total spending | Higher = high-value |



---



\## 2. Purchase Behaviour Features



| Feature | Description | Insight |

|--------|-------------|--------|

| avg\_quantity\_per\_order | Mean units per order | Basket size |

| max\_quantity | Largest single purchase | Bulk buying indicator |

| min\_quantity | Lowest quantity | Edge-case detection |

| std\_quantity | Variation in quantity | Stability of buying |

| total\_items\_purchased | Total units purchased | Engagement level |

| unique\_products | Distinct products purchased | Product diversity |

| unique\_invoices | Distinct order count | Purchase occasions |



---



\## 3. Monetary Behaviour Features



| Feature | Description | Insight |

|--------|-------------|--------|

| total\_revenue | Lifetime spend | Value contributed |

| avg\_order\_value | Spend per order | Ticket size |

| max\_order\_value | Peak purchase | VIP signals |

| min\_order\_value | Lowest spend | Discount behaviour |

| std\_order\_value | Spend variability | Stability |

| revenue\_per\_item | Spend per product | Price sensitivity |



---



\## 4. Temporal Behaviour Features



| Feature | Description | Insight |

|--------|-------------|--------|

| active\_days | Days with purchases | Activity frequency |

| active\_months | Active months | Long-term value |

| customer\_tenure\_days | Active duration | Loyalty period |

| avg\_days\_between\_orders | Order interval | Regularity |

| purchase\_span\_days | Lifecycle period | Customer maturity |



---



\## 5. Stability Features



| Feature | Description | Purpose |

|--------|-------------|--------|

| order\_consistency | Frequency ÷ tenure | Buying regularity |

| spend\_consistency | Avg spend ÷ variance | Risk behaviour |



---



\## 6. Target Variable



| Field | Meaning |

|------|--------|

| Churn | 1 = churned, 0 = active |



Definition:  

A customer is churned if \*\*Recency > 90 days\*\*



