import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Create Task 3 output folders
output_folder = "../reports/task3_apexplanet"
chart_folder = "../reports/task3_apexplanet/charts"
os.makedirs(chart_folder, exist_ok=True)

# Load the cleaned official ApexPlanet dataset
df = pd.read_csv("../data/apexplanet_cleaned_orders.csv")

# Create a customer-level table
customers = (
    df.groupby("Customer_ID")
    .agg(
        Customer_Name=("Customer_Name", "first"),
        Age=("Age", "mean"),
        City=("City", "first"),
        Order_Count=("Order_ID", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Total_Sales", "sum"),
        Average_Order_Value=("Total_Sales", "mean")
    )
    .reset_index()
)

# Select features for customer segmentation
features = ["Total_Sales", "Order_Count", "Total_Quantity", "Age"]

# Standardize data before clustering
scaler = StandardScaler()
scaled_features = scaler.fit_transform(customers[features])

# Create three customer segments
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
customers["Cluster"] = kmeans.fit_predict(scaled_features)

# Give meaningful names to clusters based on average total sales
cluster_order = (
    customers.groupby("Cluster")["Total_Sales"]
    .mean()
    .sort_values()
    .index
    .tolist()
)

segment_names = {
    cluster_order[0]: "Low-Value Customers",
    cluster_order[1]: "Medium-Value Customers",
    cluster_order[2]: "High-Value Customers"
}

customers["Segment"] = customers["Cluster"].map(segment_names)

# Save segmented customer data
customers.to_csv(
    "../data/apexplanet_customer_segments.csv",
    index=False
)

# Segment summary
segment_summary = (
    customers.groupby("Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Sales=("Total_Sales", "sum"),
        Average_Sales=("Total_Sales", "mean"),
        Average_Quantity=("Total_Quantity", "mean"),
        Average_Age=("Age", "mean")
    )
    .round(2)
    .reset_index()
)

segment_summary.to_csv(
    f"{output_folder}/segment_summary.csv",
    index=False
)

# Chart 1: Customer count by segment
sns.set_theme(style="whitegrid")

plt.figure(figsize=(9, 6))
sns.barplot(
    data=segment_summary,
    x="Segment",
    y="Customers",
    hue="Segment",
    palette="viridis",
    legend=False
)
plt.title("Number of Customers by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig(f"{chart_folder}/customers_by_segment.png")
plt.close()

# Chart 2: Sales by segment
plt.figure(figsize=(9, 6))
sns.barplot(
    data=segment_summary,
    x="Segment",
    y="Total_Sales",
    hue="Segment",
    palette="magma",
    legend=False
)
plt.title("Total Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Sales (INR)")
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig(f"{chart_folder}/sales_by_segment.png")
plt.close()

# Chart 3: Customer segmentation scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=customers,
    x="Age",
    y="Total_Sales",
    hue="Segment",
    palette="Set2",
    s=80
)
plt.title("Customer Segmentation by Age and Total Sales")
plt.xlabel("Customer Age")
plt.ylabel("Total Sales (INR)")
plt.tight_layout()
plt.savefig(f"{chart_folder}/customer_segments_scatter.png")
plt.close()

# Write summary
total_customers = len(customers)
highest_segment = segment_summary.loc[
    segment_summary["Total_Sales"].idxmax(), "Segment"
]

summary = f"""
TASK 3 - CUSTOMER SEGMENTATION SUMMARY

Total Customers: {total_customers}
Number of Segments: 3
Highest Sales Segment: {highest_segment}

SEGMENT SUMMARY:
{segment_summary.to_string(index=False)}
"""

with open(f"{output_folder}/task3_segmentation_summary.txt", "w") as file:
    file.write(summary)

print(summary)
print("\nCustomer segments, charts, and summary were saved successfully.")