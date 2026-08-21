-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 10_final_analysis.sql
-- Description: Consolidated Executive Analytical View & Final Reporting Queries.
-- ============================================================================

-- Create Executive KPI Summary Table / Materialized View
CREATE OR REPLACE VIEW reporting.vw_executive_kpi_summary AS
SELECT 
    COUNT(*) AS total_customer_population,
    COUNT(*) FILTER (WHERE is_churned) AS total_churned_customers,
    COUNT(*) FILTER (WHERE NOT is_churned) AS total_retained_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS overall_churn_rate_pct,
    ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS overall_retention_rate_pct,
    ROUND(SUM(mrr), 2) AS total_monthly_recurring_revenue,
    ROUND(SUM(mrr_at_risk), 2) AS total_mrr_at_risk,
    ROUND((SUM(mrr_at_risk) / SUM(mrr)) * 100, 2) AS mrr_at_risk_pct,
    ROUND(AVG(tenure_months), 2) AS average_tenure_months,
    ROUND(AVG(mrr), 2) AS average_monthly_charges
FROM analytics.vw_customer_churn_clean;

-- Output Executive Summary
SELECT * FROM reporting.vw_executive_kpi_summary;

-- Strategic Action Priority Matrix
SELECT 
    'Priority 1: Month-to-Month Electronic Check Onboarding' AS intervention_initiative,
    COUNT(*) AS target_customers,
    SUM(mrr_at_risk) AS mrr_at_risk_recoverable,
    ROUND((SUM(mrr_at_risk) / (SELECT SUM(mrr_at_risk) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS pct_of_total_mrr_exposure
FROM analytics.vw_customer_churn_clean
WHERE contract_type = 'Month-to-month' 
  AND payment_method = 'Electronic check'
  AND is_churned

UNION ALL

SELECT 
    'Priority 2: Early Tenure (0-6 Months) Fiber Optic Support Interventions' AS intervention_initiative,
    COUNT(*) AS target_customers,
    SUM(mrr_at_risk) AS mrr_at_risk_recoverable,
    ROUND((SUM(mrr_at_risk) / (SELECT SUM(mrr_at_risk) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS pct_of_total_mrr_exposure
FROM analytics.vw_customer_churn_clean
WHERE tenure_months <= 6 
  AND internet_service = 'Fiber optic'
  AND is_churned

UNION ALL

SELECT 
    'Priority 3: Annual Contract Incentive Conversion for Month-to-Month Base' AS intervention_initiative,
    COUNT(*) AS target_customers,
    SUM(mrr) AS mrr_at_risk_recoverable,
    ROUND((SUM(mrr) / (SELECT SUM(mrr) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS pct_of_total_mrr_exposure
FROM analytics.vw_customer_churn_clean
WHERE contract_type = 'Month-to-month' 
  AND NOT is_churned;
