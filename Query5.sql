/* 
========================================================================================
PROJECT: B2B Accounts Receivable & Working Capital Intelligence
BUSINESS QUESTION 5:
"What is the month-on-month trend between gross billed revenue and actual cash collected, 
and how is the cumulative cash collection trajectory progressing over the 90-day window?"

BUSINESS OBJECTIVE:
Evaluate the company's cash conversion efficiency and track the widening working capital 
gap between revenue recognition and actual cash liquidity.

TECHNICAL IMPLEMENTATION:
- Time-series monthly aggregation using DATE_FORMAT(InvoiceDate, '%Y-%m').
- Monthly collection recovery rate percentage.
- Cumulative running total using analytical Window Function: SUM(SUM(...)) OVER (ORDER BY Month).

KEY BUSINESS FINDINGS:
- Cash collection efficiency held strong at ~48-50% in July and August.
- September and October collection rates dropped sharply to 13.8% and 7.4% due to long credit terms, 
  creating a substantial short-term working capital funding deficit.
========================================================================================
*/
SELECT 
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS Billing_Month,
    COUNT(InvoiceID) AS Invoices_Issued,
    SUM(InvoiceAmount) AS Monthly_Billed_INR,
    SUM(PaidAmount) AS Monthly_Collected_INR,
    SUM(BalanceAmount) AS Monthly_Outstanding_INR,
    ROUND(SUM(PaidAmount) * 100.0 / NULLIF(SUM(InvoiceAmount), 0), 2) AS Collection_Rate_Pct,
    -- Running Cumulative Collected Amount across 90 Days
    SUM(SUM(PaidAmount)) OVER (ORDER BY DATE_FORMAT(InvoiceDate, '%Y-%m')) AS Cumulative_Cash_Collected_INR
FROM Fact_Invoices
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY Billing_Month ASC;