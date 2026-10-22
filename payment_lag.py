import pandas as pd
import numpy as np

# Step 1 se nikli enriched file load karein
df = pd.read_csv('fact_invoices_enriched.csv')

# Sirf settled/paid invoices filter karein jahan payment date available hai
paid_invoices = df[df['Payment_Date'].notna() & (df['Payment_Status'] != 'Unpaid')].copy()

# Client-level delay behavior analyze karein
client_delay_summary = paid_invoices.groupby(['Client_ID', 'Client_Name', 'Industry']).agg(
    Settled_Invoices_Count=('Invoice_ID', 'count'),
    Total_Paid_Value=('Paid_Amount', 'sum'),
    Average_Payment_Delay_Days=('Payment_Delay_Days', lambda x: round(x.mean(), 1)),
    Max_Payment_Delay_Days=('Payment_Delay_Days', 'max'),
    Min_Payment_Delay_Days=('Payment_Delay_Days', 'min')
).reset_index()

# Settlement Discipline Tier categorize karein
def categorize_discipline(avg_delay):
    if avg_delay <= 0:
        return 'Prompt Payer (On-time / Early)'
    elif 1 <= avg_delay <= 7:
        return 'Mild Delay (Grace Period Acceptable)'
    elif 8 <= avg_delay <= 15:
        return 'Moderate Delay (Follow-up Required)'
    else:
        return 'Severe Habitual Defaulter'

client_delay_summary['Discipline_Tier'] = client_delay_summary['Average_Payment_Delay_Days'].apply(categorize_discipline)

# Sort by highest average payment delay
client_delay_summary = client_delay_summary.sort_values(by='Average_Payment_Delay_Days', ascending=False)

print("\n================== CLIENT PAYMENT TURNAROUND BEHAVIOR ==================")
print(client_delay_summary[[
    'Client_Name', 
    'Settled_Invoices_Count', 
    'Average_Payment_Delay_Days', 
    'Max_Payment_Delay_Days', 
    'Discipline_Tier'
]].to_string(index=False))
print("========================================================================\n")

# Export for Power BI
client_delay_summary.to_csv('dim_payment_behavior.csv', index=False)
print("Success: 'dim_payment_behavior.csv' create ho gayi hai Power BI ke liye!")
