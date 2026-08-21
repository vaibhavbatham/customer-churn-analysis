-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 08_retention_analysis.sql
-- Description: Retention curves, milestone survival analysis, and tenure cohort dynamics.
-- ============================================================================

-- 1. Churn and Retention Rates Across Discrete Tenure Bands
SELECT 
    tenure_band,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE NOT is_churned) AS retained_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct,
    ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS retention_rate_pct,
    SUM(mrr) AS total_band_mrr,
    SUM(mrr_at_risk) AS mrr_at_risk,
    ROUND((SUM(mrr_at_risk) / SUM(mrr)) * 100, 2) AS mrr_risk_pct_within_band
FROM analytics.vw_customer_churn_clean
GROUP BY tenure_band, tenure_band_order
ORDER BY tenure_band_order;

-- 2. Milestone Survival & Retention Analysis (Cumulative Milestone Reach)
WITH milestone_definitions AS (
    SELECT 1 AS milestone_month, '1 Month' AS milestone_label UNION ALL
    SELECT 3, '3 Months' UNION ALL
    SELECT 6, '6 Months' UNION ALL
    SELECT 12, '12 Months (1 Year)' UNION ALL
    SELECT 24, '24 Months (2 Years)' UNION ALL
    SELECT 36, '36 Months (3 Years)' UNION ALL
    SELECT 48, '48 Months (4 Years)' UNION ALL
    SELECT 60, '60 Months (5 Years)' UNION ALL
    SELECT 72, '72 Months (6 Years)'
),
total_pop AS (
    SELECT COUNT(*) AS total_pop_count FROM analytics.vw_customer_churn_clean
)
SELECT 
    m.milestone_label,
    m.milestone_month,
    COUNT(c.customer_id) AS customers_reached_milestone,
    ROUND((COUNT(c.customer_id)::NUMERIC / t.total_pop_count) * 100, 2) AS pct_total_population_reached,
    COUNT(c.customer_id) FILTER (WHERE NOT c.is_churned) AS active_retained_customers,
    COUNT(c.customer_id) FILTER (WHERE c.is_churned) AS churned_customers,
    ROUND(
        (COUNT(c.customer_id) FILTER (WHERE NOT c.is_churned)::NUMERIC / NULLIF(COUNT(c.customer_id), 0)) * 100, 
        2
    ) AS cohort_retention_rate_pct
FROM milestone_definitions m
CROSS JOIN total_pop t
LEFT JOIN analytics.vw_customer_churn_clean c
    ON c.tenure_months >= m.milestone_month
GROUP BY m.milestone_label, m.milestone_month, t.total_pop_count
ORDER BY m.milestone_month;

-- 3. Specific Hypothesis Validation: Early Tenure (0-6M) vs Mature Tenure (5+ Years / 60M+)
SELECT 
    '0-6 Months Early Tenure' AS tenure_cohort,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE NOT is_churned) AS retained_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS retention_rate_pct,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct
FROM analytics.vw_customer_churn_clean
WHERE tenure_months <= 6

UNION ALL

SELECT 
    '60+ Months (5 Years+) Mature Cohort' AS tenure_cohort,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE NOT is_churned) AS retained_customers,
    COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
    ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS retention_rate_pct,
    ROUND((COUNT(*) FILTER (WHERE is_churned)::NUMERIC / COUNT(*)) * 100, 2) AS churn_rate_pct
FROM analytics.vw_customer_churn_clean
WHERE tenure_months >= 60;
