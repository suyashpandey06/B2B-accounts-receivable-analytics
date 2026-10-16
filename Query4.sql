/* 
========================================================================================
PROJECT: B2B Accounts Receivable & Working Capital Intelligence
BUSINESS QUESTION 4:
"Which industry sectors account for the highest volume of billing disputes, and how much 
working capital is actively trapped in disputed cash-at-risk?"

BUSINESS OBJECTIVE:
Connect billing operational inefficiencies and client friction points directly to 
unrealized cash flow to accelerate operational dispute resolution SLAs.

TECHNICAL IMPLEMENTATION:
- Conditional counting and summing using SUM(CASE WHEN DisputeFlag = 'Yes' THEN ...).
- Industry-level aggregation, dispute incidence rate %, and blocked cash-at-risk metrics.

KEY BUSINESS FINDINGS:
- Over ₹28 Lakh of working capital remains frozen due to active billing disputes.
- Telecommunications and Manufacturing sectors exhibit the highest dispute concentration.
========================================================================================
*/
SELECT 
    c.Industry,
    COUNT(f.InvoiceID) AS Total_Invoices,
    SUM(CASE WHEN f.DisputeFlag = 'Yes' THEN 1 ELSE 0 END) AS Disputed_Invoices_Count,
    ROUND(SUM(CASE WHEN f.DisputeFlag = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(f.InvoiceID), 2) AS Dispute_Rate_Pct,
    SUM(f.BalanceAmount) AS Total_Outstanding_Balance,
    SUM(CASE WHEN f.DisputeFlag = 'Yes' THEN f.BalanceAmount ELSE 0 END) AS Disputed_Cash_At_Risk,
    ROUND(SUM(CASE WHEN f.DisputeFlag = 'Yes' THEN f.BalanceAmount ELSE 0 END) * 100.0 / NULLIF(SUM(f.BalanceAmount), 0), 2) AS Disputed_Balance_Share_Pct
FROM Fact_Invoices f
JOIN Dim_Clients c ON f.ClientID = c.ClientID
GROUP BY c.Industry
ORDER BY Disputed_Cash_At_Risk DESC;