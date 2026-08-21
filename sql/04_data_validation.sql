-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 04_data_validation.sql
-- Description: Comprehensive data quality audit and validation queries.
-- ============================================================================

-- 1. Check Total Row Count & Unique Customer IDs
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) - COUNT(DISTINCT customer_id) AS duplicate_customer_ids
FROM staging.stg_customer_churn;

-- 2. Identify Duplicate Records (if any)
SELECT 
    customer_id,
    COUNT(*) AS occurrence_count
FROM staging.stg_customer_churn
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 3. Audit Missing / NULL Values Across Core Columns
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL OR TRIM(customer_id) = '') AS missing_customer_ids,
    COUNT(*) FILTER (WHERE tenure IS NULL) AS missing_tenure,
    COUNT(*) FILTER (WHERE monthly_charges IS NULL) AS missing_monthly_charges,
    COUNT(*) FILTER (WHERE total_charges IS NULL OR TRIM(total_charges) = '') AS missing_total_charges,
    COUNT(*) FILTER (WHERE contract IS NULL OR TRIM(contract) = '') AS missing_contract,
    COUNT(*) FILTER (WHERE churn IS NULL OR TRIM(churn) = '') AS missing_churn
FROM staging.stg_customer_churn;

-- 4. Deep-Dive: Investigate the 11 Missing / Blank TotalCharges Records
-- RATIONALE: All 11 records have tenure = 0 and churn = 'No' (new subscribers who haven't completed month 1)
SELECT 
    customer_id,
    tenure,
    contract,
    payment_method,
    monthly_charges,
    total_charges,
    churn
FROM staging.stg_customer_churn
WHERE TRIM(total_charges) = '' OR total_charges IS NULL;

-- 5. Range & Boundary Sanity Checks
SELECT 
    MIN(tenure) AS min_tenure,
    MAX(tenure) AS max_tenure,
    MIN(monthly_charges) AS min_monthly_charges,
    MAX(monthly_charges) AS max_monthly_charges,
    COUNT(*) FILTER (WHERE tenure < 0) AS invalid_negative_tenure,
    COUNT(*) FILTER (WHERE monthly_charges <= 0) AS invalid_zero_or_negative_mrr
FROM staging.stg_customer_churn;

-- 6. Categorical Value Distribution & Integrity Audit
SELECT 
    contract,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM staging.stg_customer_churn) * 100, 2) AS pct_share
FROM staging.stg_customer_churn
GROUP BY contract
ORDER BY customer_count DESC;

SELECT 
    churn,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM staging.stg_customer_churn) * 100, 2) AS pct_share
FROM staging.stg_customer_churn
GROUP BY churn;
