-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 06_customer_segmentation.sql
-- Description: Multi-dimensional customer segmentation & risk matrix analysis.
-- ============================================================================

-- 1. Customer Segmentation by Contract Type & Tenure Band Matrix
WITH customer_matrix AS (
    SELECT 
        contract_type,
        tenure_band,
        tenure_band_order,
        COUNT(*) AS total_customers,
        COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
        SUM(mrr) AS total_mrr,
        SUM(mrr_at_risk) AS mrr_at_risk
    FROM analytics.vw_customer_churn_clean
    GROUP BY contract_type, tenure_band, tenure_band_order
)
SELECT 
    contract_type,
    tenure_band,
    total_customers,
    churned_customers,
    ROUND((churned_customers::NUMERIC / total_customers) * 100, 2) AS churn_rate_pct,
    total_mrr,
    mrr_at_risk,
    ROUND((mrr_at_risk / total_mrr) * 100, 2) AS mrr_at_risk_pct,
    RANK() OVER (ORDER BY mrr_at_risk DESC) AS rank_by_mrr_risk
FROM customer_matrix
ORDER BY mrr_at_risk DESC;

-- 2. 2x2 Risk-Value Matrix (Churn Risk vs MRR Value)
WITH segment_aggregation AS (
    SELECT 
        CASE 
            WHEN churn_risk_tier = 'High Risk' AND mrr_tier = 'High (>)' THEN 'Tier 1: Critical (High Churn & High MRR)'
            WHEN churn_risk_tier = 'High Risk' THEN 'Tier 2: High Churn / Low-Med MRR'
            WHEN mrr_tier = 'High (>)' THEN 'Tier 3: High MRR / Med-Low Churn'
            ELSE 'Tier 4: Stable Base (Low Risk & Low-Med MRR)'
        END AS strategic_segment,
        COUNT(*) AS customer_count,
        COUNT(*) FILTER (WHERE is_churned) AS churned_count,
        SUM(mrr) AS segment_mrr,
        SUM(mrr_at_risk) AS segment_mrr_at_risk
    FROM analytics.vw_customer_churn_clean
    GROUP BY 1
)
SELECT 
    strategic_segment,
    customer_count,
    ROUND((customer_count::NUMERIC / (SELECT COUNT(*) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS customer_share_pct,
    churned_count,
    ROUND((churned_count::NUMERIC / customer_count) * 100, 2) AS segment_churn_rate_pct,
    segment_mrr,
    segment_mrr_at_risk,
    ROUND((segment_mrr_at_risk / (SELECT SUM(mrr_at_risk) FROM analytics.vw_customer_churn_clean)) * 100, 2) AS pct_of_total_mrr_risk
FROM segment_aggregation
ORDER BY segment_mrr_at_risk DESC;
