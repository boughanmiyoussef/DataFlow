-- Total sales and revenue by product category
SELECT 
    order_category,
    product,
    COUNT(*) as total_orders,
    SUM(order_amount) as total_revenue
FROM transformed_sales_orders
GROUP BY order_category, product
ORDER BY total_revenue DESC;