-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 05_data_cleaning.sql
-- Description: Cleans data, handles missing values, and builds analytical views.
-- ============================================================================

-- Populate dim_customers table with cleaned and typed data
INSERT INTO analytics.dim_customers (
    customer_id,
    gender,
    senior_citizen,
    has_partner,
    has_dependents,
    tenure_months,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract_type,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges,
    churn_status,
    is_churned
)
SELECT 
    TRIM(customer_id) AS customer_id,
    INITCAP(TRIM(gender)) AS gender,
    CASE WHEN senior_citizen = 1 THEN TRUE ELSE FALSE END AS senior_citizen,
    CASE WHEN partner = 'Yes' THEN TRUE ELSE FALSE END AS has_partner,
    CASE WHEN dependents = 'Yes' THEN TRUE ELSE FALSE END AS has_dependents,
    tenure AS tenure_months,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract AS contract_type,
    CASE WHEN paperless_billing = 'Yes' THEN TRUE ELSE FALSE END AS paperless_billing,
    payment_method,
    monthly_charges,
    -- Impute blank total_charges as 0.00 for new customers with tenure = 0
    COALESCE(NULLIF(TRIM(total_charges), '')::NUMERIC(12, 2), 0.00) AS total_charges,
    churn AS churn_status,
    CASE WHEN churn = 'Yes' THEN TRUE ELSE FALSE END AS is_churned
FROM staging.stg_customer_churn
ON CONFLICT (customer_id) DO NOTHING;

-- Create Analytical Clean View with Derived Business Fields
CREATE OR REPLACE VIEW analytics.vw_customer_churn_clean AS
SELECT 
    customer_id,
    gender,
    senior_citizen,
    has_partner,
    has_dependents,
    tenure_months,
    
    -- Derived Tenure Band
    CASE 
        WHEN tenure_months <= 6 THEN '0-6 Months'
        WHEN tenure_months <= 12 THEN '7-12 Months'
        WHEN tenure_months <= 24 THEN '13-24 Months'
        WHEN tenure_months <= 36 THEN '25-36 Months'
        WHEN tenure_months <= 48 THEN '37-48 Months'
        WHEN tenure_months <= 60 THEN '49-60 Months'
        ELSE '60+ Months'
    END AS tenure_band,
    
    -- Tenure Order for Sort
    CASE 
        WHEN tenure_months <= 6 THEN 1
        WHEN tenure_months <= 12 THEN 2
        WHEN tenure_months <= 24 THEN 3
        WHEN tenure_months <= 36 THEN 4
        WHEN tenure_months <= 48 THEN 5
        WHEN tenure_months <= 60 THEN 6
        ELSE 7
    END AS tenure_band_order,

    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract_type,
    paperless_billing,
    payment_method,
    monthly_charges AS mrr,
    total_charges,
    churn_status,
    is_churned,
    
    -- Customer Status label
    CASE WHEN is_churned THEN 'Churned' ELSE 'Retained' END AS customer_status,
    
    -- MRR at Risk (exposed recurring monthly revenue)
    CASE WHEN is_churned THEN monthly_charges ELSE 0.00 END AS mrr_at_risk,
    
    -- Monthly Charges Tier
    CASE 
        WHEN monthly_charges < 35.00 THEN 'Low (<)'
        WHEN monthly_charges <= 75.00 THEN 'Medium (-)'
        ELSE 'High (>)'
    END AS mrr_tier,
    
    -- Churn Risk Tier
    CASE 
        WHEN contract_type = 'Month-to-month' AND tenure_months <= 12 THEN 'High Risk'
        WHEN contract_type = 'Month-to-month' OR tenure_months <= 12 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS churn_risk_tier
FROM analytics.dim_customers;

-- Verify Clean View Count
SELECT COUNT(*) AS verified_clean_count FROM analytics.vw_customer_churn_clean;
