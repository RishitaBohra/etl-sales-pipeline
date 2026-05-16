USE salesdb;

SELECT * FROM sales_data;

SELECT Region, SUM(TotalSales) AS Total_Revenue
FROM sales_data
GROUP BY Region;

SELECT Product, TotalSales
FROM sales_data
ORDER BY TotalSales DESC;