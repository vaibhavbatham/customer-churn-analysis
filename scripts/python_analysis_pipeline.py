import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_python_pipeline(base_dir):
    print("======================================================================")
    print("EXECUTING PYTHON STATISTICAL & VISUAL ANALYTICS PIPELINE")
    print("======================================================================")
    
    clean_csv = os.path.join(base_dir, 'data', 'processed', 'customer_churn_clean.csv')
    screenshots_dir = os.path.join(base_dir, 'screenshots')
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    df = pd.read_csv(clean_csv)
    print(f"Loaded {len(df):,} cleaned records from {clean_csv}")
    
    # Configure plotting style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    sns.set_palette(['#3b82f6', '#ef4444', '#10b981', '#f59e0b'])
    
    # ------------------------------------------------------------------
    # 1. Monthly Charges KDE Distribution: Retained vs Churned
    # ------------------------------------------------------------------
    print("\n[1/4] Generating Monthly Charges KDE Distribution...")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.kdeplot(data=df[df['customer_status'] == 'Retained']['MonthlyCharges'], 
                label='Retained Subscribers (n=5,174, Mean: $61.27)', 
                color='#10b981', fill=True, alpha=0.3, linewidth=2, ax=ax)
    sns.kdeplot(data=df[df['customer_status'] == 'Churned']['MonthlyCharges'], 
                label='Churned Subscribers (n=1,869, Mean: $74.44)', 
                color='#ef4444', fill=True, alpha=0.4, linewidth=2, ax=ax)
    ax.set_title('Monthly Recurring Charge Distribution: Retained vs. Churned Customers', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Probability Density', fontsize=11, fontweight='semibold')
    ax.axvline(df[df['customer_status'] == 'Retained']['MonthlyCharges'].median(), color='#059669', linestyle='--', alpha=0.7, label='Retained Median ($64.43)')
    ax.axvline(df[df['customer_status'] == 'Churned']['MonthlyCharges'].median(), color='#dc2626', linestyle='--', alpha=0.7, label='Churned Median ($79.65)')
    ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=10)
    plt.tight_layout()
    fig_path1 = os.path.join(screenshots_dir, 'statistical_kde_charges_distribution.png')
    fig.savefig(fig_path1)
    plt.close(fig)
    print(f"      -> Saved {fig_path1}")
    
    # ------------------------------------------------------------------
    # 2. Milestone Retention Curve (1M to 72M)
    # ------------------------------------------------------------------
    print("\n[2/4] Generating Milestone Retention Curve...")
    ret_df = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'retention_curve_data.csv'))
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(ret_df['milestone_months'], ret_df['active_retention_rate_pct'], 
            marker='o', markersize=8, color='#2563eb', linewidth=2.5, label='Active Retention Rate (%)')
    ax.fill_between(ret_df['milestone_months'], ret_df['active_retention_rate_pct'], 60, color='#3b82f6', alpha=0.15)
    
    # Annotate Key Milestones
    ax.annotate('Month 1: 73.4%\n(Immediate Drop)', xy=(1, 73.42), xytext=(5, 68),
                arrowprops=dict(facecolor='#ef4444', shrink=0.08, width=1.5, headwidth=6),
                fontweight='bold', fontsize=9, color='#dc2626')
    ax.annotate('Month 12: 82.5%\n(Inflection Point)', xy=(12, 82.51), xytext=(16, 76),
                arrowprops=dict(facecolor='#f59e0b', shrink=0.08, width=1.5, headwidth=6),
                fontweight='bold', fontsize=9, color='#d97706')
    ax.annotate('Month 60+: 93.3%\n(Loyalty Plateau)', xy=(60, 93.32), xytext=(48, 96),
                arrowprops=dict(facecolor='#10b981', shrink=0.08, width=1.5, headwidth=6),
                fontweight='bold', fontsize=9, color='#059669')
                
    ax.set_ylim(60, 102)
    ax.set_title('Customer Milestone Retention Curve Across 72-Month Horizon', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Tenure Horizon (Months Reached)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Active Retention Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xticks(ret_df['milestone_months'])
    ax.legend(loc='lower right', frameon=True, facecolor='#ffffff')
    plt.tight_layout()
    fig_path2 = os.path.join(screenshots_dir, 'statistical_milestone_retention_curve.png')
    fig.savefig(fig_path2)
    plt.close(fig)
    print(f"      -> Saved {fig_path2}")
    
    # ------------------------------------------------------------------
    # 3. Cumulative Pareto Revenue Loss Distribution
    # ------------------------------------------------------------------
    print("\n[3/4] Generating Pareto Cumulative Revenue Loss Curve...")
    churned_df = df[df['is_churned']].sort_values(by='MonthlyCharges', ascending=False).copy()
    churned_df['cum_mrr'] = churned_df['MonthlyCharges'].cumsum()
    churned_df['cum_pct'] = (churned_df['cum_mrr'] / churned_df['MonthlyCharges'].sum()) * 100
    churned_df['customer_pct'] = np.linspace(0, 100, len(churned_df))
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(churned_df['customer_pct'], churned_df['cum_pct'], color='#e11d48', linewidth=2.5, label='Actual MRR Loss Concentration')
    ax.plot([0, 100], [0, 100], color='#94a3b8', linestyle='--', label='Equal Loss Distribution (Baseline)')
    
    # Highlight 20/80 Pareto point
    p20_val = np.interp(20, churned_df['customer_pct'], churned_df['cum_pct'])
    ax.plot([20, 20], [0, p20_val], color='#f59e0b', linestyle=':')
    ax.plot([0, 20], [p20_val, p20_val], color='#f59e0b', linestyle=':')
    ax.plot(20, p20_val, 'o', color='#f59e0b', markersize=8)
    ax.annotate(f'Top 20% Churned = {p20_val:.1f}% Lost MRR', xy=(20, p20_val), xytext=(28, p20_val - 5),
                fontweight='bold', fontsize=9, color='#b45309')
                
    ax.set_title('Pareto Distribution of Monthly Recurring Revenue (MRR) Lost to Churn', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Cumulative % of Churned Customers', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Cumulative % of Lost MRR ($)', fontsize=11, fontweight='semibold')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 102)
    ax.legend(loc='lower right', frameon=True, facecolor='#ffffff')
    plt.tight_layout()
    fig_path3 = os.path.join(screenshots_dir, 'statistical_pareto_revenue_loss.png')
    fig.savefig(fig_path3)
    plt.close(fig)
    print(f"      -> Saved {fig_path3}")
    
    # ------------------------------------------------------------------
    # 4. Contract x Tenure Risk Interaction Heatmap
    # ------------------------------------------------------------------
    print("\n[4/4] Generating Contract x Tenure Churn Heatmap...")
    order_bands = ['0-6 Months', '7-12 Months', '13-24 Months', '25-36 Months', '37-48 Months', '49-60 Months', '60+ Months']
    order_contracts = ['Month-to-month', 'One year', 'Two year']
    pivot_heat = df.pivot_table(index='Contract', columns='tenure_band', values='is_churned', aggfunc='mean') * 100
    pivot_heat = pivot_heat.reindex(index=order_contracts, columns=order_bands)
    
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    sns.heatmap(pivot_heat, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Churn Rate (%)'}, ax=ax, linewidths=0.5)
    ax.set_title('Churn Rate Heatmap: Contract Type vs. Tenure Lifecycle Band (%)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Tenure Lifecycle Band', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Contract Type', fontsize=11, fontweight='semibold')
    plt.tight_layout()
    fig_path4 = os.path.join(screenshots_dir, 'statistical_contract_tenure_heatmap.png')
    fig.savefig(fig_path4)
    plt.close(fig)
    print(f"      -> Saved {fig_path4}")
    
    print("\n======================================================================")
    print("[SUCCESS] Python Statistical & Visualization Pipeline Completed!")
    print("======================================================================")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_python_pipeline(base_dir)
