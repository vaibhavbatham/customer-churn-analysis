-- ============================================================================
-- Customer Churn & Revenue Risk Analysis (SaaS / Subscription Business)
-- File: 01_create_database.sql
-- Description: Creates the database, analytical schemas, and setting configurations.
-- ============================================================================

-- Create dedicated analytics schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS reporting;

-- Comment on schemas
COMMENT ON SCHEMA staging IS 'Staging layer for raw ingestion and data audit';
COMMENT ON SCHEMA analytics IS 'Production analytical models, cleaned tables, and derived views';
COMMENT ON SCHEMA reporting IS 'Executive reporting views and aggregated KPI summaries';
