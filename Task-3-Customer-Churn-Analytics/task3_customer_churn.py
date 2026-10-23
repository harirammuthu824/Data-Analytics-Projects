# Task 3: Customer Churn Analytics
# Synthetic sample data demonstration. Replace with official data if provided.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "CustomerID": range(1001, 1001+n),
    "Gender": np.random.choice(["Male", "Female"], n),
    "Tenure": np.random.randint(1, 73, n),
    "MonthlyCharges": np.random.randint(20, 121, n),
    "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.25, 0.20]),
    "InternetService": np.random.choice(["DSL", "Fiber optic", "No internet"], n)
})
prob = np.where(df["Contract"] == "Month-to-month", 0.40, 0.12)
prob += np.where(df["Tenure"] < 12, 0.15, 0)
prob = np.clip(prob, 0.05, 0.85)
df["Churn"] = np.where(np.random.random(n) < prob, "Yes", "No")

contract_churn = pd.crosstab(df["Contract"], df["Churn"], normalize="index") * 100
print("Total customers:", len(df))
print("Churned customers:", int((df["Churn"] == "Yes").sum()))
print(f"Churn rate: {(df['Churn'] == 'Yes').mean()*100:.2f}%")
print("\nChurn by contract (%):\n", contract_churn.round(2))

df.to_csv("customer_churn_analysis.csv", index=False)
contract_churn.to_csv("churn_by_contract.csv")

df["Churn"].value_counts().reindex(["No", "Yes"]).plot(kind="bar", title="Customer Churn Distribution")
plt.xlabel("Churn"); plt.ylabel("Customers"); plt.tight_layout(); plt.savefig("churn_distribution.png"); plt.show()
contract_churn["Yes"].sort_values(ascending=False).plot(kind="bar", title="Churn Rate by Contract Type")
plt.xlabel("Contract Type"); plt.ylabel("Churn Rate (%)"); plt.tight_layout(); plt.savefig("churn_by_contract.png"); plt.show()
df.groupby("Churn")["MonthlyCharges"].mean().reindex(["No", "Yes"]).plot(kind="bar", title="Average Monthly Charges by Churn")
plt.xlabel("Churn"); plt.ylabel("Average Monthly Charges"); plt.tight_layout(); plt.savefig("charges_by_churn.png"); plt.show()
