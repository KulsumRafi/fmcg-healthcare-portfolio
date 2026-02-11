-- ============================================================================
-- FMCG Healthcare Analytics - SQL Analysis Queries
-- ============================================================================
-- This document contains comprehensive SQL queries for FMCG Healthcare
-- portfolio analysis covering sales, inventory, distribution, and customer insights

-- ============================================================================
-- 1. SALES PERFORMANCE ANALYSIS
-- ============================================================================

-- Query 1.1: Total Sales Revenue by Category
SELECT 
    p.category,
    COUNT(s.sale_id) as total_transactions,
    SUM(s.quantity_sold) as total_units_sold,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(s.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 2) as revenue_percentage
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Query 1.2: Monthly Sales Trend Analysis
SELECT 
    strftime('%Y-%m', s.sale_date) as month,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as units_sold,
    SUM(s.total_amount) as monthly_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_order_value,
    ROUND(AVG(s.discount_percent), 2) as avg_discount
FROM sales s
GROUP BY strftime('%Y-%m', s.sale_date)
ORDER BY month;

-- Query 1.3: Top 10 Best-Selling Products
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    COUNT(s.sale_id) as times_sold,
    SUM(s.quantity_sold) as total_quantity,
    SUM(s.total_amount) as total_revenue,
    ROUND(SUM(s.total_amount) / COUNT(s.sale_id), 2) as avg_order_value
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;

-- Query 1.4: Sales Performance by Retailer Type
SELECT 
    r.retailer_type,
    COUNT(DISTINCT r.retailer_id) as retailer_count,
    COUNT(s.sale_id) as total_transactions,
    SUM(s.quantity_sold) as total_units,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT r.retailer_id), 2) as revenue_per_retailer
FROM sales s
JOIN retailers r ON s.retailer_id = r.retailer_id
GROUP BY r.retailer_type
ORDER BY total_revenue DESC;

-- Query 1.5: Discount Impact Analysis
SELECT 
    CASE 
        WHEN discount_percent = 0 THEN 'No Discount'
        WHEN discount_percent <= 5 THEN '1-5% Discount'
        WHEN discount_percent <= 10 THEN '6-10% Discount'
        ELSE '>10% Discount'
    END as discount_range,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as units_sold,
    SUM(s.total_amount) as revenue,
    ROUND(AVG(s.quantity_sold), 2) as avg_units_per_transaction,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value
FROM sales s
GROUP BY discount_range
ORDER BY discount_percent;

-- ============================================================================
-- 2. DISTRIBUTION & RETAILER ANALYSIS
-- ============================================================================

-- Query 2.1: Sales by Region and Distributor
SELECT 
    d.region,
    d.distributor_name,
    COUNT(DISTINCT r.retailer_id) as retailer_count,
    COUNT(s.sale_id) as total_sales,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_order_value,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT r.retailer_id), 2) as revenue_per_retailer
FROM sales s
JOIN retailers r ON s.retailer_id = r.retailer_id
JOIN distributors d ON r.distributor_id = d.distributor_id
GROUP BY d.distributor_id
ORDER BY total_revenue DESC;

-- Query 2.2: Top Performing Retailers
SELECT 
    r.retailer_id,
    r.retailer_name,
    r.retailer_type,
    r.city,
    d.distributor_name,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as total_units,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_order_value,
    COUNT(DISTINCT s.product_id) as unique_products_sold
FROM sales s
JOIN retailers r ON s.retailer_id = r.retailer_id
LEFT JOIN distributors d ON r.distributor_id = d.distributor_id
GROUP BY r.retailer_id
ORDER BY total_revenue DESC
LIMIT 15;

