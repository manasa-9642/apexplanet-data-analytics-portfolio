# Task 1: Data Immersion and Wrangling

## Dataset Overview

This project uses the official ApexPlanet sales dataset. The raw dataset contains 1,000 sales records and includes order details, customer information, product information, quantity, unit price, and total sales.

## Data Quality Assessment

The following data-quality issues were identified in the raw dataset:

- 20 missing values in the `Age` column
- 13 missing values in the `City` column
- 8 duplicate values in the `Order_ID` column

No missing values were found in the other columns. The `Total_Sales` values were also validated against `Quantity × Unit_Price`.

## Cleaning and Transformation

The following cleaning actions were performed:

- Removed duplicate order IDs, keeping one unique record per order
- Replaced missing age values with the median age
- Replaced missing city values with the most common city
- Removed extra spaces from text columns
- Converted `Order_Date` to date format
- Created `Order_Month` for monthly analysis
- Created `Age_Group` for customer-segment analysis
- Recalculated `Total_Sales` using quantity and unit price

## Final Dataset Summary

- Raw records: 1,000
- Cleaned records: 992
- Duplicate order IDs remaining: 0
- Missing values remaining: 0

## Data Dictionary

| Column | Meaning |
|---|---|
| `Order_ID` | Unique order identifier |
| `Order_Date` | Date on which the order was placed |
| `Customer_ID` | Unique customer identifier |
| `Customer_Name` | Customer name |
| `Age` | Customer age |
| `Gender` | Customer gender |
| `City` | Customer city |
| `Product` | Product purchased |
| `Category` | Product category |
| `Quantity` | Number of product units purchased |
| `Unit_Price` | Price per product unit |
| `Total_Sales` | Total value of the order |
| `Order_Month` | Month derived from the order date |
| `Age_Group` | Customer age segment derived from age |

## Files

- `task1_apexplanet_cleaning.py` - Python data-cleaning script
- `ApexPlanet_DataAnalytics_Dataset.xlsx` - Original raw dataset
- `apexplanet_cleaned_orders.csv` - Cleaned, analysis-ready dataset