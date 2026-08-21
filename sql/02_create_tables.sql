-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 02_create_tables.sql
-- Description: DDL table definitions for staging and production tables.
-- ============================================================================

-- Drop staging table if exists
DROP TABLE IF EXISTS staging.stg_customer_churn;

-- Create raw staging table matching CSV structure
CREATE TABLE staging.stg_customer_churn (
    customer_id         VARCHAR(50),
    gender              VARCHAR(20),
    senior_citizen      INTEGER,
    partner             VARCHAR(10),
    dependents          VARCHAR(10),
    tenure              INTEGER,
    phone_service       VARCHAR(10),
    multiple_lines      VARCHAR(30),
    internet_service    VARCHAR(30),
    online_security     VARCHAR(30),
    online_backup       VARCHAR(30),
    device_protection   VARCHAR(30),
    tech_support        VARCHAR(30),
    streaming_tv        VARCHAR(30),
    streaming_movies    VARCHAR(30),
    contract            VARCHAR(30),
    paperless_billing   VARCHAR(10),
    payment_method      VARCHAR(50),
    monthly_charges     NUMERIC(10, 2),
    total_charges       VARCHAR(50), -- Stored as VARCHAR initially to capture whitespace/missing values
    churn               VARCHAR(10)
);

-- Drop analytics table if exists
DROP TABLE IF EXISTS analytics.dim_customers;

-- Create production analytics customer table with proper constraints
CREATE TABLE analytics.dim_customers (
    customer_id         VARCHAR(50) PRIMARY KEY,
    gender              VARCHAR(20) NOT NULL,
    senior_citizen      BOOLEAN NOT NULL,
    has_partner         BOOLEAN NOT NULL,
    has_dependents      BOOLEAN NOT NULL,
    tenure_months       INTEGER NOT NULL CHECK (tenure_months >= 0),
    phone_service       VARCHAR(10) NOT NULL,
    multiple_lines      VARCHAR(30) NOT NULL,
    internet_service    VARCHAR(30) NOT NULL,
    online_security     VARCHAR(30) NOT NULL,
    online_backup       VARCHAR(30) NOT NULL,
    device_protection   VARCHAR(30) NOT NULL,
    tech_support        VARCHAR(30) NOT NULL,
    streaming_tv        VARCHAR(30) NOT NULL,
    streaming_movies    VARCHAR(30) NOT NULL,
    contract_type       VARCHAR(30) NOT NULL,
    paperless_billing   BOOLEAN NOT NULL,
    payment_method      VARCHAR(50) NOT NULL,
    monthly_charges     NUMERIC(10, 2) NOT NULL CHECK (monthly_charges >= 0),
    total_charges       NUMERIC(12, 2) NOT NULL CHECK (total_charges >= 0),
    churn_status        VARCHAR(10) NOT NULL CHECK (churn_status IN ('Yes', 'No')),
    is_churned          BOOLEAN NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_contract ON analytics.dim_customers(contract_type);
CREATE INDEX idx_customers_tenure ON analytics.dim_customers(tenure_months);
CREATE INDEX idx_customers_churn ON analytics.dim_customers(churn_status);
