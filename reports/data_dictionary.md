# Enterprise Data Dictionary

| Column Name | SQL Data Type | Source Layer | Description | Business Rules & Permitted Values |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(50)` | Staging / Raw | Unique customer identifier | Primary Key; 10-char format `XXXXX-XXXXX` |
| `gender` | `VARCHAR(20)` | Staging / Raw | Customer biological gender | `'Male'`, `'Female'` |
| `senior_citizen` | `BOOLEAN` | Clean / Derived | Senior citizen age indicator | `TRUE` if >= 65 years, else `FALSE` |
| `has_partner` | `BOOLEAN` | Clean / Derived | Marital / partner status | `TRUE` if customer has a partner, else `FALSE` |
| `has_dependents` | `BOOLEAN` | Clean / Derived | Dependent family member flag | `TRUE` if customer has dependents, else `FALSE` |
| `tenure_months` | `INTEGER` | Clean | Customer lifetime in months | Value range: `0` to `72` months |
| `phone_service` | `VARCHAR(10)` | Clean | Phone service subscription | `'Yes'`, `'No'` |
| `multiple_lines` | `VARCHAR(30)` | Clean | Multiple voice lines indicator | `'Yes'`, `'No'`, `'No phone service'` |
| `internet_service`| `VARCHAR(30)` | Clean | Digital connection type | `'DSL'`, `'Fiber optic'`, `'No'` |
| `online_security` | `VARCHAR(30)` | Clean | Add-on security suite | `'Yes'`, `'No'`, `'No internet service'` |
| `online_backup` | `VARCHAR(30)` | Clean | Add-on cloud backup | `'Yes'`, `'No'`, `'No internet service'` |
| `device_protection`| `VARCHAR(30)`| Clean | Hardware warranty plan | `'Yes'`, `'No'`, `'No internet service'` |
| `tech_support` | `VARCHAR(30)` | Clean | Dedicated technical support | `'Yes'`, `'No'`, `'No internet service'` |
| `streaming_tv` | `VARCHAR(30)` | Clean | TV streaming add-on | `'Yes'`, `'No'`, `'No internet service'` |
| `streaming_movies`| `VARCHAR(30)` | Clean | Movie streaming add-on | `'Yes'`, `'No'`, `'No internet service'` |
| `contract_type` | `VARCHAR(30)` | Clean | Subscription commitment term | `'Month-to-month'`, `'One year'`, `'Two year'` |
| `paperless_billing`| `BOOLEAN` | Clean / Derived | Digital electronic invoicing | `TRUE` if paperless, else `FALSE` |
| `payment_method` | `VARCHAR(50)` | Clean | Billing payment instrument | `'Electronic check'`, `'Mailed check'`, `'Bank transfer (auto)'`, `'Credit card (auto)'` |
| `monthly_charges` | `NUMERIC(10,2)`| Clean | Monthly Recurring Revenue (MRR)| Range: `$18.25` to `$118.75` |
| `total_charges` | `NUMERIC(12,2)`| Clean | Lifetime cumulative spend | Range: `$0.00` to `$8,684.80` (0 for tenure=0) |
| `churn_status` | `VARCHAR(10)` | Clean | Churn event indicator | `'Churned'`, `'Retained'` |
| `is_churned` | `BOOLEAN` | Clean / Derived | Boolean churn flag | `TRUE` if Churned, `FALSE` if Retained |
| `mrr_at_risk` | `NUMERIC(10,2)`| Clean / Derived | Exposed recurring revenue | `monthly_charges` if Churned, else `$0.00` |
| `tenure_band` | `VARCHAR(30)` | Clean / Derived | Grouped tenure lifecycle cohort| `'0-6 Months'`, `'7-12 Months'`, `'13-24 Months'`, `'25-36 Months'`, `'37-48 Months'`, `'49-60 Months'`, `'60+ Months'` |
| `mrr_tier` | `VARCHAR(30)` | Clean / Derived | Revenue contribution bracket | `'Low (<$35)'`, `'Medium ($35-$75)'`, `'High (>$75)'` |
| `churn_risk_tier`| `VARCHAR(30)` | Clean / Derived | Operational churn risk level | `'High Risk'`, `'Medium Risk'`, `'Low Risk'` |
| `risk_segment` | `VARCHAR(50)` | Clean / Derived | 2x2 Strategic Matrix Tier | `'Tier 1: Critical'`, `'Tier 2: High Churn / Low MRR'`, `'Tier 3: High MRR / Low Churn'`, `'Tier 4: Stable Base'` |
