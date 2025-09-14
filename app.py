
import streamlit as st
import pandas as pd

# Step 1: Load Synthetic Data
transactions = pd.read_csv("synthetic_data.csv")

# Step 2: Dashboard Title
st.title("Treasury Optimization Dashboard")

# Step 3: Display Recent Transactions
st.subheader("Recent Transactions")
st.dataframe(transactions.sort_values(by='date', ascending=False))

# Step 4: Calculate Current Balances
current_balances = transactions.groupby('account')['running_balance'].last()
st.subheader("Current Balances")
st.bar_chart(current_balances)

# Step 5: Alerts for High/Low Balances
st.subheader("Alerts")
for acc, bal in current_balances.items():
    if bal > 90000:
        st.warning(f"{acc}: High idle cash detected → ${bal}")
    elif bal < 20000:
        st.error(f"{acc}: Low balance alert → ${bal}")

# Step 6: Basic Rule-Based Optimization Suggestions
st.subheader("Optimization Suggestions")
high_balance_accounts = current_balances[current_balances > 90000]
low_balance_accounts = current_balances[current_balances < 50000]

for high_acc, high_bal in high_balance_accounts.items():
    for low_acc, low_bal in low_balance_accounts.items():
        suggested_amount = min(20000, high_bal - 90000)
        st.info(f"Suggestion: Transfer ${suggested_amount} from {high_acc} to {low_acc}")

# Optional: FX conversion suggestion
fx_rates = {'USD_EUR': 0.93, 'USD_GBP': 0.81}
if 'USD Account' in high_balance_accounts:
    st.info(f"FX Suggestion: Convert $20k USD → €{round(20000*fx_rates['USD_EUR'])}")
