import os
import pandas as pd
import numpy as np

def run_cleaning_and_imputation(raw_path, output_dir):
    print("----------------------------------------------------------------------")
    print("STEP 1: Ingesting Raw Census Dataset")
    print("----------------------------------------------------------------------")
    df = pd.read_csv(raw_path)
    total_raw = len(df)
    print(f"Total Census Records Ingested: {total_raw:,} records")
    assert total_raw == 7043, f"Expected 7,043 records, got {total_raw}"

    print("\n----------------------------------------------------------------------")
    print("STEP 2: Business-Rule-Based Imputation Audit for TotalCharges")
    print("----------------------------------------------------------------------")
    # Identify whitespace or blank TotalCharges
    mask_blank = (df['TotalCharges'].astype(str).str.strip() == '') | (df['TotalCharges'].isnull())
    blank_count = mask_blank.sum()
    print(f"Detected {blank_count} records with blank/whitespace TotalCharges.")
    
    # Audit these records
    blank_records = df[mask_blank][['customerID', 'tenure', 'MonthlyCharges', 'Contract', 'Churn']]
    print(blank_records.to_string(index=False))
    
    # Validate business rationale:
    # 100% of these records have tenure == 0 and Churn == 'No'
    assert (df.loc[mask_blank, 'tenure'] == 0).all(), "Error: Not all blank TotalCharges have tenure = 0!"
    assert (df.loc[mask_blank, 'Churn'] == 'No').all(), "Error: Blank TotalCharges accounts should be active unbilled subscribers!"
    print("\n[VALIDATION PASSED] Business Rationale Confirmed:")
    print("  -> All 11 records are brand new month-0 subscribers who joined during the current billing cycle.")
    print("  -> No prior invoice has been finalized, so accrued historical billing is exactly $0.00.")
    print("  -> Imputing 0.00 maintains 100% census integrity without dropping rows or introducing statistical bias.")

    # Apply Business Rule Imputation
    df['TotalCharges_Clean'] = pd.to_numeric(df['TotalCharges'].astype(str).str.strip().replace('', '0.00'), errors='coerce')
    assert df['TotalCharges_Clean'].isnull().sum() == 0, "Error: Unexpected NaN after cleaning TotalCharges"

    print("\n----------------------------------------------------------------------")
    print("STEP 3: Analytical Feature Engineering")
    print("----------------------------------------------------------------------")
    # Customer status & is_churned
    df['customer_status'] = df['Churn'].map({'Yes': 'Churned', 'No': 'Retained'})
    df['is_churned'] = df['Churn'] == 'Yes'

    # Tenure Bands
    def get_tenure_band(t):
        if t <= 6: return '0-6 Months'
        elif t <= 12: return '7-12 Months'
        elif t <= 24: return '13-24 Months'
        elif t <= 36: return '25-36 Months'
        elif t <= 48: return '37-48 Months'
        elif t <= 60: return '49-60 Months'
        else: return '60+ Months'

    df['tenure_band'] = df['tenure'].apply(get_tenure_band)

    # Monthly Recurring Revenue (MRR) at risk
    df['mrr_at_risk'] = np.where(df['is_churned'], df['MonthlyCharges'], 0.0)

    # MRR Tier
    def get_mrr_tier(mc):
        if mc < 35.0: return 'Low (<$35)'
        elif mc <= 75.0: return 'Medium ($35-$75)'
        else: return 'High (>$75)'

    df['mrr_tier'] = df['MonthlyCharges'].apply(get_mrr_tier)

    # Churn Risk Tier by Contract
    def get_churn_risk_tier(c):
        if c == 'Month-to-month': return 'High Risk'
        elif c == 'One year': return 'Medium Risk'
        else: return 'Low Risk'

    df['churn_risk_tier'] = df['Contract'].apply(get_churn_risk_tier)

    # 2x2 Strategic Risk Segment Matrix
    def get_risk_segment(row):
        is_high_risk = row['Contract'] == 'Month-to-month'
        is_high_mrr = row['MonthlyCharges'] >= 65.0
        if is_high_risk and is_high_mrr:
            return 'Tier 1: Critical (High Churn & High MRR)'
        elif is_high_risk and not is_high_mrr:
            return 'Tier 2: High Churn / Low-Med MRR'
        elif not is_high_risk and is_high_mrr:
            return 'Tier 3: High MRR / Med-Low Churn'
        else:
            return 'Tier 4: Stable Base (Low Risk & Low-Med MRR)'

    df['risk_segment'] = df.apply(get_risk_segment, axis=1)

    print(f"Engineered Features: tenure_band, customer_status, mrr_at_risk, mrr_tier, churn_risk_tier, risk_segment")

    print("\n----------------------------------------------------------------------")
    print("STEP 4: Exporting Processed Analytical Datasets")
    print("----------------------------------------------------------------------")
    os.makedirs(output_dir, exist_ok=True)
    clean_csv_path = os.path.join(output_dir, 'customer_churn_clean.csv')
    df.to_csv(clean_csv_path, index=False)
    print(f"Exported primary clean dataset: {clean_csv_path} ({len(df):,} rows)")

    # Contract summary
    c_grp = df.groupby('Contract').agg(
        total_customers=('customerID', 'count'),
        churned_customers=('is_churned', 'sum'),
        total_mrr=('MonthlyCharges', 'sum'),
        mrr_at_risk=('mrr_at_risk', 'sum')
    ).reset_index()
    c_grp['retained_customers'] = c_grp['total_customers'] - c_grp['churned_customers']
    c_grp['churn_rate_pct'] = (c_grp['churned_customers'] / c_grp['total_customers'] * 100).round(2)
    c_grp['retention_rate_pct'] = (100.0 - c_grp['churn_rate_pct']).round(2)
    c_grp['mrr_risk_pct'] = (c_grp['mrr_at_risk'] / c_grp['total_mrr'] * 100).round(2)
    c_grp['pct_of_total_mrr_lost'] = (c_grp['mrr_at_risk'] / df['mrr_at_risk'].sum() * 100).round(2)
    c_grp.to_csv(os.path.join(output_dir, 'churn_by_contract.csv'), index=False)
    print("Exported churn_by_contract.csv")

    # Tenure band summary
    order_bands = ['0-6 Months', '7-12 Months', '13-24 Months', '25-36 Months', '37-48 Months', '49-60 Months', '60+ Months']
    t_grp = df.groupby('tenure_band').agg(
        total_customers=('customerID', 'count'),
        churned_customers=('is_churned', 'sum'),
        total_mrr=('MonthlyCharges', 'sum'),
        mrr_at_risk=('mrr_at_risk', 'sum')
    ).reindex(order_bands).reset_index()
    t_grp['retained_customers'] = t_grp['total_customers'] - t_grp['churned_customers']
    t_grp['churn_rate_pct'] = (t_grp['churned_customers'] / t_grp['total_customers'] * 100).round(2)
    t_grp['retention_rate_pct'] = (100.0 - t_grp['churn_rate_pct']).round(2)
    t_grp['mrr_risk_pct'] = (t_grp['mrr_at_risk'] / t_grp['total_mrr'] * 100).round(2)
    t_grp.to_csv(os.path.join(output_dir, 'churn_by_tenure.csv'), index=False)
    print("Exported churn_by_tenure.csv")

    # Milestone Retention Curve (1, 3, 6, 12, 24, 36, 48, 60, 72 months)
    milestones = [1, 3, 6, 12, 24, 36, 48, 60, 72]
    ret_rows = []
    for m in milestones:
        reached = (df['tenure'] >= m).sum()
        retained = ((df['tenure'] >= m) & (df['customer_status'] == 'Retained')).sum()
        ret_rate = round(retained / reached * 100, 2)
        ret_rows.append({
            'milestone_months': m,
            'customers_reached': reached,
            'customers_retained': retained,
            'active_retention_rate_pct': ret_rate,
            'attrition_rate_pct': round(100.0 - ret_rate, 2)
        })
    df_ret = pd.DataFrame(ret_rows)
    df_ret.to_csv(os.path.join(output_dir, 'retention_curve_data.csv'), index=False)
    print("Exported retention_curve_data.csv")

    # Risk segment summary
    tier_order = [
        'Tier 1: Critical (High Churn & High MRR)',
        'Tier 2: High Churn / Low-Med MRR',
        'Tier 3: High MRR / Med-Low Churn',
        'Tier 4: Stable Base (Low Risk & Low-Med MRR)'
    ]
    r_grp = df.groupby('risk_segment').agg(
        total_customers=('customerID', 'count'),
        churned_customers=('is_churned', 'sum'),
        total_mrr=('MonthlyCharges', 'sum'),
        mrr_at_risk=('mrr_at_risk', 'sum')
    ).reindex(tier_order).reset_index()
    r_grp['customer_share_pct'] = (r_grp['total_customers'] / total_raw * 100).round(2)
    r_grp['churn_rate_pct'] = (r_grp['churned_customers'] / r_grp['total_customers'] * 100).round(2)
    r_grp['pct_of_lost_mrr'] = (r_grp['mrr_at_risk'] / df['mrr_at_risk'].sum() * 100).round(2)
    r_grp.to_csv(os.path.join(output_dir, 'revenue_risk_segments.csv'), index=False)
    print("Exported revenue_risk_segments.csv")

    print("\n[SUCCESS] Pipeline completed successfully!")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, 'data', 'raw', 'customer_churn_raw.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    run_cleaning_and_imputation(raw_csv, processed_dir)