-- Query 2.3: Regional Sales Distribution
SELECT 
    r.state,
    COUNT(DISTINCT r.retailer_id) as retailer_count,
    COUNT(s.sale_id) as total_transactions,
    SUM(s.quantity_sold) as total_units,
    SUM(s.total_amount) as total_revenue,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT r.retailer_id), 2) as revenue_per_retailer,
    ROUND(SUM(s.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 2) as market_share_percentage
FROM sales s
JOIN retailers r ON s.retailer_id = r.retailer_id
GROUP BY r.state
ORDER BY total_revenue DESC;

-- Query 2.4: Retailer Performance Comparison
SELECT 
    r.retailer_name,
    r.retailer_type,
    COUNT(s.sale_id) as sales_count,
    SUM(s.quantity_sold) as units_sold,
    SUM(s.total_amount) as revenue,
    ROUND(SUM(s.total_amount) / COUNT(s.sale_id), 2) as avg_order_value,
    ROUND(COUNT(s.sale_id) / 
        (SELECT COUNT(DISTINCT sale_date) FROM sales WHERE retailer_id = r.retailer_id), 2) as sales_per_day,
    COUNT(DISTINCT s.product_id) as product_variety
FROM sales s
JOIN retailers r ON s.retailer_id = r.retailer_id
GROUP BY r.retailer_id
ORDER BY revenue DESC;

-- ============================================================================
-- 3. INVENTORY MANAGEMENT
-- ============================================================================

-- Query 3.1: Current Inventory Status
SELECT 
    p.product_name,
    p.category,
    COUNT(i.inventory_id) as retailer_locations,
    SUM(i.stock_quantity) as total_stock,
    ROUND(AVG(i.stock_quantity), 2) as avg_stock_per_location,
    MIN(i.stock_quantity) as min_stock,
    MAX(i.stock_quantity) as max_stock,
    COUNT(CASE WHEN i.stock_quantity < i.reorder_level THEN 1 END) as locations_below_reorder
FROM inventory i
JOIN products p ON i.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_stock DESC;

-- Query 3.2: Low Stock Alert - Products Below Reorder Level
SELECT 
    i.inventory_id,
    p.product_name,
    p.category,
    r.retailer_name,
    r.city,
    i.stock_quantity,
    i.reorder_level,
    (i.reorder_level - i.stock_quantity) as units_needed,
    p.unit_price,
    ROUND((i.reorder_level - i.stock_quantity) * p.unit_price, 2) as reorder_cost
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN retailers r ON i.retailer_id = r.retailer_id
WHERE i.stock_quantity < i.reorder_level
ORDER BY units_needed DESC;

-- Query 3.3: Inventory Turnover Analysis
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(s.quantity_sold) as total_sold,
    SUM(i.stock_quantity) as current_stock,
    ROUND(SUM(s.quantity_sold) / NULLIF(SUM(i.stock_quantity), 0), 2) as turnover_ratio,
    ROUND(SUM(s.total_amount), 2) as revenue_generated
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
LEFT JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id
ORDER BY turnover_ratio DESC;

-- Query 3.4: Inventory Value by Retailer
SELECT 
    r.retailer_name,
    r.retailer_type,
    r.city,
    COUNT(i.inventory_id) as product_count,
    SUM(i.stock_quantity) as total_units,
    ROUND(SUM(i.stock_quantity * p.unit_price), 2) as inventory_value,
    ROUND(AVG(i.stock_quantity), 2) as avg_units_per_product
FROM inventory i
JOIN retailers r ON i.retailer_id = r.retailer_id
JOIN products p ON i.product_id = p.product_id
GROUP BY r.retailer_id
ORDER BY inventory_value DESC;

-- ============================================================================
-- 4. CUSTOMER ANALYSIS
-- ============================================================================

-- Query 4.1: Customer Purchase Behavior by Demographics
SELECT 
    cd.age_group,
    cd.income_level,
    COUNT(DISTINCT cd.customer_id) as customer_count,
    COUNT(sbc.transaction_id) as total_purchases,
    SUM(sbc.quantity) as total_units_purchased,
    ROUND(COUNT(sbc.transaction_id) / COUNT(DISTINCT cd.customer_id), 2) as avg_purchases_per_customer,
    ROUND(SUM(sbc.quantity) / COUNT(sbc.transaction_id), 2) as avg_units_per_purchase
FROM customer_demographics cd
LEFT JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
GROUP BY cd.age_group, cd.income_level
ORDER BY total_purchases DESC;

-- Query 4.2: Health Condition Impact on Product Preferences
SELECT 
    cd.health_condition,
    p.category,
    COUNT(DISTINCT cd.customer_id) as customer_count,
    COUNT(sbc.transaction_id) as purchase_count,
    SUM(sbc.quantity) as total_quantity,
    ROUND(COUNT(sbc.transaction_id) / COUNT(DISTINCT cd.customer_id), 2) as avg_purchases_per_customer
FROM customer_demographics cd
JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
JOIN products p ON sbc.product_id = p.product_id
WHERE cd.health_condition != 'None'
GROUP BY cd.health_condition, p.category
ORDER BY purchase_count DESC;

-- Query 4.3: Geographic Customer Distribution
SELECT 
    cd.city,
    COUNT(DISTINCT cd.customer_id) as customer_count,
    COUNT(sbc.transaction_id) as total_transactions,
    SUM(sbc.quantity) as total_units_purchased,
    ROUND(COUNT(sbc.transaction_id) / COUNT(DISTINCT cd.customer_id), 2) as avg_transactions_per_customer,
    COUNT(DISTINCT sbc.product_id) as unique_products_purchased
FROM customer_demographics cd
LEFT JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
GROUP BY cd.city
ORDER BY total_transactions DESC;

-- Query 4.4: Customer Segmentation by Purchase Value
SELECT 
    CASE 
        WHEN purchase_count >= 10 THEN 'High-Value'
        WHEN purchase_count >= 5 THEN 'Medium-Value'
        ELSE 'Low-Value'
    END as customer_segment,
    COUNT(DISTINCT customer_id) as customer_count,
    ROUND(AVG(purchase_count), 2) as avg_purchases,
    ROUND(AVG(total_quantity), 2) as avg_units_purchased,
    MIN(purchase_count) as min_purchases,
    MAX(purchase_count) as max_purchases
FROM (
    SELECT 
        cd.customer_id,
        COUNT(sbc.transaction_id) as purchase_count,
        SUM(sbc.quantity) as total_quantity
    FROM customer_demographics cd
    LEFT JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
    GROUP BY cd.customer_id
)
GROUP BY customer_segment;

-- ============================================================================
-- 5. MANUFACTURER & PRODUCT ANALYSIS
-- ============================================================================

-- Query 5.1: Manufacturer Performance
SELECT 
    m.manufacturer_name,
    m.country,
    COUNT(DISTINCT p.product_id) as product_count,
    COUNT(s.sale_id) as total_sales,
    SUM(s.quantity_sold) as total_units,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_order_value,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT p.product_id), 2) as revenue_per_product
