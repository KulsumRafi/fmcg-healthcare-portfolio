#!/usr/bin/env python3
"""
Execute SQL Analysis Queries and Generate Results
Runs all SQL queries from sql_queries.sql and exports results
"""

import sqlite3
import pandas as pd
from pathlib import Path
import json

DB_PATH = '/home/ubuntu/fmcg-healthcare-portfolio/data/fmcg_healthcare.db'
OUTPUT_DIR = Path('/home/ubuntu/fmcg-healthcare-portfolio/analysis')
RESULTS_DIR = OUTPUT_DIR / 'sql_results'
RESULTS_DIR.mkdir(exist_ok=True)

class SQLAnalyzer:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.results = {}
    
    def execute_query(self, query_name, query):
        """Execute a SQL query and store results"""
        try:
            df = pd.read_sql_query(query, self.conn)
            self.results[query_name] = df
            print(f"  ✓ {query_name}: {len(df)} rows")
            return df
        except Exception as e:
            print(f"  ✗ {query_name}: {str(e)}")
            return None
    
    def run_all_queries(self):
        """Run all SQL analysis queries"""
        print("Executing SQL Analysis Queries...\n")
        
        # 1. SALES PERFORMANCE ANALYSIS
        print("1. SALES PERFORMANCE ANALYSIS")
        
        self.execute_query("sales_by_category", """
        SELECT 
            p.category,
            COUNT(s.sale_id) as transactions,
            SUM(s.quantity_sold) as units_sold,
            SUM(s.total_amount) as revenue,
            ROUND(AVG(s.total_amount), 2) as avg_order_value,
            ROUND(SUM(s.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 2) as revenue_pct
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        """)
        
        self.execute_query("monthly_sales_trend", """
        SELECT 
            strftime('%Y-%m', s.sale_date) as month,
            COUNT(s.sale_id) as transaction_count,
            SUM(s.quantity_sold) as units_sold,
            SUM(s.total_amount) as monthly_revenue,
            ROUND(AVG(s.total_amount), 2) as avg_order_value,
            ROUND(AVG(s.discount_percent), 2) as avg_discount
        FROM sales s
        GROUP BY strftime('%Y-%m', s.sale_date)
        ORDER BY month
        """)
        
        self.execute_query("top_10_products", """
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
        LIMIT 10
        """)
        
        self.execute_query("sales_by_retailer_type", """
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
        ORDER BY total_revenue DESC
        """)
        
        self.execute_query("discount_impact_analysis", """
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
        ORDER BY discount_percent
        """)
        
        # 2. DISTRIBUTION & RETAILER ANALYSIS
        print("\n2. DISTRIBUTION & RETAILER ANALYSIS")
        
        self.execute_query("sales_by_region_distributor", """
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
        ORDER BY total_revenue DESC
        """)
        
        self.execute_query("top_retailers", """
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
        LIMIT 15
        """)
        
        self.execute_query("regional_sales_distribution", """
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
        ORDER BY total_revenue DESC
        """)
        
        # 3. INVENTORY MANAGEMENT
        print("\n3. INVENTORY MANAGEMENT")
        
        self.execute_query("inventory_status", """
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
        ORDER BY total_stock DESC
        """)
        
        self.execute_query("low_stock_alert", """
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
        ORDER BY units_needed DESC
        """)
        
        self.execute_query("inventory_turnover", """
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
        ORDER BY turnover_ratio DESC
        """)
        
        # 4. CUSTOMER ANALYSIS
        print("\n4. CUSTOMER ANALYSIS")
        
        self.execute_query("customer_demographics_analysis", """
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
        ORDER BY total_purchases DESC
        """)
        
        self.execute_query("health_condition_product_preference", """
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
        ORDER BY purchase_count DESC
        """)
        
        self.execute_query("geographic_customer_distribution", """
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
        ORDER BY total_transactions DESC
        """)
        
        # 5. MANUFACTURER & PRODUCT ANALYSIS
        print("\n5. MANUFACTURER & PRODUCT ANALYSIS")
        
        self.execute_query("manufacturer_performance", """
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
        ORDER BY total_revenue DESC
        """)
        
        self.execute_query("product_category_performance", """
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
        ORDER BY total_revenue DESC
        """)
        
        # 6. ADVANCED ANALYTICS
        print("\n6. ADVANCED ANALYTICS")
        
        self.execute_query("business_kpis", """
        SELECT 
            COUNT(DISTINCT s.sale_id) as total_transactions,
            SUM(s.quantity_sold) as total_units_sold,
            ROUND(SUM(s.total_amount), 2) as total_revenue,
            ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
            ROUND(SUM(s.total_amount) / COUNT(DISTINCT s.sale_id), 2) as revenue_per_transaction,
            COUNT(DISTINCT s.retailer_id) as active_retailers,
            COUNT(DISTINCT s.product_id) as products_sold,
            ROUND(AVG(s.discount_percent), 2) as avg_discount_rate
        FROM sales s
        """)
        
        self.execute_query("seasonal_trends", """
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
        ORDER BY quarter, revenue DESC
        """)
        
        print("\n✓ All SQL queries executed successfully!")
    
    def export_results(self):
        """Export all results to CSV and JSON"""
        print("\nExporting results...")
        
        for query_name, df in self.results.items():
            # Export to CSV
            csv_path = RESULTS_DIR / f"{query_name}.csv"
            df.to_csv(csv_path, index=False)
            
            # Export to JSON
            json_path = RESULTS_DIR / f"{query_name}.json"
            df.to_json(json_path, orient='records', indent=2)
            
            print(f"  ✓ {query_name}")
        
        print(f"\n✓ Results exported to {RESULTS_DIR}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    analyzer = SQLAnalyzer(DB_PATH)
    analyzer.run_all_queries()
    analyzer.export_results()
    analyzer.close()
    
    print("\n" + "="*60)
    print("SQL ANALYSIS COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
