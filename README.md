# 📊 B2B Accounts Receivable & Working Capital Intelligence (90-Day Diagnostic)

## 📌 Executive Summary
An end-to-end financial analytics and credit risk diagnostic evaluating **90 consecutive days** of B2B invoicing transactions across 12 corporate client accounts. 

The objective of this project is to uncover liquidity bottlenecks, evaluate delinquent payment behaviors, and provide CFO-level strategic recommendations to unlock working capital trapped in overdue invoices and operational disputes.

---

## 🛠️ Tech Stack & Relational Architecture
- **Database Engine:** MySQL Server 8.0 & MySQL Workbench
- **Business Intelligence:** Microsoft Power BI Desktop (Star Schema Modeling, Advanced DAX)
- **Data Engineering:** Microsoft Excel / CSV (90-Day Synthetic Ledger with Delinquency Scenarios)

### Data Architecture (Star Schema)
- **`Dim_Clients` (Dimension Table):** `ClientID` (PK), `ClientName`, `Industry`, `Region`, `CreditLimit_INR`, `PaymentTerms`
- **`Fact_Invoices` (Fact Table):** `InvoiceID` (PK), `ClientID` (FK), `InvoiceDate`, `DueDate`, `PaymentDate`, `InvoiceAmount`, `PaidAmount`, `BalanceAmount`, `OverdueDays`, `AgingBucket`, `PaymentStatus`, `DisputeFlag`
- **Relationship:** One-to-Many (`1 : *`) between `Dim_Clients[ClientID]` and `Fact_Invoices[ClientID]`

---

## 📈 Core Financial KPIs

| Metric | Value | Business Significance |
| :--- | :--- | :--- |
| **Gross Billed Revenue** | **₹5.96 Cr** | Total transaction volume invoiced over 90 days |
| **Total Outstanding (AR)** | **₹4.25 Cr** | Gross uncollected capital currently outstanding |
| **Total Overdue Debt** | **₹1.40 Cr** | Capital exceeding agreed contract due dates |
| **Portfolio Overdue Ratio** | **32.8%** | Aggregate delinquency rate (*Industry benchmark: < 15%*) |
| **Days Sales Outstanding (DSO)** | **64.2 Days** | Average cash turnaround time (*Contract target: 45 Days*) |

---

## 🔍 SQL Analytical Queries & Findings

### 1. Accounts Receivable Aging Breakdown (`Query1.sql`)
- **Business Problem:** Categorize open debt into risk buckets (Current, 1–30, 31–60, 61–90 days).
- **Core Insight:** **34.89% (~₹1.48 Cr)** of outstanding debt is overdue. While ₹96.65L is in the 1–30 day bucket, **₹47.23L** has slipped into the 31–60 day critical delay bracket.
- **SQL Logic:** Conditional classification using `CASE WHEN` and subquery percentage calculations.

### 2. Client Credit Governance & Limit Breaches (`Query2.sql`)
- **Business Problem:** Identify corporate clients exceeding 70% credit utilization with high overdue debt.
- **Core Insight:** **Meridian Enterprise Software (CL-107)** and **Apex Auto Manufacturing (CL-109)** breached credit limits, operating at **143.95%** and **140.90%** credit utilization, with over **50% of their total balance overdue**.
- **SQL Logic:** Common Table Expression (CTE) with aggregate multi-table `JOIN` and threshold filters.

### 3. Payment Turnaround & Average Settlement Lag (`Query3.sql`)
- **Business Problem:** Evaluate historical payment turnaround discipline per client against contract terms.
- **Core Insight:** Enterprise accounts systematically delay settlements by **5 to 9 days** past agreed Net 30/45 terms, with outlier cases extending up to **48 days**.
- **SQL Logic:** Analytical Window Functions: `AVG(DATEDIFF(...)) OVER (PARTITION BY ClientID)`.

### 4. Billing Disputes & Frozen Cash-at-Risk (`Query4.sql`)
- **Business Problem:** Quantify the volume of capital locked in active invoice disputes by industry.
- **Core Insight:** Over **₹28 Lakh** of working capital is actively frozen due to client billing disputes, heavily concentrated in the Telecom and Manufacturing sectors.
- **SQL Logic:** Industry aggregation with conditional counting: `SUM(CASE WHEN DisputeFlag = 'Yes' THEN ...)`

### 5. Cash Recovery Decay & Cumulative Running Inflow (`Query5.sql`)
- **Business Problem:** Track month-on-month collection efficiency and cumulative cash recovery trajectory.
- **Core Insight:** Cash recovery efficiency stood strong at **~48–50%** in July and August, but dropped sharply to **13.8% (Sep)** and **7.4% (Oct)** due to stretched credit terms, widening the cash deficit.
- **SQL Logic:** Time-series aggregation and cumulative running totals using `SUM(SUM(...)) OVER (ORDER BY Month)`.

---

## 💡 Strategic Recommendations for Management
1. **Immediate Credit Hold:** Freeze new purchase orders for accounts exceeding 120% credit limit utilization until their overdue balance drops below 80%.
2. **Payment Terms Restructuring:** Transition chronic late-paying accounts (average delay > 7 days) from Net 30/45 to Net 15, paired with a 2% early payment discount (2/10 Net 30).
3. **Dispute Resolution SLA:** Establish a strict 7-day cross-functional SLA between billing and logistics teams to expedite dispute resolution and unfreeze ₹28L in disputed funds.

---

## 📂 Repository File Structure
```text
├── README.md                              <- Executive Project Documentation
├── B2B_Working_Capital_Dashboard.pbix      <- Interactive Power BI Report
│
├── sql/
│   ├── Query1_Aging_Analysis.sql          <- Aging bucket distribution logic
│   ├── Query2_Credit_Risk_Breach.sql      <- CTE for credit limit violations
│   ├── Query3_Payment_Delay_Window.sql    <- Window function for average delay
│   ├── Query4_Disputed_Cash_At_Risk.sql   <- Dispute rate and trapped cash
│   └── Query5_Monthly_Inflow_Trend.sql    <- Cumulative running collections
│
├── data/
│   ├── Dim_Clients.csv                    <- Dimension client master data
│   └── Fact_Invoices.csv                  <- Transactional invoice records
│
└── assets/
    └── dashboard_preview.png              <- Executive dashboard screenshot
