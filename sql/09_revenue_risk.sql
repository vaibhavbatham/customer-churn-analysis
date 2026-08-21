-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 09_revenue_risk.sql
-- Description: Advanced revenue-at-risk analytics, rankings, and cumulative window functions.
-- ============================================================================

-- 1. High-Value Customer Risk Ranking using DENSE_RANK()
WITH high_risk_accounts AS (
    SELECT 
        customer_id,
        contract_type,
        tenure_months,
        payment_method,
        mrr,
        total_charges,
        churn_status,
        mrr_at_risk
    FROM analytics.vw_customer_churn_clean
    WHERE is_churned
)
SELECT 
    customer_id,
    contract_type,
    tenure_months,
    payment_method,
    mrr,
    DENSE_RANK() OVER (ORDER BY mrr DESC) AS mrr_loss_rank,
    SUM(mrr) OVER (ORDER BY mrr DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_mrr_lost
FROM high_risk_accounts
LIMIT 20;

-- 2. Pareto Revenue Risk Analysis by Contract & Payment Method
WITH segment_revenue AS (
    SELECT 
        contract_type,
        payment_method,
        COUNT(*) AS total_customers,
        COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
        SUM(mrr_at_risk) AS segment_mrr_lost
    FROM analytics.vw_customer_churn_clean
    GROUP BY contract_type, payment_method
)
SELECT 
    contract_type,
    payment_method,
    total_customers,
    churned_customers,
    segment_mrr_lost,
    ROUND((segment_mrr_lost / SUM(segment_mrr_lost) OVER ()) * 100, 2) AS pct_of_total_churned_mrr,
    SUM(segment_mrr_lost) OVER (ORDER BY segment_mrr_lost DESC) AS cumulative_mrr_at_risk,
    ROUND(
        (SUM(segment_mrr_lost) OVER (ORDER BY segment_mrr_lost DESC) / SUM(segment_mrr_lost) OVER ()) * 100, 
        2
    ) AS cumulative_pct_mrr_at_risk,
    RANK() OVER (ORDER BY segment_mrr_lost DESC) AS priority_rank
FROM segment_revenue
ORDER BY segment_mrr_lost DESC;

-- 3. Monthly Recurring Revenue (MRR) Summary by Customer Tier & Status
SELECT 
    mrr_tier,
    customer_status,
    COUNT(*) AS customer_count,
    SUM(mrr) AS total_mrr_in_tier,
    ROUND(AVG(mrr), 2) AS avg_mrr_per_customer,
    ROUND((SUM(mrr) / SUM(SUM(mrr)) OVER ()) * 100, 2) AS pct_of_company_total_mrr
FROM analytics.vw_customer_churn_clean
GROUP BY mrr_tier, customer_status
ORDER BY mrr_tier, customer_status;
