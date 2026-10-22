import pandas as pd

# Enriched fact table load karein
df = pd.read_csv('fact_invoices_enriched.csv')

# Industry-level dispute metrics aggregation
industry_dispute = df.groupby('Industry').agg(
    Total_Invoices=('Invoice_ID', 'count'),
    Disputed_Invoices_Count=('Dispute_Flag', lambda x: (x == 'Yes').sum()),
    Total_Billed=('Invoice_Amount', 'sum'),
    Total_Outstanding_Balance=('Balance_Amount', 'sum'),
    Disputed_Cash_At_Risk=('Balance_Amount', lambda x: x[df.loc[x.index, 'Dispute_Flag'] == 'Yes'].sum())
).reset_index()

# Percentages calculate karein
industry_dispute['Dispute_Rate_Pct'] = round(
    (industry_dispute['Disputed_Invoices_Count'] / industry_dispute['Total_Invoices']) * 100, 2
)
industry_dispute['Disputed_Share_Of_AR_Pct'] = round(
    (industry_dispute['Disputed_Cash_At_Risk'] / industry_dispute['Total_Outstanding_Balance']) * 100, 2
)

# Sort by highest disputed cash
industry_dispute = industry_dispute.sort_values(by='Disputed_Cash_At_Risk', ascending=False)

print("\n================== INDUSTRY BILLING DISPUTE & TRAPPED CASH ==================")
print(industry_dispute[[
    'Industry', 
    'Total_Invoices', 
    'Disputed_Invoices_Count', 
    'Dispute_Rate_Pct', 
    'Disputed_Cash_At_Risk', 
    'Disputed_Share_Of_AR_Pct'
]].to_string(index=False))
print("=============================================================================\n")

# Power BI export
industry_dispute.to_csv('dim_industry_dispute_summary.csv', index=False)
print("Success: 'dim_industry_dispute_summary.csv' create ho gayi hai Power BI ke liye!")