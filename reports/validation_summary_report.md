# Data Quality & Cross-Tool Reconciliation Audit Report

## 1. Data Ingestion & Integrity Audit
- **Target Customer Population:** Exactly 7,043 Customer Records.
- **Ingestion Audit Result:** Exactly 7,043 rows loaded; 0 duplicate customer IDs.
- **Primary Key Uniqueness:** `customerID` verified 100% unique (7,043 distinct keys).

## 2. Missing Value Investigation & Business Treatment
- **Audit Finding:** The raw `TotalCharges` field contained 11 whitespace records (`' '`).
- **Deep-Dive Audit:**
  - All 11 records have `tenure = 0`.
  - All 11 records have `Churn = 'No'`.
  - All 11 records represent active, newly enrolled accounts who joined within the current billing cycle and have not yet been billed.
- **Documented Treatment Decision:**
  - Imputed `TotalCharges = 0.00` rather than dropping records or imputing column averages.
  - Retained all 11 records in the active analytical population, preserving the exact 7,043 customer census.

## 3. Cross-Tool Metric Parity & Reconciliation Matrix

| Metric Name | PostgreSQL Query | Python (Pandas) | Excel Workbook | Power BI DAX | Variance | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Customers** | 7,043 | 7,043 | 7,043 | 7,043 | 0.00% | **RECONCILED (Exact)** |
| **Churned Customers** | 1,869 | 1,869 | 1,869 | 1,869 | 0.00% | **RECONCILED (Exact)** |
| **Retained Customers** | 5,174 | 5,174 | 5,174 | 5,174 | 0.00% | **RECONCILED (Exact)** |
| **Overall Churn Rate** | 26.54% | 26.54% | 26.54% | 26.54% | 0.00% | **RECONCILED (Exact)** |
| **Overall Retention Rate**| 73.46% | 73.46% | 73.46% | 73.46% | 0.00% | **RECONCILED (Exact)** |
| **Total MRR** | $456,116.60 | $456,116.60 | $456,116.60 | $456,116.60 | 0.00% | **RECONCILED (Exact)** |
| **MRR at Risk ($)** | $139,130.85 | $139,130.85 | $139,130.85 | $139,130.85 | 0.00% | **RECONCILED (Exact)** |
| **MRR at Risk (%)** | 30.50% | 30.50% | 30.50% | 30.50% | 0.00% | **RECONCILED (Exact)** |
| **0-6M Tenure Retention** | 47.06% | 47.06% | 47.06% | 47.06% | 0.00% | **RECONCILED (Exact)** |
| **5-Year Cohort Retention**| 93.32% | 93.32% | 93.32% | 93.32% | 0.00% | **RECONCILED (Exact)** |
