import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load official cleaned data
df = pd.read_csv("../data/apexplanet_cleaned_orders.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# KPI values
total_orders = len(df)
total_sales = df["Total_Sales"].sum()
average_order_value = df["Total_Sales"].mean()

category_sales = df.groupby("Category")["Total_Sales"].sum().sort_values()
city_sales = df.groupby("City")["Total_Sales"].sum().sort_values()
age_group_sales = df.groupby(
    "Age_Group", observed=False
)["Total_Sales"].sum()

top_city = city_sales.idxmax()

monthly_sales = df.groupby("Order_Month")["Total_Sales"].sum()

# Dashboard layout
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.subplots_adjust(top=0.72, hspace=0.45, wspace=0.30)

fig.suptitle(
    "ApexPlanet Sales Dashboard - Task 2",
    fontsize=22,
    fontweight="bold",
    color="#0F766E"
)

card_style = dict(
    boxstyle="round,pad=0.7",
    facecolor="#D1FAE5",
    edgecolor="#0F766E"
)

fig.text(
    0.15, 0.84, f"Total Orders\n{total_orders:,}",
    ha="center", va="center", fontsize=14,
    fontweight="bold", bbox=card_style
)

fig.text(
    0.37, 0.84, f"Total Sales\nINR {total_sales:,.0f}",
    ha="center", va="center", fontsize=14,
    fontweight="bold", bbox=card_style
)

fig.text(
    0.62, 0.84, f"Average Order Value\nINR {average_order_value:,.0f}",
    ha="center", va="center", fontsize=14,
    fontweight="bold", bbox=card_style
)

fig.text(
    0.84, 0.84, f"Top City\n{top_city}",
    ha="center", va="center", fontsize=14,
    fontweight="bold", bbox=card_style
)

# Monthly sales trend
axes[0, 0].plot(
    monthly_sales.index, monthly_sales.values,
    marker="o", color="#0F766E"
)
axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Total Sales")
axes[0, 0].tick_params(axis="x", rotation=45)

# Sales by category
axes[0, 1].barh(
    category_sales.index, category_sales.values,
    color="#2563EB"
)
axes[0, 1].set_title("Sales by Category")
axes[0, 1].set_xlabel("Total Sales")

# Sales by city
axes[1, 0].bar(
    city_sales.index, city_sales.values,
    color="#EA580C"
)
axes[1, 0].set_title("Sales by City")
axes[1, 0].set_xlabel("City")
axes[1, 0].set_ylabel("Total Sales")
axes[1, 0].tick_params(axis="x", rotation=30)

# Sales by age group
axes[1, 1].bar(
    age_group_sales.index.astype(str),
    age_group_sales.values,
    color="#7C3AED"
)
axes[1, 1].set_title("Sales by Age Group")
axes[1, 1].set_xlabel("Age Group")
axes[1, 1].set_ylabel("Total Sales")

# Save dashboard
plt.savefig(
    "../reports/task2_apexplanet/task2_apexplanet_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

print("Task 2 dashboard created successfully.")