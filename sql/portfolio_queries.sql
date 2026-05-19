-- 1. Monthly revenue and profit
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(net_revenue) AS net_revenue,
    SUM(profit) AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(net_revenue), 0) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY 1
ORDER BY 1;

-- 2. Category performance
SELECT
    category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    SUM(net_revenue) AS net_revenue,
    SUM(profit) AS profit,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct
FROM orders
GROUP BY category
ORDER BY net_revenue DESC;

-- 3. Sales channel performance
SELECT
    sales_channel,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(net_revenue) AS net_revenue,
    SUM(profit) AS profit,
    ROUND(SUM(net_revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS revenue_per_order
FROM orders
GROUP BY sales_channel
ORDER BY net_revenue DESC;

-- 4. Returning customers
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS orders,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order,
    SUM(net_revenue) AS net_revenue,
    SUM(profit) AS profit
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY net_revenue DESC;
