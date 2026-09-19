import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("orders_cleaned.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["Revenue"] = df["Quantity"] * df["Price"]

print("Shape:", df.shape)
print("\nDescriptive statistics:")
print(df[["Quantity", "Price", "Revenue"]].describe())

print("\nRevenue by category:")
print(df.groupby("ProductCategory")["Revenue"].agg(["count", "sum", "mean"]).sort_values("sum", ascending=False))

print("\nOrder status:")
print(df["Status"].value_counts())

print("\nCountry revenue:")
print(df.groupby("Country")["Revenue"].sum().sort_values(ascending=False))

print("\nYearly revenue:")
print(df.assign(Year=df["OrderDate"].dt.year).groupby("Year")["Revenue"].sum())

# Anomaly detection using IQR
q1 = df["Revenue"].quantile(0.25)
q3 = df["Revenue"].quantile(0.75)
iqr = q3 - q1
upper = q3 + 1.5 * iqr
anomalies = df[df["Revenue"] > upper]
print("\nRevenue anomalies:")
print(anomalies[["OrderID", "ProductCategory", "Quantity", "Price", "Revenue", "Status"]])

# Charts
df.groupby("ProductCategory")["Revenue"].sum().sort_values().plot(kind="barh", title="Revenue by Product Category")
plt.tight_layout()
plt.show()

df["Status"].value_counts().plot(kind="bar", title="Order Status Distribution")
plt.tight_layout()
plt.show()

yearly = df.assign(Year=df["OrderDate"].dt.year).groupby("Year")["Revenue"].sum()
yearly.plot(kind="line", marker="o", title="Yearly Revenue Trend")
plt.tight_layout()
plt.show()

plt.scatter(df["Quantity"], df["Revenue"], alpha=0.55)
plt.xlabel("Quantity")
plt.ylabel("Revenue")
plt.title("Quantity vs Revenue")
plt.show()
