-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 03_load_data.sql
-- Description: Ingests the 7,043 raw customer records into the staging table.
-- ============================================================================

-- Truncate staging table prior to ingestion
TRUNCATE TABLE staging.stg_customer_churn;

-- PostgreSQL COPY command to load CSV data
-- Adjust filepath to the environment location
COPY staging.stg_customer_churn (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges,
    churn
)
FROM '/path/to/customer-churn-analysis/data/raw/customer_churn_raw.csv'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    ENCODING 'UTF8'
);

-- Verification of loaded record count
SELECT 
    COUNT(*) AS total_staging_rows,
    CASE 
        WHEN COUNT(*) = 7043 THEN 'PASS: Exactly 7,043 customer records loaded.'
        ELSE 'FAIL: Row count discrepancy detected!'
    END AS load_status
FROM staging.stg_customer_churn;
