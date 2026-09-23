import os
import duckdb
import pandas as pd

def run_sql_pipeline(base_dir):
    print("======================================================================")
    print("EXECUTING POSTGRESQL ANALYTICAL DATABASE PIPELINE")
    print("======================================================================")
    
    raw_csv = os.path.join(base_dir, 'data', 'raw', 'customer_churn_raw.csv').replace('\\', '/')
    sql_outputs_dir = os.path.join(base_dir, 'reports', 'sql_query_outputs')
    os.makedirs(sql_outputs_dir, exist_ok=True)
    
    # Initialize DuckDB engine (PostgreSQL dialect compliant)
    con = duckdb.connect(':memory:')
    
    # 1. Schemas
    print("\n[1/6] Creating Database Schemas (staging, analytics, reporting)...")
    con.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    con.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
    con.execute("CREATE SCHEMA IF NOT EXISTS reporting;")
    print("      -> Schemas created successfully.")
    
    # 2. DDL Tables
    print("\n[2/6] Executing DDL Table Definitions & Constraints...")
    con.execute("""
    CREATE TABLE staging.stg_customer_churn (
        customer_id         VARCHAR,
        gender              VARCHAR,
        senior_citizen      INTEGER,
        partner             VARCHAR,
        dependents          VARCHAR,
        tenure              INTEGER,
        phone_service       VARCHAR,
        multiple_lines      VARCHAR,
        internet_service    VARCHAR,
        online_security     VARCHAR,
        online_backup       VARCHAR,
        device_protection   VARCHAR,
        tech_support        VARCHAR,
        streaming_tv        VARCHAR,
        streaming_movies    VARCHAR,
        contract            VARCHAR,
        paperless_billing   VARCHAR,
        payment_method      VARCHAR,
        monthly_charges     DOUBLE,
        total_charges       VARCHAR,
        churn               VARCHAR
    );
    """)
    
    con.execute("""
    CREATE TABLE analytics.dim_customers (
        customer_id         VARCHAR PRIMARY KEY,
        gender              VARCHAR NOT NULL,
        senior_citizen      BOOLEAN NOT NULL,
        has_partner         BOOLEAN NOT NULL,
        has_dependents      BOOLEAN NOT NULL,
        tenure_months       INTEGER NOT NULL CHECK (tenure_months >= 0),
        phone_service       VARCHAR NOT NULL,
        multiple_lines      VARCHAR NOT NULL,
        internet_service    VARCHAR NOT NULL,
        online_security     VARCHAR NOT NULL,
        online_backup       VARCHAR NOT NULL,
        device_protection   VARCHAR NOT NULL,
        tech_support        VARCHAR NOT NULL,
        streaming_tv        VARCHAR NOT NULL,
        streaming_movies    VARCHAR NOT NULL,
        contract_type       VARCHAR NOT NULL,
        paperless_billing   BOOLEAN NOT NULL,
        payment_method      VARCHAR NOT NULL,
        monthly_charges     DOUBLE NOT NULL CHECK (monthly_charges >= 0),
        total_charges       DOUBLE NOT NULL CHECK (total_charges >= 0),
        churn_status        VARCHAR NOT NULL CHECK (churn_status IN ('Yes', 'No')),
        is_churned          BOOLEAN NOT NULL
    );
    """)
    print("      -> Tables created: staging.stg_customer_churn, analytics.dim_customers.")
    
    # 3. Bulk Ingestion (COPY)
    print(f"\n[3/6] Bulk Ingesting Census Data via COPY from {raw_csv}...")
    con.execute(f"""
    COPY staging.stg_customer_churn FROM '{raw_csv}' (HEADER TRUE, DELIMITER ',');
    """)
    staging_count = con.execute("SELECT COUNT(*) FROM staging.stg_customer_churn;").fetchone()[0]
    print(f"      -> Ingested {staging_count:,} rows into staging.stg_customer_churn.")
    assert staging_count == 7043, f"Expected 7,043 rows, got {staging_count}"
    
    # 4. Data Quality & Imputation into Analytics Layer
    print("\n[4/6] Applying Business-Rule Imputation & Populating Analytics Model...")
    con.execute("""
    INSERT INTO analytics.dim_customers (
        customer_id, gender, senior_citizen, has_partner, has_dependents,
        tenure_months, phone_service, multiple_lines, internet_service,
        online_security, online_backup, device_protection, tech_support,
        streaming_tv, streaming_movies, contract_type, paperless_billing,
        payment_method, monthly_charges, total_charges, churn_status, is_churned
    )
    SELECT 
        TRIM(customer_id) AS customer_id,
        gender,
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
        -- Business-rule imputation: impute 0.00 for month-0 unbilled subscribers
        COALESCE(NULLIF(TRIM(total_charges), '')::DOUBLE, 0.00) AS total_charges,
        churn AS churn_status,
        CASE WHEN churn = 'Yes' THEN TRUE ELSE FALSE END AS is_churned
    FROM staging.stg_customer_churn;
    """)
    analytics_count = con.execute("SELECT COUNT(*) FROM analytics.dim_customers;").fetchone()[0]
    print(f"      -> Populated {analytics_count:,} clean records into analytics.dim_customers.")
    assert analytics_count == 7043, f"Expected 7,043 records, got {analytics_count}"
    
    # 5. Create Analytical View & Reporting Views
    print("\n[5/6] Creating Clean Analytical View & Executive Reporting Views...")
    con.execute("""
    CREATE OR REPLACE VIEW analytics.vw_customer_churn_clean AS
    SELECT 
        customer_id, gender, senior_citizen, has_partner, has_dependents,
        tenure_months,
        CASE 
            WHEN tenure_months <= 6 THEN '0-6 Months'
            WHEN tenure_months <= 12 THEN '7-12 Months'
            WHEN tenure_months <= 24 THEN '13-24 Months'
            WHEN tenure_months <= 36 THEN '25-36 Months'
            WHEN tenure_months <= 48 THEN '37-48 Months'
            WHEN tenure_months <= 60 THEN '49-60 Months'
            ELSE '60+ Months'
        END AS tenure_band,
        phone_service, multiple_lines, internet_service,
        online_security, online_backup, device_protection, tech_support,
        streaming_tv, streaming_movies, contract_type, paperless_billing,
        payment_method,
        monthly_charges AS mrr,
        total_charges,
        churn_status,
        is_churned,
        CASE WHEN is_churned THEN 'Churned' ELSE 'Retained' END AS customer_status,
        CASE WHEN is_churned THEN monthly_charges ELSE 0.00 END AS mrr_at_risk,
        CASE 
            WHEN monthly_charges < 35.00 THEN 'Low (<$35)'
            WHEN monthly_charges <= 75.00 THEN 'Medium ($35-$75)'
            ELSE 'High (>$75)'
        END AS mrr_tier,
        CASE 
            WHEN contract_type = 'Month-to-month' THEN 'High Risk'
            WHEN contract_type = 'One year' THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS churn_risk_tier
    FROM analytics.dim_customers;
    """)
    
    con.execute("""
    CREATE OR REPLACE VIEW reporting.vw_executive_kpi_summary AS
    SELECT 
        COUNT(*) AS total_customer_population,
        COUNT(*) FILTER (WHERE is_churned) AS total_churned_customers,
        COUNT(*) FILTER (WHERE NOT is_churned) AS total_retained_customers,
        ROUND((COUNT(*) FILTER (WHERE is_churned)::DOUBLE / COUNT(*)) * 100, 2) AS overall_churn_rate_pct,
        ROUND((COUNT(*) FILTER (WHERE NOT is_churned)::DOUBLE / COUNT(*)) * 100, 2) AS overall_retention_rate_pct,
        ROUND(SUM(mrr), 2) AS total_monthly_recurring_revenue,
        ROUND(SUM(mrr_at_risk), 2) AS total_mrr_at_risk,
        ROUND((SUM(mrr_at_risk) / SUM(mrr)) * 100, 2) AS mrr_at_risk_pct,
        ROUND(AVG(tenure_months), 2) AS average_tenure_months,
        ROUND(AVG(mrr), 2) AS average_monthly_charges
    FROM analytics.vw_customer_churn_clean;
    """)
    print("      -> Views created: analytics.vw_customer_churn_clean, reporting.vw_executive_kpi_summary.")
    
    # 6. Advanced SQL Analytics Queries & Exports
    print("\n[6/6] Executing Advanced SQL Queries (CTEs, Window Functions, Ranking, Pareto)...")
    
    # Query A: Executive KPI Summary
    df_kpi = con.execute("SELECT * FROM reporting.vw_executive_kpi_summary;").df()
    df_kpi.to_csv(os.path.join(sql_outputs_dir, "01_executive_kpi_summary.csv"), index=False)
    print("      -> Query 1 (Executive KPIs) Executed & Exported.")
    
    # Query B: Contract Churn & MRR Pareto
    q_contract = """
    WITH contract_summary AS (
        SELECT 
            contract_type,
            COUNT(*) AS total_customers,
            COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
            ROUND((COUNT(*) FILTER (WHERE is_churned)::DOUBLE / COUNT(*)) * 100, 2) AS churn_rate_pct,
            ROUND(SUM(mrr), 2) AS total_mrr,
            ROUND(SUM(mrr_at_risk), 2) AS mrr_at_risk
        FROM analytics.vw_customer_churn_clean
        GROUP BY contract_type
    )
    SELECT 
        contract_type,
        total_customers,
        churned_customers,
        churn_rate_pct,
        total_mrr,
        mrr_at_risk,
        ROUND((mrr_at_risk / SUM(mrr_at_risk) OVER ()) * 100, 2) AS pct_of_total_mrr_lost,
        SUM(mrr_at_risk) OVER (ORDER BY mrr_at_risk DESC) AS cumulative_mrr_lost,
        DENSE_RANK() OVER (ORDER BY mrr_at_risk DESC) AS risk_rank
    FROM contract_summary
    ORDER BY mrr_at_risk DESC;
    """
    df_contract = con.execute(q_contract).df()
    df_contract.to_csv(os.path.join(sql_outputs_dir, "02_contract_churn_pareto.csv"), index=False)
    print("      -> Query 2 (Contract Churn & Pareto Loss) Executed & Exported.")
    
    # Query C: Milestone Retention Curve
    q_retention = """
    WITH milestone_prep AS (
        SELECT 
            unnest([1, 3, 6, 12, 24, 36, 48, 60, 72]) AS milestone_months
    )
    SELECT 
        m.milestone_months,
        COUNT(c.customer_id) AS customers_reached,
        COUNT(c.customer_id) FILTER (WHERE NOT c.is_churned) AS customers_retained,
        ROUND((COUNT(c.customer_id) FILTER (WHERE NOT c.is_churned)::DOUBLE / COUNT(c.customer_id)) * 100, 2) AS active_retention_rate_pct,
        ROUND((COUNT(c.customer_id) FILTER (WHERE c.is_churned)::DOUBLE / COUNT(c.customer_id)) * 100, 2) AS attrition_rate_pct
    FROM milestone_prep m
    JOIN analytics.vw_customer_churn_clean c ON c.tenure_months >= m.milestone_months
    GROUP BY m.milestone_months
    ORDER BY m.milestone_months;
    """
    df_retention = con.execute(q_retention).df()
    df_retention.to_csv(os.path.join(sql_outputs_dir, "03_milestone_retention_curve.csv"), index=False)
    print("      -> Query 3 (Milestone Retention Curve) Executed & Exported.")
    
    # Query D: Pareto Loss by Contract & Payment Method
    q_pareto = """
    WITH segment_revenue AS (
        SELECT 
            contract_type,
            payment_method,
            COUNT(*) AS total_customers,
            COUNT(*) FILTER (WHERE is_churned) AS churned_customers,
            ROUND(SUM(mrr_at_risk), 2) AS segment_mrr_lost
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
        ROUND(SUM(segment_mrr_lost) OVER (ORDER BY segment_mrr_lost DESC), 2) AS cumulative_mrr_at_risk,
        ROUND(
            (SUM(segment_mrr_lost) OVER (ORDER BY segment_mrr_lost DESC) / SUM(segment_mrr_lost) OVER ()) * 100, 
            2
        ) AS cumulative_pct_mrr_at_risk,
        RANK() OVER (ORDER BY segment_mrr_lost DESC) AS priority_rank
    FROM segment_revenue
    ORDER BY segment_mrr_lost DESC;
    """
    df_pareto = con.execute(q_pareto).df()
    df_pareto.to_csv(os.path.join(sql_outputs_dir, "04_segment_pareto_ranking.csv"), index=False)
    print("      -> Query 4 (Segment Pareto Ranking) Executed & Exported.")
    
    print("\n======================================================================")
    print("SQL PIPELINE EXECUTION SUMMARY & VERIFICATION")
    print("======================================================================")
    print(f"Total Population Ingested:  {df_kpi['total_customer_population'].iloc[0]:,} customers")
    print(f"Total Churned Customers:   {df_kpi['total_churned_customers'].iloc[0]:,} customers ({df_kpi['overall_churn_rate_pct'].iloc[0]:.2f}%)")
    print(f"Total Retained Customers:  {df_kpi['total_retained_customers'].iloc[0]:,} customers ({df_kpi['overall_retention_rate_pct'].iloc[0]:.2f}%)")
    print(f"Total Company MRR:         ${df_kpi['total_monthly_recurring_revenue'].iloc[0]:,.2f}")
    print(f"MRR at Risk (Lost):        ${df_kpi['total_mrr_at_risk'].iloc[0]:,.2f} ({df_kpi['mrr_at_risk_pct'].iloc[0]:.2f}%)")
    print("======================================================================")
    print("[SUCCESS] All SQL scripts, tables, views, CTEs, and window queries executed with 0 errors!")
    
    return con

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_sql_pipeline(base_dir)
