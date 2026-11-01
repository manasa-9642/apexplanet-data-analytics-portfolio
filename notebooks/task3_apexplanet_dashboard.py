import pandas as pd
import plotly.express as px
import streamlit as st

# Page setup
st.set_page_config(
    page_title="ApexPlanet Customer Segmentation Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("../data/apexplanet_cleaned_orders.csv")
customers = pd.read_csv("../data/apexplanet_customer_segments.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# Add customer segment to every order
df = df.merge(
    customers[["Customer_ID", "Segment"]],
    on="Customer_ID",
    how="left"
)

# Title
st.title("ApexPlanet Customer Segmentation Dashboard")
st.caption("Task 3: Deep-Dive Customer Analysis and Interactive Dashboard")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

# Apply filters
filtered_df = df[
    (df["City"].isin(cities)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments))
].copy()

# KPI calculations
total_sales = filtered_df["Total_Sales"].sum()
total_orders = len(filtered_df)
total_customers = filtered_df["Customer_ID"].nunique()
average_order_value = filtered_df["Total_Sales"].mean()
average_quantity = filtered_df["Quantity"].mean()

# KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"INR {total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")
col4.metric("Average Order Value", f"INR {average_order_value:,.0f}")
col5.metric("Average Quantity", f"{average_quantity:.1f}")

st.divider()

# Monthly sales chart
monthly_sales = (
    filtered_df.groupby("Order_Month")["Total_Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order_Month",
    y="Total_Sales",
    markers=True,
    title="Monthly Sales Trend"
)
fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Total Sales (INR)")

# Sales by category
category_sales = (
    filtered_df.groupby("Category")["Total_Sales"]
    .sum()
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Total_Sales",
    color="Category",
    title="Sales by Category"
)
fig_category.update_layout(showlegend=False, xaxis_title="Category",
                           yaxis_title="Total Sales (INR)")

# Sales by city
city_sales = (
    filtered_df.groupby("City")["Total_Sales"]
    .sum()
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

fig_city = px.bar(
    city_sales,
    x="City",
    y="Total_Sales",
    color="City",
    title="Sales by City"
)
fig_city.update_layout(showlegend=False, xaxis_title="City",
                       yaxis_title="Total Sales (INR)")

# Sales by segment
segment_sales = (
    filtered_df.groupby("Segment")["Total_Sales"]
    .sum()
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

fig_segment = px.bar(
    segment_sales,
    x="Segment",
    y="Total_Sales",
    color="Segment",
    title="Sales by Customer Segment"
)
fig_segment.update_layout(showlegend=False, xaxis_title="Customer Segment",
                          yaxis_title="Total Sales (INR)")

# Dashboard layout
left_column, right_column = st.columns(2)

with left_column:
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.plotly_chart(fig_city, use_container_width=True)

with right_column:
    st.plotly_chart(fig_category, use_container_width=True)
    st.plotly_chart(fig_segment, use_container_width=True)

# Data table
st.subheader("Filtered Sales Records")
st.dataframe(
    filtered_df[
        [
            "Order_ID", "Order_Date", "Customer_ID", "City",
            "Product", "Category", "Quantity", "Total_Sales", "Segment"
        ]
    ],
    use_container_width=True
)