# Power BI Interactive Dashboard Specification (3 Pages)

## Page 1: Executive Overview (High-Level Performance)
- **Target Audience:** Chief Executive Officer, Chief Revenue Officer, VP of Customer Success.
- **Goal:** Provide immediate clarity on baseline churn, exposed MRR, contract insulation, and lifecycle retention curves.

### Visual Components:
1. **Top KPI Strip (6 Cards):**
   - Total Customers: `7,043`
   - Retained Customers: `5,174`
   - Overall Churn Rate: `26.54%` (Red callout)
   - Total MRR: `\$456,117`
   - MRR at Risk: `\$139,131` (Red callout)
   - % MRR at Risk: `30.50%`
2. **Visual 1 (Clustered Column Chart):** Churn Rate by Contract Type (`Month-to-month: 42.71%`, `One year: 11.27%`, `Two year: 2.83%`).
3. **Visual 2 (Bar Chart):** Churn Rate by Tenure Band (`0-6M: 52.94%`, `7-12M: 35.89%`, down to `60+M: 6.61%`).
4. **Visual 3 (Line Chart with Benchmark Lines):** Customer Retention Curve across tenure milestones (1m to 72m), highlighting the 6-month drop-off and 5-year retention (`93.32%`).
5. **Visual 4 (Horizontal Bar Chart):** MRR at Risk by Contract Type (`\$120,847` in Month-to-Month).

---

## Page 2: Churn Drivers & Customer Behavior (Deep Diagnostics)
- **Target Audience:** VP of Product, Head of Customer Support, Marketing Operations.
- **Goal:** Uncover operational and product friction causing subscriber cancellation.

### Visual Components:
1. **Visual 1 (Grouped Bar Chart):** Churn Rate by Internet Service & Tech Support Add-on (Highlights 41.6% churn in unassisted Fiber Optic users).
2. **Visual 2 (Horizontal Bar Chart):** Churn Rate by Payment Method (Highlights 45.29% churn in Electronic Check users).
3. **Visual 3 (Clustered Column):** Churn by Senior Citizen Status & Paperless Billing.
4. **Visual 4 (KDE / Distribution Chart):** Monthly Charges Density comparing Retained vs Churned customers.

---

## Page 3: Revenue-at-Risk & Prioritization Matrix (Actionable Targeting)
- **Target Audience:** Account Management, Retention Taskforce, Revenue Operations.
- **Goal:** Pinpoint high-MRR, high-risk accounts to maximize retention ROI.

### Visual Components:
1. **Visual 1 (Ranked Bar Chart):** MRR at Risk by Strategic Segment (`Tier 1 Critical: \$54,687`, `Tier 3 High MRR: \$38,167`).
2. **Visual 2 (Pareto Line Chart):** Cumulative % of Lost MRR vs % of Churned Accounts.
3. **Visual 3 (Stacked Column Chart):** Total MRR split by Customer Status across Tenure Bands.
4. **Visual 4 (Heatmap / Matrix Table):** 2x2 Risk vs Revenue Exposure Matrix ($ at Risk).

---

## Interactive Slicers on All Pages:
- **Contract Type:** `Month-to-month`, `One year`, `Two year`
- **Tenure Band:** `0-6M`, `7-12M`, `13-24M`, `25-36M`, `37-48M`, `49-60M`, `60+M`
- **Payment Method:** `Electronic check`, `Mailed check`, `Bank transfer`, `Credit card`
- **Internet Service:** `DSL`, `Fiber optic`, `No`
- **Customer Status:** `Churned`, `Retained`
