-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 07_churn_analysis.sql
-- Description: Comprehensive churn driver analysis across product, service & demographics.
-- ============================================================================

-- 1. Overall Baseline Churn & Retention Metrics
SELECT 
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    COUNT(*) FILTER (WHERE NOT is_churned) AS retained_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS overall_churn_rate_pct,
    ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS overall_retention_rate_pct,
    SUM(mrr) AS total_mrr,
    SUM(mrr_at_risk) AS total_mrr_at_risk,
    ROUND((SUM(mrr_at_risk) / SUM(mrr)) * 100, 2) AS overall_mrr_at_risk_pct
FROM analytics.vw_customer_churn_clean;

-- 2. Churn Drivers by Contract Type
SELECT 
    contract_type,
    COUNT(*) AS customer_count,
    COUNT(*) FILTER (WHERE is_churned) AS churned_count,
    COUNT(*) FILTER (WHERE NOT is_churned) AS retained_count,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct,
    SUM(mrr) AS contract_mrr,
    SUM(mrr_at_risk) AS contract_mrr_at_risk,
    ROUND((SUM(mrr_at_risk) / (SELECT SUM(mrr_at_risk) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS pct_share_of_all_churn_mrr
FROM analytics.vw_customer_churn_clean
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- 3. Churn Drivers by Payment Method
SELECT 
    payment_method,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct,
    SUM(mrr_at_risk) AS mrr_at_risk,
    RANK() OVER (ORDER BY (COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) DESC) AS churn_rank
FROM analytics.vw_customer_churn_clean
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- 4. Churn Drivers by Internet Service & Support Add-ons
SELECT 
    internet_service,
    tech_support,
    online_security,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct,
    SUM(mrr_at_risk) AS mrr_at_risk
FROM analytics.vw_customer_churn_clean
GROUP BY internet_service, tech_support, online_security
ORDER BY total_customers DESC;

-- 5. Churn Drivers by Demographics (Senior, Partner, Dependents)
SELECT 
    CASE WHEN senior_citizen THEN 'Senior' ELSE 'Non-Senior' END AS senior_status,
    CASE WHEN has_partner THEN 'Partner' ELSE 'No Partner' END AS partner_status,
    CASE WHEN has_dependents THEN 'Dependents' ELSE 'No Dependents' END AS dependent_status,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct,
    SUM(mrr_at_risk) AS mrr_at_risk
FROM analytics.vw_customer_churn_clean
GROUP BY 1, 2, 3
ORDER BY churn_rate_pct DESC;
