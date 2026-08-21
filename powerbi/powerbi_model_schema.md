# Power BI Data Model Architecture & Schema Documentation

## 1. Overview
The **Customer Churn & Revenue Risk Analysis** Power BI data model is designed as a star schema optimized for in-memory VertiPaq tabular performance, sub-second query response, and seamless cross-filtering across customer demographics, contract terms, tenure milestones, and billing channels.

```
       +-------------------------+
       |     dim_tenure_band     |
       +-------------------------+
                   | 1
                   |
                   | *
+---------------------------------------+       1 +-----------------------+
|             dim_customers             |---------|     dim_contract      |
|  (Core Fact / Dimension Table: 7,043) |       * +-----------------------+
+---------------------------------------+
                   | *
                   |
                   | 1
       +-------------------------+
       |   dim_payment_method    |
       +-------------------------+
```

---

## 2. Table Specifications

### Primary Table: `dim_customers` (7,043 rows)
Contains customer-level attributes, subscription characteristics, billing metrics, and churn outcomes.

| Column Name | Data Type | Description | Sample Values |
| :--- | :--- | :--- | :--- |
| `customerID` | Text (PK) | Unique 10-character alphanumeric customer ID | `7590-VHVEG`, `5575-GNVDE` |
| `gender` | Text | Biological gender | `Male`, `Female` |
| `SeniorCitizen` | Whole Number | Senior indicator (0/1) | `0`, `1` |
| `Partner` | Text | Has partner indicator | `Yes`, `No` |
| `Dependents` | Text | Has dependents indicator | `Yes`, `No` |
| `tenure` | Whole Number | Customer subscription lifetime in months | `1` to `72` |
| `Contract` | Text (FK) | Commitment term | `Month-to-month`, `One year`, `Two year` |
| `PaperlessBilling`| Text | Paperless billing flag | `Yes`, `No` |
| `PaymentMethod` | Text (FK) | Payment instrument | `Electronic check`, `Credit card (auto)` |
| `MonthlyCharges` | Decimal ($) | Monthly Recurring Revenue (MRR) | `18.25` to `118.75` |
| `TotalCharges_Clean`| Decimal ($) | Lifetime cumulative billing (imputed 0 for tenure=0)| `0.00` to `8684.80` |
| `Churn` | Text | Churn flag | `Yes`, `No` |
| `customer_status`| Text | Standardized status | `Churned`, `Retained` |
| `tenure_band` | Text (FK) | Binned tenure cohort | `0-6 Months`, `7-12 Months`, ... |
| `mrr_at_risk` | Decimal ($) | Exposed recurring revenue | `$0.00` if Retained, `$MC` if Churned |
| `risk_segment` | Text | 2x2 Risk-Value Matrix tier | `Tier 1: Critical`, `Tier 4: Stable Base` |

---

## 3. Relationships & Cardinality

| From: Fact/Dimension | From Column | To: Dimension | To Column | Cardinality | Cross-filter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_customers` | `Contract` | `dim_contract` | `Contract` | Many-to-One (*:1) | Single |
| `dim_customers` | `tenure_band` | `dim_tenure_band`| `tenure_band`| Many-to-One (*:1) | Single |
| `dim_customers` | `PaymentMethod` | `dim_payment_method` | `PaymentMethod` | Many-to-One (*:1) | Single |

---

## 4. Sorting & Formatting Standards
- `tenure_band` sorted by `tenure_band_order` (1 to 7) to guarantee chronological display in visuals.
- `Contract` ordered logically: `Month-to-month` -> `One year` -> `Two year`.
- Currency formatting applied globally: `\$#,##0.00`.
- Percentage formatting applied globally: `0.00%`.
