import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create folders for Task 2 outputs
output_folder = "../reports/task2_apexplanet"
chart_folder = "../reports/task2_apexplanet/charts"

os.makedirs(chart_folder, exist_ok=True)

# Load the official cleaned dataset
df = pd.read_csv("../data/apexplanet_cleaned_orders.csv")

# Prepare dates
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# Chart style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Monthly sales trend
monthly_sales = df.groupby("Order_Month")["Total_Sales"].sum()

plt.plot(monthly_sales.index, monthly_sales.values,
         marker="o", color="#0F766E")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{chart_folder}/monthly_sales_trend.png")
plt.close()

# 2. Sales by category
category_sales = df.groupby("Category")["Total_Sales"].sum().sort_values()

category_sales.plot(kind="barh", color="#2563EB")
plt.title("Total Sales by Category")
plt.xlabel("Total Sales")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(f"{chart_folder}/sales_by_category.png")
plt.close()

# 3. Top 10 products by sales
product_sales = (
    df.groupby("Product")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

product_sales.sort_values().plot(kind="barh", color="#7C3AED")
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(f"{chart_folder}/top_products.png")
plt.close()

# 4. Sales by city
city_sales = (
    df.groupby("City")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

city_sales.plot(kind="bar", color="#EA580C")
plt.title("Total Sales by City")
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{chart_folder}/sales_by_city.png")
plt.close()

# 5. Sales by age group
age_group_sales = (
    df.groupby("Age_Group", observed=False)["Total_Sales"]
    .sum()
)

age_group_sales.plot(kind="bar", color="#059669")
plt.title("Total Sales by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{chart_folder}/sales_by_age_group.png")
plt.close()

# 6. Correlation heatmap
numeric_columns = ["Age", "Quantity", "Unit_Price", "Total_Sales"]

plt.figure(figsize=(8, 6))
sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap="YlGnBu",
    fmt=".2f"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{chart_folder}/correlation_heatmap.png")
plt.close()

# Summary statistics
total_orders = len(df)
total_sales = df["Total_Sales"].sum()
average_order_value = df["Total_Sales"].mean()
top_category = category_sales.idxmax()
top_product = product_sales.idxmax()
top_city = city_sales.idxmax()

summary = f"""
TASK 2 - EXPLORATORY DATA ANALYSIS SUMMARY

Total Orders: {total_orders}
Total Sales: INR {total_sales:,.2f}
Average Order Value: INR {average_order_value:,.2f}

Top Category by Sales: {top_category}
Top Product by Sales: {top_product}
Top City by Sales: {top_city}
"""

with open(f"{output_folder}/eda_summary.txt", "w") as file:
    file.write(summary)

print(summary)
print("EDA charts and summary were saved successfully.")