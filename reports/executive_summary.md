# Executive Summary Report
## Customer Churn & Recurring Revenue Risk Analysis (SaaS / Subscription Business)

**Target Audience:** Chief Executive Officer, Chief Revenue Officer, Board of Directors  
**Analyzed Population:** Exactly 7,043 Customer Records  
**Total Subscription Base MRR:** $456,116.60  
**Prepared by:** Senior Data Analytics Lead  

---

### Executive KPI Summary

| Metric Category | Key Performance Indicator | Value | Business Impact |
| :--- | :--- | :--- | :--- |
| **Customer Volume** | Total Customer Population | **7,043** | Full active & historical subscriber base analyzed |
| **Retention & Churn** | Retained Active Customers | **5,174 (73.46%)** | Healthy core subscriber base |
| **Retention & Churn** | Churned Customers | **1,869 (26.54%)** | Elevated baseline churn requiring direct intervention |
| **Revenue Exposure** | Total Monthly Recurring Revenue (MRR) | **$456,116.60** | Annualized run-rate: ~$5.47M ARR |
| **Revenue Exposure** | Monthly Recurring Revenue at Risk | **$139,130.85** | Immediate top-line revenue attrition |
| **Revenue Exposure** | Percentage of Total MRR at Risk | **30.50%** | Disproportionate churn impact on high-MRR tiers |
| **Lifecycle Metrics** | Early Tenure (0-6M) Churn Rate | **52.94%** | Primary attrition window ($49.9K MRR lost) |
| **Lifecycle Metrics** | Early Tenure (0-6M) Retention Rate | **47.06%** | Validates early drop-off hypothesis |
| **Lifecycle Metrics** | Mature Cohort (60M+ / 5-Yr) Retention | **93.32%** | Validates high long-term customer stickiness |
| **Customer Lifetime** | Average Customer Tenure | **32.37 Months** | Average lifecycle duration across all segments |
| **Billing Metrics** | Average Monthly Revenue per Customer | **$64.76** | Baseline average subscriber yield |

---

### Key Analytical Findings

1. **Contract Type is the Dominant Predictor of Churn Risk:**
   - **Month-to-Month Contracts:** Churn at **42.71%**, representing **1,655 churned customers** and **$120,847.10 in lost MRR** (**86.86%** of all revenue lost).
   - **1-Year Contracts:** Churn at **11.27%** ($14,118.45 lost MRR).
   - **2-Year Contracts:** Churn at **2.83%** ($4,165.30 lost MRR).
   - *Conclusion:* Longer contractual commitments provide near-complete revenue insulation.

2. **The "First 180 Days" Drop-off Window:**
   - Customers in the 0-6 month window experience a staggering **52.94% churn rate**, shedding **$49,896.10 in MRR**.
   - Beyond 12 months, churn drops below 28%, and beyond 60 months, churn collapses to **6.61%**.

3. **High-Risk Product & Payment Friction:**
   - **Electronic Check:** Churn rate is **45.29%**, generating **$80,894.65 in lost MRR**, compared to ~15% for automated Credit Card or ACH transfer.
   - **Unassisted Fiber Optic Users:** Subscribers with high-speed Fiber Optic without Tech Support or Online Security experience over **41.6% churn**, driven by onboarding friction and higher price point ($75+).

4. **Strategic Risk-Value Prioritization (Pareto Distribution):**
   - **Tier 1 Critical Segment (Month-to-Month, Tenure <= 12M, MRR > $75):** Accounts for **$54,687.20 (39.31%)** of all lost MRR despite representing only 15.02% of customer volume.

---

### Top 5 Strategic Business Recommendations

1. **Launch "Annual Advantage" Contract Conversion Campaign:**
   - Offer Month-to-Month subscribers reaching Month 3 a targeted discount (e.g., 2 months free on an annual plan). Converting just 15% of Month-to-Month users recovers ~$18.1K in recurring MRR.
2. **Implement a Proactive 90-Day Onboarding Program:**
   - Deploy dedicated Customer Success touchpoints at Day 14, Day 30, Day 60, and Day 90 to guide new subscribers through core value realization and mitigate the 52.94% early churn cliff.
3. **Incentivize Automated Autopay Migration:**
   - Provide a one-time $10 account credit or $2/month discount for switching from Electronic Check to Automated ACH or Credit Card payments.
4. **Bundle Premium Support with High-MRR Tiers:**
   - Automatically include complimentary Tech Support and Onboarding Assistance for all Fiber Optic and >$75 MRR plans to eliminate technical friction.
5. **Establish an Early Warning Account Health Scorecard:**
   - Track usage telemetry and support tickets for high-MRR accounts in months 1-6. Trigger automated executive outreach when engagement drops below baseline.
