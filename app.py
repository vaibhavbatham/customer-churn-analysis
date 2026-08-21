import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os

# Page configuration
st.set_page_config(
    page_title="Customer Churn & Revenue Risk Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for executive dark/light dashboard theme
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .metric-alert {
        color: #ef4444 !important;
    }
    .metric-success {
        color: #10b981 !important;
    }
    .metric-primary {
        color: #2563eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "processed", "customer_churn_clean.csv")
    if not os.path.exists(csv_path):
        csv_path = "data/processed/customer_churn_clean.csv"
    df = pd.read_csv(csv_path)
    return df

df = load_data()

# Sidebar Navigation & Filters
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Navigation & Filters")
app_mode = st.sidebar.radio(
    "Select Dashboard View",
    ["Executive Overview", "Churn Drivers & Diagnostics", "Revenue Risk & Matrix", "What-If Simulator", "SQL & Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Interactive Segment Filters")

selected_contracts = st.sidebar.multiselect(
    "Contract Type",
    options=df["Contract"].unique().tolist(),
    default=df["Contract"].unique().tolist()
)

selected_tenures = st.sidebar.multiselect(
    "Tenure Band",
    options=["0-6 Months", "7-12 Months", "13-24 Months", "25-36 Months", "37-48 Months", "49-60 Months", "60+ Months"],
    default=["0-6 Months", "7-12 Months", "13-24 Months", "25-36 Months", "37-48 Months", "49-60 Months", "60+ Months"]
)

selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=df["PaymentMethod"].unique().tolist(),
    default=df["PaymentMethod"].unique().tolist()
)

selected_internet = st.sidebar.multiselect(
    "Internet Service",
    options=df["InternetService"].unique().tolist(),
    default=df["InternetService"].unique().tolist()
)

# Apply filters
filtered_df = df[
    (df["Contract"].isin(selected_contracts)) &
    (df["tenure_band"].isin(selected_tenures)) &
    (df["PaymentMethod"].isin(selected_payments)) &
    (df["InternetService"].isin(selected_internet))
]

if filtered_df.empty:
    st.warning("No records match the selected filter combination. Please broaden your selection.")
    st.stop()

# Core Calculated Metrics
tot_cust = len(filtered_df)
churn_cust = (filtered_df["customer_status"] == "Churned").sum()
retained_cust = (filtered_df["customer_status"] == "Retained").sum()
churn_rate = churn_cust / tot_cust if tot_cust > 0 else 0
retention_rate = retained_cust / tot_cust if tot_cust > 0 else 0
tot_mrr = filtered_df["MonthlyCharges"].sum()
mrr_risk = filtered_df[filtered_df["customer_status"] == "Churned"]["MonthlyCharges"].sum()
mrr_risk_pct = (mrr_risk / tot_mrr * 100) if tot_mrr > 0 else 0
avg_tenure = filtered_df["tenure"].mean()
avg_monthly = filtered_df["MonthlyCharges"].mean()

# Header Banner
st.markdown('<div class="main-title">Customer Churn & Recurring Revenue Risk Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SaaS Subscription Analytics & Retention Intelligence Platform (7,043 Accounts Census)</div>', unsafe_allow_html=True)

# Top KPI Strip
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total Customers</div><div class="metric-value">{tot_cust:,}</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Churn Rate</div><div class="metric-value metric-alert">{churn_rate:.2%}</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Retained Base</div><div class="metric-value metric-success">{retained_cust:,}</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total MRR</div><div class="metric-value metric-primary">${tot_mrr:,.0f}</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="metric-card"><div class="metric-title">MRR at Risk</div><div class="metric-value metric-alert">${mrr_risk:,.0f}</div></div>', unsafe_allow_html=True)
with kpi6:
    st.markdown(f'<div class="metric-card"><div class="metric-title">% MRR at Risk</div><div class="metric-value metric-alert">{mrr_risk_pct:.1f}%</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# VIEW 1: EXECUTIVE OVERVIEW
# ------------------------------------------------------------------------------
if app_mode == "Executive Overview":
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📌 Churn Rate by Contract Commitment")
        contract_agg = filtered_df.groupby("Contract").agg(
            total=("customerID", "count"),
            churned=("customer_status", lambda x: (x == "Churned").sum()),
            mrr_risk=("mrr_at_risk", "sum")
        ).reset_index()
        contract_agg["churn_rate"] = (contract_agg["churned"] / contract_agg["total"]) * 100
        
        chart_contract = alt.Chart(contract_agg).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X("Contract:N", title="Contract Type", sort=["Month-to-month", "One year", "Two year"]),
            y=alt.Y("churn_rate:Q", title="Churn Rate (%)"),
            color=alt.Color("Contract:N", scale=alt.Scale(domain=["Month-to-month", "One year", "Two year"], range=["#ef4444", "#f59e0b", "#10b981"]), legend=None),
            tooltip=["Contract", alt.Tooltip("churn_rate:Q", format=".2f", title="Churn Rate (%)"), alt.Tooltip("churned:Q", title="Churned Accounts"), alt.Tooltip("mrr_risk:Q", format="$,.2f", title="Lost MRR ($)")]
        ).properties(height=320)
        st.altair_chart(chart_contract, use_container_width=True)
        st.caption("Month-to-month contracts exhibit over **42.7% churn**, driving **86.9%** of total recurring revenue loss.")
    
    with col_r:
        st.subheader("⏳ Churn Rate across Tenure Lifecycle Bands")
        tenure_order = ["0-6 Months", "7-12 Months", "13-24 Months", "25-36 Months", "37-48 Months", "49-60 Months", "60+ Months"]
        tenure_agg = filtered_df.groupby("tenure_band").agg(
            total=("customerID", "count"),
            churned=("customer_status", lambda x: (x == "Churned").sum()),
            mrr_risk=("mrr_at_risk", "sum")
        ).reindex(tenure_order).dropna().reset_index()
        tenure_agg["churn_rate"] = (tenure_agg["churned"] / tenure_agg["total"]) * 100
        
        chart_tenure = alt.Chart(tenure_agg).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X("tenure_band:N", title="Tenure Band", sort=tenure_order),
            y=alt.Y("churn_rate:Q", title="Churn Rate (%)"),
            color=alt.Color("churn_rate:Q", scale=alt.Scale(scheme="reds"), legend=None),
            tooltip=["tenure_band", alt.Tooltip("churn_rate:Q", format=".2f", title="Churn Rate (%)"), alt.Tooltip("churned:Q", title="Lost Customers"), alt.Tooltip("mrr_risk:Q", format="$,.2f", title="Lost MRR ($)")]
        ).properties(height=320)
        st.altair_chart(chart_tenure, use_container_width=True)
        st.caption("Over **52.9%** of subscribers churn during the first 180 days (0-6M cliff). Retention stabilizes past Month 12.")

    st.markdown("---")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.subheader("📈 Customer Retention Curve across Milestones")
        milestones = [1, 3, 6, 12, 24, 36, 48, 60, 72]
        c_records = []
        for m in milestones:
            act = (filtered_df["tenure"] >= m).sum()
            ret = ((filtered_df["tenure"] >= m) & (filtered_df["customer_status"] == "Retained")).sum()
            r_pct = (ret / act * 100) if act > 0 else 0
            c_records.append({"Milestone (Months)": m, "Active Retention (%)": r_pct, "Subscribers Remaining": act})
        df_ret_curve = pd.DataFrame(c_records)
        
        chart_curve = alt.Chart(df_ret_curve).mark_line(point=True, color="#0284c7", strokeWidth=3).encode(
            x=alt.X("Milestone (Months):Q", title="Tenure Milestones (Months)"),
            y=alt.Y("Active Retention (%):Q", scale=alt.Scale(domain=[60, 100]), title="Retention Rate (%)"),
            tooltip=["Milestone (Months)", alt.Tooltip("Active Retention (%):Q", format=".2f"), "Subscribers Remaining"]
        ).properties(height=300)
        st.altair_chart(chart_curve, use_container_width=True)
        st.caption("Mature subscribers reaching 5+ years (60M) reach a **93.32% retention rate**.")
        
    with col_b2:
        st.subheader("💰 Monthly Recurring Revenue at Risk ($)")
        contract_mrr = filtered_df[filtered_df["customer_status"] == "Churned"].groupby("Contract")["MonthlyCharges"].sum().reset_index()
        chart_mrr = alt.Chart(contract_mrr).mark_bar().encode(
            x=alt.X("MonthlyCharges:Q", title="MRR at Risk ($ USD)"),
            y=alt.Y("Contract:N", sort="-x", title=""),
            color=alt.Color("Contract:N", scale=alt.Scale(domain=["Month-to-month", "One year", "Two year"], range=["#ef4444", "#f59e0b", "#10b981"]), legend=None),
            tooltip=["Contract", alt.Tooltip("MonthlyCharges:Q", format="$,.2f", title="MRR Lost ($)")]
        ).properties(height=300)
        st.altair_chart(chart_mrr, use_container_width=True)
        st.caption("Month-to-month accounts represent **$120,847.10** of the total exposed $139.1K MRR.")

# ------------------------------------------------------------------------------
# VIEW 2: CHURN DRIVERS & DIAGNOSTICS
# ------------------------------------------------------------------------------
elif app_mode == "Churn Drivers & Diagnostics":
    st.subheader("🔍 Deep-Dive: Service, Add-On & Payment Friction Points")
    
    cd1, cd2 = st.columns(2)
    with cd1:
        st.write("##### Churn by Internet Service & Tech Support")
        tech_agg = filtered_df.groupby(["InternetService", "TechSupport"]).agg(
            total=("customerID", "count"),
            churned=("customer_status", lambda x: (x == "Churned").sum())
        ).reset_index()
        tech_agg["churn_rate"] = (tech_agg["churned"] / tech_agg["total"]) * 100
        
        tech_chart = alt.Chart(tech_agg).mark_bar().encode(
            x=alt.X("InternetService:N", title="Internet Service"),
            y=alt.Y("churn_rate:Q", title="Churn Rate (%)"),
            color=alt.Color("TechSupport:N", title="Tech Support"),
            xOffset="TechSupport:N",
            tooltip=["InternetService", "TechSupport", alt.Tooltip("churn_rate:Q", format=".2f", title="Churn %")]
        ).properties(height=320)
        st.altair_chart(tech_chart, use_container_width=True)
        st.caption("Subscribers with Fiber Optic without Tech Support churn at **41.6%**.")
        
    with cd2:
        st.write("##### Churn by Billing Payment Instrument")
        pm_agg = filtered_df.groupby("PaymentMethod").agg(
            total=("customerID", "count"),
            churned=("customer_status", lambda x: (x == "Churned").sum()),
            mrr_risk=("mrr_at_risk", "sum")
        ).reset_index()
        pm_agg["churn_rate"] = (pm_agg["churned"] / pm_agg["total"]) * 100
        
        pm_chart = alt.Chart(pm_agg).mark_bar().encode(
            x=alt.X("churn_rate:Q", title="Churn Rate (%)"),
            y=alt.Y("PaymentMethod:N", sort="-x", title=""),
            color=alt.Color("churn_rate:Q", scale=alt.Scale(scheme="orangered"), legend=None),
            tooltip=["PaymentMethod", alt.Tooltip("churn_rate:Q", format=".2f", title="Churn %"), alt.Tooltip("mrr_risk:Q", format="$,.2f", title="Lost MRR ($)")]
        ).properties(height=320)
        st.altair_chart(pm_chart, use_container_width=True)
        st.caption("Electronic Check has a **45.29% churn rate**, shedding **$80.9K in MRR**.")

# ------------------------------------------------------------------------------
# VIEW 3: REVENUE RISK & MATRIX
# ------------------------------------------------------------------------------
elif app_mode == "Revenue Risk & Matrix":
    st.subheader("🎯 2x2 Risk-Value Prioritization Matrix")
    
    matrix_df = filtered_df.groupby("risk_segment").agg(
        customers=("customerID", "count"),
        churned=("customer_status", lambda x: (x == "Churned").sum()),
        total_mrr=("MonthlyCharges", "sum"),
        mrr_risk=("mrr_at_risk", "sum")
    ).reset_index()
    matrix_df["churn_rate"] = (matrix_df["churned"] / matrix_df["customers"]) * 100
    matrix_df["%_of_lost_mrr"] = (matrix_df["mrr_risk"] / df["mrr_at_risk"].sum()) * 100
    
    col_m1, col_m2 = st.columns([3, 2])
    with col_m1:
        st.dataframe(
            matrix_df.style.format({
                "customers": "{:,}",
                "churned": "{:,}",
                "churn_rate": "{:.2f}%",
                "total_mrr": "${:,.2f}",
                "mrr_risk": "${:,.2f}",
                "%_of_lost_mrr": "{:.2f}%"
            }),
            use_container_width=True
        )
    with col_m2:
        m_chart = alt.Chart(matrix_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("mrr_risk:Q", title="Lost MRR ($)"),
            color=alt.Color("risk_segment:N", title="Strategic Tier", scale=alt.Scale(scheme="category10")),
            tooltip=["risk_segment", alt.Tooltip("mrr_risk:Q", format="$,.2f", title="Lost MRR ($)")]
        ).properties(height=300)
        st.altair_chart(m_chart, use_container_width=True)

# ------------------------------------------------------------------------------
# VIEW 4: WHAT-IF RETENTION SIMULATOR
# ------------------------------------------------------------------------------
elif app_mode == "What-If Simulator":
    st.subheader("💡 Interactive Churn Reduction & Revenue Recovery Simulator")
    st.write("Simulate strategic interventions to model Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR) saved.")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        m2m_conv_pct = st.slider("Month-to-Month to Annual Conversion Rate (%)", 0, 50, 15, help="Percentage of Month-to-Month subscribers shifted to 1-Year plans")
        early_churn_red_pct = st.slider("Early-Tenure (0-6M) Onboarding Churn Reduction (%)", 0, 50, 20, help="Percentage reduction in churn rate for new subscribers")
        echeck_autopay_conv_pct = st.slider("Electronic Check to Automated Autopay Migration (%)", 0, 50, 25, help="Percentage of Electronic Check users migrated to Autopay")
    
    with sim_col2:
        # Simulation math
        # 1. M2M conversion impact: M2M churn drops from 42.71% to 11.27% (diff = 31.44% on converted base)
        m2m_churned_mrr = 120847.10
        m2m_saved_mrr = m2m_churned_mrr * (m2m_conv_pct / 100) * ((42.71 - 11.27) / 42.71)
        
        # 2. Early tenure saved: $49,896.10 early MRR loss * reduction %
        early_saved_mrr = 49896.10 * (early_churn_red_pct / 100)
        
        # 3. E-check autopay migration saved: E-check churn (45.29%) -> Autopay churn (15.24%)
        echeck_churned_mrr = 80894.65
        echeck_saved_mrr = echeck_churned_mrr * (echeck_autopay_conv_pct / 100) * ((45.29 - 15.24) / 45.29)
        
        tot_saved_mrr = m2m_saved_mrr + early_saved_mrr + echeck_saved_mrr
        tot_saved_arr = tot_saved_mrr * 12
        
        st.markdown(f"""
        <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:0.9rem; font-weight:700; color:#166534; text-transform:uppercase;">Estimated Monthly Revenue Saved</div>
            <div style="font-size:2.4rem; font-weight:800; color:#15803d; margin:6px 0;">+${tot_saved_mrr:,.2f} / Month</div>
            <div style="font-size:1.1rem; font-weight:600; color:#166534;">Annualized Revenue Protected: <b>+${tot_saved_arr:,.2f} ARR</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.write(f"- **Annual Plan Conversion:** +${m2m_saved_mrr:,.2f}/mo")
        st.write(f"- **90-Day Onboarding Program:** +${early_saved_mrr:,.2f}/mo")
        st.write(f"- **Autopay Migration:** +${echeck_saved_mrr:,.2f}/mo")

# ------------------------------------------------------------------------------
# VIEW 5: SQL & DATA EXPLORER
# ------------------------------------------------------------------------------
elif app_mode == "SQL & Data Explorer":
    st.subheader("🗄️ SQL Query Sandbox & Dataset Inspector")
    
    st.write("##### Sample SQL Analytical Queries")
    sql_query_choice = st.selectbox(
        "Select Pre-Built Analytical Query",
        [
            "SELECT contract, count(*), sum(MonthlyCharges) FROM customers GROUP BY contract",
            "SELECT tenure_band, avg(MonthlyCharges), sum(mrr_at_risk) FROM customers GROUP BY tenure_band",
            "SELECT payment_method, count(*) FILTER(where Churn='Yes') as churned FROM customers GROUP BY payment_method"
        ]
    )
    
    st.code(sql_query_choice, language="sql")
    
    st.write("##### Filtered Census Data Records (Top 100)")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    csv_export = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_export,
        file_name="filtered_customer_churn_data.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Built for Executive SaaS Analytics Portfolio | Data Analyst Portfolio Project | Python, PostgreSQL, Excel, Power BI")
