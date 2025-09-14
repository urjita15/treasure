import streamlit as st
import pandas as pd

# -----------------------------
# Step 1: Load Synthetic Data
# -----------------------------
transactions = pd.read_csv("synthetic_data.csv")

# Ensure correct data types
transactions['date'] = pd.to_datetime(transactions['date'])
transactions['running_balance'] = pd.to_numeric(transactions['running_balance'])

# -----------------------------
# Step 2: Dashboard Title
# -----------------------------
st.title("Treasury Optimization Dashboard")

# -----------------------------
# Step 3: Display Recent Transactions
# -----------------------------
st.subheader("Recent Transactions")
# Show only the latest 20 transactions to keep table readable
st.write(transactions.sort_values(by='date', ascending=False).head(20))

# -----------------------------
# Step 4: Calculate Current Balances
# -----------------------------
current_balances = transactions.groupby('account')['running_balance'].last().reset_index()
current_balances_dict = dict(zip(current_balances['account'], current_balances['running_balance']))

st.subheader("Current Balances")
st.bar_chart(current_balances.set_index('account'))

# -----------------------------
# Step 5: Alerts for High/Low Balances
# -----------------------------
st.subheader("Alerts")
for acc, bal in current_balances_dict.items():
    if bal > 90000:
        st.warning(f"{acc}: High idle cash detected → ${bal}")
    elif bal < 20000:
        st.error(f"{acc}: Low balance alert → ${bal}")
    else:
        st.success(f"{acc}: Balance within normal range → ${bal}")

# -----------------------------
# Step 6: Basic Rule-Based Optimization Suggestions
# -----------------------------
st.subheader("Optimization Suggestions")

high_balance_accounts = {k: v for k, v in current_balances_dict.items() if v > 88000}
low_balance_accounts = {k: v for k, v in current_balances_dict.items() if v < 85000}

for high_acc, high_bal in high_balance_accounts.items():
    for low_acc, low_bal in low_balance_accounts.items():
        suggested_amount = min(20000, high_bal - 90000)
        st.info(f"Suggestion: Transfer ${suggested_amount} from {high_acc} to {low_acc}")
        break  # limit to one suggestion per low account to avoid flooding

# Optional: FX conversion suggestion (synthetic example)
fx_rates = {'USD_EUR': 0.93, 'USD_GBP': 0.81}
if 'USD Account' in high_balance_accounts:
    st.info(f"FX Suggestion: Convert $20k USD → €{round(20000*fx_rates['USD_EUR'])}")
