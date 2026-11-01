import pandas as pd

# Read the official raw ApexPlanet dataset
df = pd.read_excel(
    "../data/ApexPlanet_DataAnalytics_Dataset.xlsx",
    sheet_name="Sales_Dataset"
)

print("Original rows:", len(df))
print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate Order IDs:", df["Order_ID"].duplicated().sum())

# Remove duplicate Order IDs
df = df.drop_duplicates(subset="Order_ID", keep="first").copy()

# Fill missing Age values with the median
df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill missing City values with the most common city
df["City"] = df["City"].fillna(df["City"].mode()[0])

# Remove extra spaces from text columns
text_columns = [
    "Order_ID", "Customer_ID", "Customer_Name",
    "Gender", "City", "Product", "Category"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# Convert order dates and create a month column
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# Create age groups for later analysis
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[17, 25, 35, 45, 55, 65],
    labels=["18-25", "26-35", "36-45", "46-55", "56-65"]
)

# Validate total sales
df["Total_Sales"] = (df["Quantity"] * df["Unit_Price"]).round(2)

# Save a separate cleaned dataset
df.to_csv("../data/apexplanet_cleaned_orders.csv", index=False)

print("\nCleaned rows:", len(df))
print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDuplicate Order IDs after cleaning:",
      df["Order_ID"].duplicated().sum())

print("\nCleaned dataset saved successfully.")