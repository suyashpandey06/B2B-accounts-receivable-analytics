import pandas as pd
import numpy as np

# 1. Dataset Load & Date Parsing
df = pd.read_csv('b2b_invoicing_data.csv')
df['Payment_Date'] = df['Payment_Date'].replace('NULL', np.nan)

for col in ['Invoice_Date', 'Due_Date', 'Payment_Date']:
    df[col] = pd.to_datetime(df[col])

# 2. Financial Metrics Engineering
snapshot_date = pd.to_datetime('2026-10-16')

# Balance Outstanding
df['Balance_Amount'] = df['Invoice_Amount'] - df['Paid_Amount']

# Turnaround Delay (Paid invoices ke liye)
df['Payment_Delay_Days'] = (df['Payment_Date'] - df['Due_Date']).dt.days

# Overdue Days (Unpaid invoices ke liye)
def calculate_overdue(row):
    if row['Balance_Amount'] > 0 and pd.isna(row['Payment_Date']):
        return max((snapshot_date - row['Due_Date']).days, 0)
    return 0

df['Overdue_Days'] = df.apply(calculate_overdue, axis=1)

# Risk Aging Buckets
def assign_aging_bucket(days, balance):
    if balance == 0:
        return 'Settled'
    elif days == 0:
        return 'Current (Not Due)'
    elif 1 <= days <= 30:
        return '1-30 Days'
    elif 31 <= days <= 60:
        return '31-60 Days'
    elif 61 <= days <= 90:
        return '61-90 Days'
    else:
        return '90+ Days'

df['Aging_Bucket'] = df.apply(lambda x: assign_aging_bucket(x['Overdue_Days'], x['Balance_Amount']), axis=1)

# 3. Portfolio Risk Summary Console Output
print("=================== PORTFOLIO METRICS ===================")
total_ar = df['Balance_Amount'].sum()
overdue_ar = df[df['Overdue_Days'] > 0]['Balance_Amount'].sum()
disputed_ar = df[df['Dispute_Flag'] == 'Yes']['Balance_Amount'].sum()

print(f"Total Outstanding AR   : Rs. {total_ar:,.2f}")
print(f"Total Overdue Balance  : Rs. {overdue_ar:,.2f}")
print(f"Overdue Percentage     : {(overdue_ar / total_ar) * 100:.2f}%")
print(f"Disputed Cash at Risk  : Rs. {disputed_ar:,.2f}")
print("=========================================================")

# 4. Export Cleaned File for Power BI
df.to_csv('fact_invoices_enriched.csv', index=False)
print("\nSuccess: 'fact_invoices_enriched.csv' create ho gayi hai Power BI ke liye!")