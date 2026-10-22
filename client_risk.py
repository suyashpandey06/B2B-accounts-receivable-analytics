import pandas as pd

# Step 1 se nikli enriched file ko read karein
df = pd.read_csv('fact_invoices_enriched.csv')

# Client level aggregations
client_summary = df.groupby(['Client_ID', 'Client_Name', 'Industry', 'Region']).agg(
    Approved_Credit_Limit=('Credit_Limit', 'first'),
    Total_Invoices_Count=('Invoice_ID', 'count'),
    Total_Billed=('Invoice_Amount', 'sum'),
    Total_Paid=('Paid_Amount', 'sum'),
    Total_Outstanding_AR=('Balance_Amount', 'sum'),
    Overdue_Balance=('Balance_Amount', lambda x: x[df.loc[x.index, 'Overdue_Days'] > 0].sum()),
    Disputed_Cash=('Balance_Amount', lambda x: x[df.loc[x.index, 'Dispute_Flag'] == 'Yes'].sum())
).reset_index()

# Risk Metrics calculation
client_summary['Credit_Utilization_Pct'] = round(
    (client_summary['Total_Outstanding_AR'] / client_summary['Approved_Credit_Limit']) * 100, 2
)
client_summary['Overdue_To_Limit_Pct'] = round(
    (client_summary['Overdue_Balance'] / client_summary['Approved_Credit_Limit']) * 100, 2
)

# Governance Action Categorization
def assign_action(utilization, overdue_ratio):
    if utilization > 100 or overdue_ratio > 50:
        return 'CRITICAL: Place Immediate Credit Freeze'
    elif utilization >= 70:
        return 'WARNING: Require Upfront Advance'
    else:
        return 'NORMAL: Healthy Account'

client_summary['Recommended_Action'] = client_summary.apply(
    lambda row: assign_action(row['Credit_Utilization_Pct'], row['Overdue_To_Limit_Pct']), axis=1
)

# Sorting by highest credit utilization
client_summary = client_summary.sort_values(by='Credit_Utilization_Pct', ascending=False)

print("\n================== CLIENT CREDIT RISK DIAGNOSTIC ==================")
print(client_summary[[
    'Client_Name', 
    'Approved_Credit_Limit', 
    'Total_Outstanding_AR', 
    'Credit_Utilization_Pct', 
    'Recommended_Action'
]].to_string(index=False))
print("===================================================================\n")

# Power BI Dimension Table Export
client_summary.to_csv('dim_client_risk_profile.csv', index=False)
print("Success: 'dim_client_risk_profile.csv' create ho gayi hai Power BI Dimension ke liye!")
