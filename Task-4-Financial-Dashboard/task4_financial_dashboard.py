# Task 4: Financial Dashboard
# Demonstration with synthetic sample data. Replace with official data if provided.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(17)
n = 600
dates = pd.date_range("2025-01-01", "2026-06-30", freq="D")
txn_dates = np.random.choice(dates, size=n)
categories = ["Salary", "Food", "Transport", "Shopping", "Bills", "Healthcare", "Education", "Entertainment", "Travel", "Other"]
types = np.random.choice(["Income", "Expense"], size=n, p=[0.25, 0.75])
rows = []
for i in range(n):
    if types[i] == "Income":
        cat = np.random.choice(["Salary", "Other"], p=[0.8, 0.2])
        amount = round(np.random.uniform(8000, 65000), 2) if cat == "Salary" else round(np.random.uniform(500, 8000), 2)
    else:
        cat = np.random.choice([c for c in categories if c != "Salary"])
        amount = round(np.random.uniform(100, 12000), 2)
    rows.append((txn_dates[i], cat, types[i], amount, np.random.choice(["Cash", "UPI", "Card", "Bank Transfer"])))

df = pd.DataFrame(rows, columns=["Date", "Category", "Type", "Amount", "PaymentMethod"])
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df.to_csv("financial_transactions.csv", index=False)

income = df.loc[df["Type"] == "Income", "Amount"].sum()
expense = df.loc[df["Type"] == "Expense", "Amount"].sum()
print("Total Income:", round(income, 2))
print("Total Expenses:", round(expense, 2))
print("Net Balance:", round(income - expense, 2))

monthly = df.assign(Month=df["Date"].dt.to_period("M").astype(str)).groupby(["Month","Type"])["Amount"].sum().unstack(fill_value=0)
monthly.to_csv("monthly_financial_summary.csv")
category = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False)
category.to_csv("expense_by_category.csv", header=["TotalExpense"])

df[df["Type"]=="Income"].assign(Month=df["Date"].dt.to_period("M").astype(str)).groupby("Month")["Amount"].sum().plot(title="Monthly Income Trend")
plt.tight_layout(); plt.savefig("monthly_income_trend.png"); plt.show()
df[df["Type"]=="Expense"].assign(Month=df["Date"].dt.to_period("M").astype(str)).groupby("Month")["Amount"].sum().plot(title="Monthly Expense Trend")
plt.tight_layout(); plt.savefig("monthly_expense_trend.png"); plt.show()
category.head(8).sort_values().plot(kind="barh", title="Top Expense Categories")
plt.tight_layout(); plt.savefig("expense_by_category.png"); plt.show()
