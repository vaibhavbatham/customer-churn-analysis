# Automated Cross-Tool Analytical Reconciliation Report

This audit report cross-validates analytical calculations across all four layers of the analytics stack: **PostgreSQL (Database Layer) ↔ Python (Analytical Pipeline) ↔ Microsoft Excel (Financial Pivot Layer) ↔ Power BI (DAX Modeling)**.

| Metric | PostgreSQL | Python | Excel Pivot | Power BI DAX | Variance | Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| Total Customers (Census) | 7,043 | 7,043 | 7,043 | 7,043 | 0.00% | PASS |
| Total Churned Customers | 1,869 | 1,869 | 1,869 | 1,869 | 0.00% | PASS |
| Total Retained Base | 5,174 | 5,174 | 5,174 | 5,174 | 0.00% | PASS |
| Overall Churn Rate (%) | 26.54% | 26.54% | 26.54% | 26.54% | 0.00% | PASS |
| Overall Retention Rate (%) | 73.46% | 73.46% | 73.46% | 73.46% | 0.00% | PASS |
| Total Monthly Recurring Revenue (MRR) | $456,116.60 | $456,116.60 | $456,116.60 | $456,116.60 | 0.00% | PASS |
| MRR at Risk (Lost MRR) | $139,130.85 | $139,130.85 | $139,130.85 | $139,130.85 | 0.00% | PASS |
| % MRR at Risk | 30.50% | 30.50% | 30.50% | 30.50% | 0.00% | PASS |
| Month-to-Month Churn Rate (%) | 42.71% | 42.71% | 42.71% | 42.71% | 0.00% | PASS |
| Month-to-Month MRR at Risk ($) | $120,847.10 | $120,847.10 | $120,847.10 | $120,847.10 | 0.00% | PASS |
| 0-6M Early Tenure Churn Rate (%) | 52.94% | 52.94% | 52.94% | 52.94% | 0.00% | PASS |
| 60+ Months Active Retention Rate (%) | 93.32% | 93.32% | 93.32% | 93.32% | 0.00% | PASS |

**Reconciliation Audit Summary:**
- **Total Metrics Tested:** 12 Core Business & Financial KPIs
- **Numerical Variance:** **0.00% across all tools**
- **Audit Outcome:** 100% PASS — Zero calculation discrepancy between SQL, Python, Excel, and Power BI.
