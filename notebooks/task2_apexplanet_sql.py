import os
import sqlite3
import pandas as pd

# Output folder
output_folder = "../reports/task2_apexplanet"
os.makedirs(output_folder, exist_ok=True)

# Load official cleaned data
df = pd.read_csv("../data/apexplanet_cleaned_orders.csv")

# Create temporary SQLite database
connection = sqlite3.connect(":memory:")
df.to_sql("sales", connection, index=False, if_exists="replace")

# Business questions and SQL queries
queries = {
    "1. Monthly Sales Trend": """
        SELECT Order_Month,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Order_Month
        ORDER BY Order_Month;
    """,

    "2. Top 5 Products by Sales": """
        SELECT Product,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Product
        ORDER BY total_sales DESC
        LIMIT 5;
    """,

    "3. Sales by Category": """
        SELECT Category,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Category
        ORDER BY total_sales DESC;
    """,

    "4. Sales by City": """
        SELECT City,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY City
        ORDER BY total_sales DESC;
    """,

    "5. Sales by Age Group": """
        SELECT Age_Group,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Age_Group
        ORDER BY total_sales DESC;
    """,

    "6. Sales by Gender": """
        SELECT Gender,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Gender
        ORDER BY total_sales DESC;
    """,

    "7. Top 10 Customers by Total Sales": """
        SELECT Customer_ID,
               Customer_Name,
               COUNT(*) AS total_orders,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Customer_ID, Customer_Name
        ORDER BY total_sales DESC
        LIMIT 10;
    """
}

# Save SQL queries and results
sql_file = f"{output_folder}/task2_apexplanet_sql_queries.sql"
result_file = f"{output_folder}/task2_apexplanet_sql_results.txt"

with open(sql_file, "w") as sql_output, open(result_file, "w") as result_output:
    for title, query in queries.items():
        result = pd.read_sql_query(query, connection)

        sql_output.write(f"-- {title}\n{query}\n\n")

        result_output.write(f"\n{'=' * 60}\n")
        result_output.write(f"{title}\n")
        result_output.write(f"{'=' * 60}\n")
        result_output.write(query)
        result_output.write("\nRESULT:\n")
        result_output.write(result.to_string(index=False))
        result_output.write("\n\n")

        print(title)
        print(result)
        print()

connection.close()

print("SQL queries and results were saved successfully.")