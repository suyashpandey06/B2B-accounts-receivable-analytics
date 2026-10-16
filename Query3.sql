/* 
========================================================================================
PROJECT: B2B Accounts Receivable & Working Capital Intelligence
BUSINESS QUESTION 3:
"What is the historical payment turnaround behavior for each client, and which accounts 
consistently delay invoice settlements beyond agreed contract terms (Net 30/45)?"

BUSINESS OBJECTIVE:
Analyze client settlement discipline to renegotiate payment terms during annual 
contract renewals and reduce average Days Sales Outstanding (DSO).

TECHNICAL IMPLEMENTATION:
- Advanced Window Function: AVG(DATEDIFF(...)) OVER (PARTITION BY ClientID).
- Tracks individual transaction lag against the client's running average turnaround delay.

KEY BUSINESS FINDINGS:
- Key enterprise accounts systematically delay settlements by 5 to 9 days past the due date.
- Outlier transactions demonstrated payment settlement delays stretching up to 48 days.
========================================================================================
*/
SELECT 
    f.ClientID,
    f.ClientName,
    f.InvoiceID,
    f.InvoiceAmount,
    f.DueDate,
    f.PaymentDate,
    DATEDIFF(f.PaymentDate, f.DueDate) AS Delay_Days_Per_Invoice,
    ROUND(AVG(DATEDIFF(f.PaymentDate, f.DueDate)) OVER(PARTITION BY f.ClientID), 1) AS Client_Average_Delay_Days
FROM Fact_Invoices f
WHERE f.PaymentDate IS NOT NULL AND f.PaymentDate != ''
ORDER BY Client_Average_Delay_Days DESC, f.ClientID;