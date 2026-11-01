-- 1. Monthly Sales Trend

        SELECT Order_Month,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Order_Month
        ORDER BY Order_Month;
    

-- 2. Top 5 Products by Sales

        SELECT Product,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Product
        ORDER BY total_sales DESC
        LIMIT 5;
    

-- 3. Sales by Category

        SELECT Category,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Category
        ORDER BY total_sales DESC;
    

-- 4. Sales by City

        SELECT City,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY City
        ORDER BY total_sales DESC;
    

-- 5. Sales by Age Group

        SELECT Age_Group,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Age_Group
        ORDER BY total_sales DESC;
    

-- 6. Sales by Gender

        SELECT Gender,
               ROUND(SUM(Total_Sales), 2) AS total_sales,
               COUNT(*) AS total_orders
        FROM sales
        GROUP BY Gender
        ORDER BY total_sales DESC;
    

-- 7. Top 10 Customers by Total Sales

        SELECT Customer_ID,
               Customer_Name,
               COUNT(*) AS total_orders,
               ROUND(SUM(Total_Sales), 2) AS total_sales
        FROM sales
        GROUP BY Customer_ID, Customer_Name
        ORDER BY total_sales DESC
        LIMIT 10;
    

