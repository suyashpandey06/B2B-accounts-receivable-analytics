import pandas as pd

# Enriched fact file load karein
df = pd.read_csv('fact_invoices_enriched.csv')
df['Invoice_Date'] = pd.to_datetime(df['Invoice_Date'])

# Month column extract karein (YYYY-MM)
df['Billing_Month'] = df['Invoice_Date'].dt.to_period('M').astype(str)

# Monthly trends aggregate karein
monthly_summary = df.groupby('Billing_Month').agg(
    Total_Invoices=('Invoice_ID', 'count'),
    Gross_Billed_INR=('Invoice_Amount', 'sum'),
    Cash_Collected_INR=('Paid_Amount', 'sum'),
    Outstanding_AR_INR=('Balance_Amount', 'sum')
).reset_index()

# Collection efficiency percentage
monthly_summary['Collection_Rate_Pct'] = round(
    (monthly_summary['Cash_Collected_INR'] / monthly_summary['Gross_Billed_INR']) * 100, 2
)

# Cumulative running total of cash collected
monthly_summary['Cumulative_Cash_Collected_INR'] = monthly_summary['Cash_Collected_INR'].cumsum()

print("\n================== MONTHLY CASH CONVERSION & RECOVERY ==================")
print(monthly_summary.to_string(index=False))
print("========================================================================\n")

# Power BI export
monthly_summary.to_csv('dim_monthly_cash_trends.csv', index=False)
print("Success: 'dim_monthly_cash_trends.csv' create ho gayi hai Power BI ke liye!")