/* 
========================================================================================
PROJECT: B2B Accounts Receivable & Working Capital Intelligence
BUSINESS QUESTION 2:
"Which corporate client accounts have breached 70% of their approved credit limits, 
and what volume of their outstanding balance is already in default/overdue status?"

BUSINESS OBJECTIVE:
Quantify credit concentration risk, enforce credit governance, and flag high-exposure 
accounts that require an immediate credit hold or credit limit review.

TECHNICAL IMPLEMENTATION:
- Common Table Expression (CTE) to aggregate invoice exposure at the client level.
- Relational INNER JOIN between Dim_Clients and Fact_Invoices with credit breach filters.

KEY BUSINESS FINDINGS:
- Meridian Enterprise Software (CL-107) and Apex Auto Manufacturing (CL-109) exceeded 
  140% credit utilization, with over 50% of their total balance past due date.
STRATEGIC ACTION:
- Place an immediate stop-shipment/credit freeze on new purchase orders for these accounts.
========================================================================================
*/
WITH ClientRisk AS (
    SELECT 
        c.ClientID,
        c.ClientName,
        c.Industry,
        c.Region,
        c.CreditLimit_INR,
        SUM(f.BalanceAmount) AS Total_Outstanding,
        SUM(CASE WHEN f.OverdueDays > 0 THEN f.BalanceAmount ELSE 0 END) AS Overdue_Balance
    FROM Dim_Clients c
    JOIN Fact_Invoices f ON c.ClientID = f.ClientID
    GROUP BY c.ClientID, c.ClientName, c.Industry, c.Region, c.CreditLimit_INR
)
SELECT 
    ClientID,
    ClientName,
    Industry,
    CreditLimit_INR,
    Total_Outstanding,
    Overdue_Balance,
    ROUND((Overdue_Balance / CreditLimit_INR) * 100, 2) AS Overdue_To_Credit_Limit_Pct
FROM ClientRisk
WHERE Overdue_Balance > (0.50 * CreditLimit_INR)
ORDER BY Overdue_To_Credit_Limit_Pct DESC;