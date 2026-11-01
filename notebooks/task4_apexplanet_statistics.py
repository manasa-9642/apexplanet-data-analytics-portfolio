import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

print("APEXPLANET TASK 4 - STATISTICAL ANALYSIS")
print("=" * 55)

# 1. LOAD DATASET
data_folder = Path("../data")
files = list(data_folder.rglob("ApexPlanet_DataAnalytics_Dataset.xlsx"))

if not files:
    files = list(data_folder.rglob("*.xlsx"))

if not files:
    raise FileNotFoundError("Excel dataset not found in data folder.")

df = pd.read_excel(files[0])

print("\n1. DATASET INFORMATION")
print("Total records:", len(df))
print("Columns:", df.columns.tolist())

# 2. DATA CLEANING
df["Total_Sales"] = pd.to_numeric(
    df["Total_Sales"], errors="coerce"
)

df = df.dropna(subset=["Gender", "Total_Sales"])

print("\n2. DATA QUALITY")
print("Missing values:")
print(df.isnull().sum())
print("Duplicate records:", df.duplicated().sum())

# 3. BUSINESS INSIGHTS
print("\n3. BUSINESS INSIGHTS")

print("Total Sales:", round(df["Total_Sales"].sum(), 2))

category_sales = df.groupby(
    "Category"
)["Total_Sales"].sum().sort_values(ascending=False)

city_sales = df.groupby(
    "City"
)["Total_Sales"].sum().sort_values(ascending=False)

print("\nSales by Category:")
print(category_sales)

print("\nSales by City:")
print(city_sales)

# 4. HYPOTHESIS TESTING
print("\n4. HYPOTHESIS TESTING")

female = df.loc[
    df["Gender"] == "Female", "Total_Sales"
].dropna()

male = df.loc[
    df["Gender"] == "Male", "Total_Sales"
].dropna()

print("Female orders:", len(female))
print("Male orders:", len(male))

print("Female mean sales:", round(female.mean(), 2))
print("Male mean sales:", round(male.mean(), 2))

# Null Hypothesis:
# There is no difference in average sales
# between male and female orders.

# Alternative Hypothesis:
# There is a difference in average sales.

t_stat, p_value = stats.ttest_ind(
    male, female, equal_var=False
)

print("\nWelch's Independent T-Test")
print("T-statistic:", round(t_stat, 4))
print("P-value:", round(p_value, 4))

if p_value < 0.05:
    print("Result: Reject the Null Hypothesis")
    print("The difference is statistically significant.")
else:
    print("Result: Fail to Reject the Null Hypothesis")
    print("The difference is not statistically significant.")

# 5. VISUALIZATION
print("\n5. CREATING CHARTS")

plt.figure(figsize=(9, 5))
category_sales.plot(kind="bar")
plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Sales (INR)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("../reports/task4_category_sales.png")
plt.show()

plt.figure(figsize=(9, 5))
city_sales.plot(kind="bar")
plt.title("Sales by City")
plt.xlabel("City")
plt.ylabel("Total Sales (INR)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("../reports/task4_city_sales.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.boxplot([female, male], labels=["Female", "Male"])
plt.title("Sales Distribution by Gender")
plt.ylabel("Total Sales (INR)")
plt.tight_layout()
plt.savefig("../reports/task4_gender_comparison.png")
plt.show()

print("\nTASK 4 ANALYSIS COMPLETED SUCCESSFULLY!")