FROM manufacturers m
LEFT JOIN products p ON m.manufacturer_id = p.manufacturer_id
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY m.manufacturer_id
ORDER BY total_revenue DESC;

-- Query 5.2: Product Category Performance Comparison
SELECT 
    p.category,
    p.subcategory,
    COUNT(DISTINCT p.product_id) as product_count,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as total_quantity,
    SUM(s.total_amount) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT p.product_id), 2) as revenue_per_product,
    ROUND(SUM(s.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 2) as market_share
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category, p.subcategory
ORDER BY total_revenue DESC;

-- Query 5.3: Price Elasticity Analysis
SELECT 
    p.product_name,
    p.unit_price,
    COUNT(s.sale_id) as sales_count,
    SUM(s.quantity_sold) as total_quantity,
    ROUND(SUM(s.total_amount), 2) as total_revenue,
    ROUND(SUM(s.quantity_sold) / COUNT(s.sale_id), 2) as avg_quantity_per_sale,
    ROUND(SUM(s.total_amount) / SUM(s.quantity_sold), 2) as effective_price
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id
ORDER BY unit_price DESC;

-- ============================================================================
-- 6. ADVANCED ANALYTICS & INSIGHTS
-- ============================================================================

-- Query 6.1: Year-over-Year Growth Analysis
SELECT 
    strftime('%Y', s.sale_date) as year,
    strftime('%m', s.sale_date) as month,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as units_sold,
    SUM(s.total_amount) as monthly_revenue,
    ROUND(SUM(s.total_amount) / COUNT(s.sale_id), 2) as avg_order_value
FROM sales s
GROUP BY year, month
ORDER BY year DESC, month DESC;

-- Query 6.2: Cross-Selling Opportunities
SELECT 
    p1.product_name as product_a,
    p2.product_name as product_b,
    p1.category as category_a,
    p2.category as category_b,
    COUNT(DISTINCT sbc1.customer_id) as customers_bought_both,
    ROUND(COUNT(DISTINCT sbc1.customer_id) * 100.0 / 
        (SELECT COUNT(DISTINCT customer_id) FROM sales_by_customer), 2) as penetration_percentage
FROM sales_by_customer sbc1
JOIN sales_by_customer sbc2 ON sbc1.customer_id = sbc2.customer_id 
    AND sbc1.product_id < sbc2.product_id
    AND sbc1.purchase_date <= sbc2.purchase_date
JOIN products p1 ON sbc1.product_id = p1.product_id
JOIN products p2 ON sbc2.product_id = p2.product_id
WHERE p1.category != p2.category
GROUP BY sbc1.product_id, sbc2.product_id
HAVING COUNT(DISTINCT sbc1.customer_id) >= 5
ORDER BY customers_bought_both DESC
LIMIT 20;

-- Query 6.3: Seasonal Trends Analysis
SELECT 
    CASE 
        WHEN strftime('%m', s.sale_date) IN ('01', '02', '03') THEN 'Q1'
        WHEN strftime('%m', s.sale_date) IN ('04', '05', '06') THEN 'Q2'
        WHEN strftime('%m', s.sale_date) IN ('07', '08', '09') THEN 'Q3'
        ELSE 'Q4'
    END as quarter,
    p.category,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as units_sold,
    SUM(s.total_amount) as revenue,
    ROUND(AVG(s.total_amount), 2) as avg_order_value
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY quarter, p.category
ORDER BY quarter, revenue DESC;

-- Query 6.4: Customer Lifetime Value Estimation
SELECT 
    cd.customer_id,
    cd.age_group,
    cd.income_level,
    cd.health_condition,
    COUNT(sbc.transaction_id) as lifetime_purchases,
    SUM(sbc.quantity) as lifetime_units,
    ROUND(SUM(sbc.quantity * p.unit_price), 2) as estimated_lifetime_value,
    MIN(sbc.purchase_date) as first_purchase_date,
    MAX(sbc.purchase_date) as last_purchase_date,
    ROUND(
        (julianday(MAX(sbc.purchase_date)) - julianday(MIN(sbc.purchase_date))) / 
        NULLIF(COUNT(sbc.transaction_id) - 1, 0), 2
    ) as avg_days_between_purchases
FROM customer_demographics cd
LEFT JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
LEFT JOIN products p ON sbc.product_id = p.product_id
WHERE sbc.transaction_id IS NOT NULL
GROUP BY cd.customer_id
ORDER BY estimated_lifetime_value DESC;

-- Query 6.5: Market Basket Analysis - Average Basket Size
SELECT 
    strftime('%Y-%m', s.sale_date) as month,
    ROUND(AVG(s.quantity_sold), 2) as avg_units_per_transaction,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
    COUNT(s.sale_id) as transaction_count,
    SUM(s.quantity_sold) as total_units,
    SUM(s.total_amount) as total_revenue,
    ROUND(SUM(s.total_amount) / COUNT(s.sale_id), 2) as revenue_per_transaction
FROM sales s
GROUP BY month
ORDER BY month DESC;

-- ============================================================================
-- 7. PERFORMANCE METRICS & KPIs
-- ============================================================================

-- Query 7.1: Overall Business KPIs
SELECT 
    COUNT(DISTINCT s.sale_id) as total_transactions,
    SUM(s.quantity_sold) as total_units_sold,
    ROUND(SUM(s.total_amount), 2) as total_revenue,
    ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
    ROUND(SUM(s.total_amount) / COUNT(DISTINCT s.sale_id), 2) as revenue_per_transaction,
    COUNT(DISTINCT s.retailer_id) as active_retailers,
    COUNT(DISTINCT s.product_id) as products_sold,
    ROUND(SUM(s.discount_percent * s.total_amount) / SUM(s.total_amount), 2) as avg_discount_rate
FROM sales s;

-- Query 7.2: Retailer Efficiency Metrics
SELECT 
    r.retailer_name,
    ROUND(
        (SELECT SUM(s.total_amount) FROM sales s WHERE s.retailer_id = r.retailer_id) / 
        (SELECT COUNT(DISTINCT sale_date) FROM sales s WHERE s.retailer_id = r.retailer_id), 2
    ) as revenue_per_day,
    ROUND(
        (SELECT COUNT(s.sale_id) FROM sales s WHERE s.retailer_id = r.retailer_id) / 
        (SELECT COUNT(DISTINCT sale_date) FROM sales s WHERE s.retailer_id = r.retailer_id), 2
    ) as transactions_per_day,
    ROUND(
        (SELECT AVG(s.quantity_sold) FROM sales s WHERE s.retailer_id = r.retailer_id), 2
    ) as avg_units_per_transaction,
    (SELECT COUNT(DISTINCT product_id) FROM sales s WHERE s.retailer_id = r.retailer_id) as unique_products_sold
FROM retailers r
ORDER BY revenue_per_day DESC;

-- Query 7.3: Product Performance Scorecard
SELECT 
    p.product_name,
    p.category,
    ROUND(
        (SELECT SUM(s.total_amount) FROM sales s WHERE s.product_id = p.product_id) / 
        (SELECT SUM(total_amount) FROM sales) * 100, 2
    ) as revenue_contribution_percent,
    (SELECT COUNT(DISTINCT retailer_id) FROM sales s WHERE s.product_id = p.product_id) as retailer_reach,
    (SELECT COUNT(DISTINCT customer_id) FROM sales_by_customer sbc WHERE sbc.product_id = p.product_id) as unique_customers,
    ROUND((SELECT AVG(total_amount) FROM sales s WHERE s.product_id = p.product_id), 2) as avg_order_value,
    (SELECT SUM(i.stock_quantity) FROM inventory i WHERE i.product_id = p.product_id) as current_stock
FROM products p
ORDER BY revenue_contribution_percent DESC;
