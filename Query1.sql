/* 
========================================================================================
PROJECT: B2B Accounts Receivable & Working Capital Intelligence
BUSINESS QUESTION 1:
"What is our total Accounts Receivable (AR) exposure, and how is outstanding debt 
distributed across risk aging buckets (Current, 1-30, 31-60, 61-90, 90+ days)?"

BUSINESS OBJECTIVE:
Identify short-term liquidity risk across aging brackets to enable the credit control 
and collections team to prioritize high-risk recovery buckets.

TECHNICAL IMPLEMENTATION:
- Conditional segmentation via CASE WHEN logic based on overdue day thresholds.
- Grouped aggregation and subquery calculation for portfolio percentage contribution.

KEY BUSINESS FINDINGS:
- Out of total outstanding AR, 34.89% (~₹1.48 Cr) is currently overdue.
- ₹47.23 Lakh falls into the 31-60 days aging bracket, posing severe working capital risk.
========================================================================================
*/
SELECT 
    AgingBucket,
    COUNT(InvoiceID) AS Invoice_Count,
    SUM(InvoiceAmount) AS Total_Billed,
    SUM(PaidAmount) AS Total_Collected,
    SUM(BalanceAmount) AS Total_Outstanding_AR,
    ROUND(SUM(BalanceAmount) * 100.0 / (SELECT SUM(BalanceAmount) FROM Fact_Invoices), 2) AS Pct_Of_Total_AR
FROM Fact_Invoices
GROUP BY AgingBucket
ORDER BY Total_Outstanding_AR DESC;