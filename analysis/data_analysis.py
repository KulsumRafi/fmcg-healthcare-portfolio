#!/usr/bin/env python3
"""
FMCG Healthcare Data Analysis
Comprehensive Python analysis with visualizations and statistical insights
"""

import sqlite3
import pandas as pd
import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DB_PATH = '/home/ubuntu/fmcg-healthcare-portfolio/data/fmcg_healthcare.db'
OUTPUT_DIR = Path('/home/ubuntu/fmcg-healthcare-portfolio/analysis')
VISUALIZATIONS_DIR = OUTPUT_DIR / 'visualizations'
VISUALIZATIONS_DIR.mkdir(exist_ok=True)

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class FMCGAnalyzer:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.insights = {}
        
    def query_to_dataframe(self, query):
        """Execute SQL query and return as pandas DataFrame"""
        return pd.read_sql_query(query, self.conn)
    
    # ========================================================================
    # 1. SALES ANALYSIS
    # ========================================================================
    
    def analyze_sales_by_category(self):
        """Analyze sales performance by product category"""
        query = """
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
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Revenue by category
        ax1 = axes[0, 0]
        colors = sns.color_palette("husl", len(df))
        bars = ax1.barh(df['category'], df['revenue'], color=colors)
        ax1.set_xlabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Total Revenue by Category', fontsize=13, fontweight='bold')
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', ha='left', va='center', fontweight='bold')
        
        # Units sold by category
        ax2 = axes[0, 1]
        ax2.bar(df['category'], df['units_sold'], color=colors, alpha=0.7)
        ax2.set_ylabel('Units Sold', fontsize=11, fontweight='bold')
        ax2.set_title('Total Units Sold by Category', fontsize=13, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        # Transaction count
        ax3 = axes[1, 0]
        ax3.pie(df['transactions'], labels=df['category'], autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax3.set_title('Transaction Distribution by Category', fontsize=13, fontweight='bold')
        
        # Average order value
        ax4 = axes[1, 1]
        ax4.bar(df['category'], df['avg_order_value'], color=colors, alpha=0.7)
        ax4.set_ylabel('Average Order Value ($)', fontsize=11, fontweight='bold')
        ax4.set_title('Average Order Value by Category', fontsize=13, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'sales_by_category.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['sales_by_category'] = df.to_dict('records')
        return df
    
    def analyze_monthly_trends(self):
        """Analyze monthly sales trends"""
        query = """
        SELECT 
            strftime('%Y-%m', s.sale_date) as month,
            COUNT(s.sale_id) as transactions,
            SUM(s.quantity_sold) as units_sold,
            SUM(s.total_amount) as revenue,
            ROUND(AVG(s.total_amount), 2) as avg_order_value
        FROM sales s
        GROUP BY strftime('%Y-%m', s.sale_date)
        ORDER BY month
        """
        df = self.query_to_dataframe(query)
        df['month'] = pd.to_datetime(df['month'])
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Revenue trend
        ax1 = axes[0, 0]
        ax1.plot(df['month'], df['revenue'], marker='o', linewidth=2.5, 
                markersize=8, color='#2E86AB')
        ax1.fill_between(df['month'], df['revenue'], alpha=0.3, color='#2E86AB')
        ax1.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Monthly Revenue Trend', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Units sold trend
        ax2 = axes[0, 1]
        ax2.plot(df['month'], df['units_sold'], marker='s', linewidth=2.5, 
                markersize=8, color='#A23B72')
        ax2.fill_between(df['month'], df['units_sold'], alpha=0.3, color='#A23B72')
        ax2.set_ylabel('Units Sold', fontsize=11, fontweight='bold')
        ax2.set_title('Monthly Units Sold Trend', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Transaction count
        ax3 = axes[1, 0]
        ax3.bar(df['month'], df['transactions'], color='#F18F01', alpha=0.7)
        ax3.set_ylabel('Transaction Count', fontsize=11, fontweight='bold')
        ax3.set_title('Monthly Transaction Count', fontsize=13, fontweight='bold')
        
        # Average order value trend
        ax4 = axes[1, 1]
        ax4.plot(df['month'], df['avg_order_value'], marker='D', linewidth=2.5, 
                markersize=8, color='#C73E1D')
        ax4.set_ylabel('Average Order Value ($)', fontsize=11, fontweight='bold')
        ax4.set_title('Monthly Average Order Value Trend', fontsize=13, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'monthly_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['monthly_trends'] = df.to_dict('records')
        return df
    
    def analyze_top_products(self):
        """Analyze top-selling products"""
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            COUNT(s.sale_id) as times_sold,
            SUM(s.quantity_sold) as total_quantity,
            SUM(s.total_amount) as total_revenue,
            ROUND(AVG(s.total_amount), 2) as avg_order_value
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
        LIMIT 10
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Top 10 by revenue
        ax1 = axes[0, 0]
        colors = sns.color_palette("viridis", len(df))
        bars = ax1.barh(df['product_name'], df['total_revenue'], color=colors)
        ax1.set_xlabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Top 10 Products by Revenue', fontsize=13, fontweight='bold')
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', ha='left', va='center', fontsize=9)
        
        # Top 10 by quantity
        ax2 = axes[0, 1]
        ax2.barh(df['product_name'], df['total_quantity'], color=colors, alpha=0.7)
        ax2.set_xlabel('Units Sold', fontsize=11, fontweight='bold')
        ax2.set_title('Top 10 Products by Units Sold', fontsize=13, fontweight='bold')
        
        # Top 10 by frequency
        ax3 = axes[1, 0]
        ax3.barh(df['product_name'], df['times_sold'], color=colors, alpha=0.7)
        ax3.set_xlabel('Times Sold', fontsize=11, fontweight='bold')
        ax3.set_title('Top 10 Products by Sales Frequency', fontsize=13, fontweight='bold')
        
        # Average order value
        ax4 = axes[1, 1]
        ax4.barh(df['product_name'], df['avg_order_value'], color=colors, alpha=0.7)
        ax4.set_xlabel('Average Order Value ($)', fontsize=11, fontweight='bold')
        ax4.set_title('Top 10 Products by Average Order Value', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'top_products.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['top_products'] = df.to_dict('records')
        return df
    
    # ========================================================================
    # 2. RETAILER ANALYSIS
    # ========================================================================
    
    def analyze_retailer_performance(self):
        """Analyze retailer performance metrics"""
        query = """
        SELECT 
            r.retailer_id,
            r.retailer_name,
            r.retailer_type,
            r.city,
            COUNT(s.sale_id) as transactions,
            SUM(s.quantity_sold) as units_sold,
            SUM(s.total_amount) as revenue,
            ROUND(AVG(s.total_amount), 2) as avg_order_value,
            COUNT(DISTINCT s.product_id) as product_variety
        FROM sales s
        JOIN retailers r ON s.retailer_id = r.retailer_id
        GROUP BY r.retailer_id
        ORDER BY revenue DESC
        LIMIT 15
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Top retailers by revenue
        ax1 = axes[0, 0]
        colors = sns.color_palette("coolwarm", len(df))
        bars = ax1.barh(df['retailer_name'], df['revenue'], color=colors)
        ax1.set_xlabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Top 15 Retailers by Revenue', fontsize=13, fontweight='bold')
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', ha='left', va='center', fontsize=8)
        
        # Retailer type distribution
        ax2 = axes[0, 1]
        retailer_type_counts = df['retailer_type'].value_counts()
        ax2.pie(retailer_type_counts, labels=retailer_type_counts.index, autopct='%1.1f%%',
               colors=sns.color_palette("Set2", len(retailer_type_counts)))
        ax2.set_title('Retailer Type Distribution (Top 15)', fontsize=13, fontweight='bold')
        
        # Transactions vs Revenue scatter
        ax3 = axes[1, 0]
        scatter = ax3.scatter(df['transactions'], df['revenue'], 
                             s=df['product_variety']*50, alpha=0.6, 
                             c=range(len(df)), cmap='viridis')
        ax3.set_xlabel('Transaction Count', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax3.set_title('Transactions vs Revenue (bubble size = product variety)', 
                     fontsize=13, fontweight='bold')
        
        # Average order value by retailer type
        ax4 = axes[1, 1]
        aov_by_type = df.groupby('retailer_type')['avg_order_value'].mean().sort_values(ascending=False)
        ax4.bar(aov_by_type.index, aov_by_type.values, 
               color=sns.color_palette("Set2", len(aov_by_type)))
        ax4.set_ylabel('Average Order Value ($)', fontsize=11, fontweight='bold')
        ax4.set_title('Average Order Value by Retailer Type', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'retailer_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['retailer_performance'] = df.to_dict('records')
        return df
    
    def analyze_regional_sales(self):
        """Analyze sales by region and state"""
        query = """
        SELECT 
            r.state,
            COUNT(DISTINCT r.retailer_id) as retailer_count,
            COUNT(s.sale_id) as transactions,
            SUM(s.quantity_sold) as units_sold,
            SUM(s.total_amount) as revenue,
            ROUND(SUM(s.total_amount) / COUNT(DISTINCT r.retailer_id), 2) as revenue_per_retailer,
            ROUND(SUM(s.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales), 2) as market_share
        FROM sales s
        JOIN retailers r ON s.retailer_id = r.retailer_id
        GROUP BY r.state
        ORDER BY revenue DESC
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Revenue by state
        ax1 = axes[0, 0]
        colors = sns.color_palette("RdYlGn", len(df))
        bars = ax1.barh(df['state'], df['revenue'], color=colors)
        ax1.set_xlabel('Revenue ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Revenue by State', fontsize=13, fontweight='bold')
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}', ha='left', va='center', fontsize=9)
        
        # Market share pie chart
        ax2 = axes[0, 1]
        ax2.pie(df['revenue'], labels=df['state'], autopct='%1.1f%%', startangle=90)
        ax2.set_title('Market Share by State', fontsize=13, fontweight='bold')
        
        # Retailers vs Revenue
        ax3 = axes[1, 0]
        ax3_twin = ax3.twinx()
        bars = ax3.bar(df['state'], df['retailer_count'], alpha=0.7, color='skyblue', label='Retailers')
        line = ax3_twin.plot(df['state'], df['revenue'], marker='o', color='red', 
                            linewidth=2.5, markersize=8, label='Revenue')
        ax3.set_ylabel('Retailer Count', fontsize=11, fontweight='bold', color='skyblue')
        ax3_twin.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold', color='red')
        ax3.set_title('Retailers Count vs Revenue by State', fontsize=13, fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)
        
        # Revenue per retailer
        ax4 = axes[1, 1]
        ax4.bar(df['state'], df['revenue_per_retailer'], color=colors, alpha=0.7)
        ax4.set_ylabel('Revenue per Retailer ($)', fontsize=11, fontweight='bold')
        ax4.set_title('Revenue per Retailer by State', fontsize=13, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'regional_sales.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['regional_sales'] = df.to_dict('records')
        return df
    
    # ========================================================================
    # 3. CUSTOMER ANALYSIS
    # ========================================================================
    
    def analyze_customer_demographics(self):
        """Analyze customer demographics and purchasing behavior"""
        query = """
        SELECT 
            cd.age_group,
            cd.income_level,
            COUNT(DISTINCT cd.customer_id) as customer_count,
            COUNT(sbc.transaction_id) as total_purchases,
            SUM(sbc.quantity) as total_units,
            ROUND(COUNT(sbc.transaction_id) / COUNT(DISTINCT cd.customer_id), 2) as avg_purchases_per_customer,
            ROUND(SUM(sbc.quantity) / COUNT(sbc.transaction_id), 2) as avg_units_per_purchase
        FROM customer_demographics cd
        LEFT JOIN sales_by_customer sbc ON cd.customer_id = sbc.customer_id
        GROUP BY cd.age_group, cd.income_level
        ORDER BY total_purchases DESC
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Customers by age and income
        pivot_customers = df.pivot_table(values='customer_count', 
                                        index='age_group', 
                                        columns='income_level', 
                                        aggfunc='sum')
        ax1 = axes[0, 0]
        pivot_customers.plot(kind='bar', ax=ax1, color=sns.color_palette("Set2", 3))
        ax1.set_ylabel('Customer Count', fontsize=11, fontweight='bold')
        ax1.set_xlabel('Age Group', fontsize=11, fontweight='bold')
        ax1.set_title('Customer Distribution by Age & Income Level', fontsize=13, fontweight='bold')
        ax1.legend(title='Income Level', fontsize=10)
        ax1.tick_params(axis='x', rotation=45)
        
        # Purchases by age and income
        pivot_purchases = df.pivot_table(values='total_purchases', 
                                        index='age_group', 
                                        columns='income_level', 
                                        aggfunc='sum')
        ax2 = axes[0, 1]
        pivot_purchases.plot(kind='bar', ax=ax2, color=sns.color_palette("Set2", 3))
        ax2.set_ylabel('Total Purchases', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Age Group', fontsize=11, fontweight='bold')
        ax2.set_title('Purchase Count by Age & Income Level', fontsize=13, fontweight='bold')
        ax2.legend(title='Income Level', fontsize=10)
        ax2.tick_params(axis='x', rotation=45)
        
        # Average purchases per customer
        pivot_avg = df.pivot_table(values='avg_purchases_per_customer', 
                                   index='age_group', 
                                   columns='income_level', 
                                   aggfunc='mean')
        ax3 = axes[1, 0]
        pivot_avg.plot(kind='bar', ax=ax3, color=sns.color_palette("Set2", 3))
        ax3.set_ylabel('Avg Purchases per Customer', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Age Group', fontsize=11, fontweight='bold')
        ax3.set_title('Average Purchases per Customer by Demographics', fontsize=13, fontweight='bold')
        ax3.legend(title='Income Level', fontsize=10)
        ax3.tick_params(axis='x', rotation=45)
        
        # Average units per purchase
        pivot_units = df.pivot_table(values='avg_units_per_purchase', 
                                     index='age_group', 
                                     columns='income_level', 
                                     aggfunc='mean')
        ax4 = axes[1, 1]
        pivot_units.plot(kind='bar', ax=ax4, color=sns.color_palette("Set2", 3))
        ax4.set_ylabel('Avg Units per Purchase', fontsize=11, fontweight='bold')
        ax4.set_xlabel('Age Group', fontsize=11, fontweight='bold')
        ax4.set_title('Average Units per Purchase by Demographics', fontsize=13, fontweight='bold')
        ax4.legend(title='Income Level', fontsize=10)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'customer_demographics.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['customer_demographics'] = df.to_dict('records')
        return df
    
    # ========================================================================
    # 4. INVENTORY ANALYSIS
    # ========================================================================
    
    def analyze_inventory_status(self):
        """Analyze current inventory status"""
        query = """
        SELECT 
            p.product_name,
            p.category,
            COUNT(i.inventory_id) as retailer_locations,
            SUM(i.stock_quantity) as total_stock,
            ROUND(AVG(i.stock_quantity), 2) as avg_stock_per_location,
            COUNT(CASE WHEN i.stock_quantity < i.reorder_level THEN 1 END) as locations_below_reorder
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_stock DESC
        """
        df = self.query_to_dataframe(query)
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Total stock by product
        ax1 = axes[0, 0]
        colors = sns.color_palette("viridis", len(df))
        bars = ax1.barh(df['product_name'], df['total_stock'], color=colors)
        ax1.set_xlabel('Total Stock Units', fontsize=11, fontweight='bold')
        ax1.set_title('Current Inventory Levels by Product', fontsize=13, fontweight='bold')
        
        # Stock distribution
        ax2 = axes[0, 1]
        ax2.scatter(df['retailer_locations'], df['total_stock'], 
                   s=df['avg_stock_per_location']*10, alpha=0.6, c=range(len(df)), cmap='viridis')
        ax2.set_xlabel('Number of Retailer Locations', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Total Stock Units', fontsize=11, fontweight='bold')
        ax2.set_title('Stock Distribution Across Locations', fontsize=13, fontweight='bold')
        
        # Low stock alerts
        ax3 = axes[1, 0]
        low_stock = df[df['locations_below_reorder'] > 0].sort_values('locations_below_reorder', ascending=False)
        if len(low_stock) > 0:
            ax3.barh(low_stock['product_name'], low_stock['locations_below_reorder'], color='#FF6B6B')
            ax3.set_xlabel('Number of Locations Below Reorder Level', fontsize=11, fontweight='bold')
            ax3.set_title('Low Stock Alert - Products Below Reorder Level', fontsize=13, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No products below reorder level', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=12)
        
        # Average stock per location
        ax4 = axes[1, 1]
        top_avg_stock = df.nlargest(10, 'avg_stock_per_location')
        ax4.barh(top_avg_stock['product_name'], top_avg_stock['avg_stock_per_location'], 
                color=sns.color_palette("coolwarm", 10))
        ax4.set_xlabel('Average Stock per Location', fontsize=11, fontweight='bold')
        ax4.set_title('Top 10 Products by Average Stock per Location', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / 'inventory_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        self.insights['inventory_status'] = df.to_dict('records')
        return df
    
    # ========================================================================
    # 5. STATISTICAL SUMMARY
    # ========================================================================
    
    def generate_statistical_summary(self):
        """Generate comprehensive statistical summary"""
        query = """
        SELECT 
            COUNT(DISTINCT s.sale_id) as total_transactions,
            SUM(s.quantity_sold) as total_units_sold,
            SUM(s.total_amount) as total_revenue,
            ROUND(AVG(s.total_amount), 2) as avg_transaction_value,
            ROUND(MIN(s.total_amount), 2) as min_transaction_value,
            ROUND(MAX(s.total_amount), 2) as max_transaction_value,
            COUNT(DISTINCT s.retailer_id) as active_retailers,
            COUNT(DISTINCT s.product_id) as products_sold,
            ROUND(AVG(s.discount_percent), 2) as avg_discount_rate
        FROM sales s
        """
        df = self.query_to_dataframe(query)
        
        amounts_query = "SELECT total_amount FROM sales"
        amounts_df = self.query_to_dataframe(amounts_query)
        stdev = amounts_df['total_amount'].std()
        
        summary = df.to_dict('records')[0]
        summary['stdev_transaction_value'] = round(stdev, 2)
        
        self.insights['statistical_summary'] = summary
        return df
    
    def run_all_analysis(self):
        """Run all analysis functions"""
        print("Running comprehensive FMCG Healthcare analysis...")
        
        print("  → Analyzing sales by category...")
        self.analyze_sales_by_category()
        
        print("  → Analyzing monthly trends...")
        self.analyze_monthly_trends()
        
        print("  → Analyzing top products...")
        self.analyze_top_products()
        
        print("  → Analyzing retailer performance...")
        self.analyze_retailer_performance()
        
        print("  → Analyzing regional sales...")
        self.analyze_regional_sales()
        
        print("  → Analyzing customer demographics...")
        self.analyze_customer_demographics()
        
        print("  → Analyzing inventory status...")
        self.analyze_inventory_status()
        
        print("  → Generating statistical summary...")
        self.generate_statistical_summary()
        
        print("✓ All analysis complete!")
        return self.insights
    
    def save_insights_json(self, output_file):
        """Save insights to JSON file"""
        # Convert datetime objects to strings for JSON serialization
        insights_serializable = {}
        for key, value in self.insights.items():
            if isinstance(value, list):
                insights_serializable[key] = [
                    {k: (str(v) if isinstance(v, (pd.Timestamp, datetime)) else v) 
                     for k, v in item.items()}
                    for item in value
                ]
            elif isinstance(value, dict):
                insights_serializable[key] = {
                    k: (str(v) if isinstance(v, (pd.Timestamp, datetime)) else v) 
                    for k, v in value.items()
                }
            else:
                insights_serializable[key] = value
        
        with open(output_file, 'w') as f:
            json.dump(insights_serializable, f, indent=2)
        
        print(f"✓ Insights saved to {output_file}")

def main():
    analyzer = FMCGAnalyzer(DB_PATH)
    insights = analyzer.run_all_analysis()
    analyzer.save_insights_json(OUTPUT_DIR / 'analysis_insights.json')
    
    print(f"\n✓ Visualizations saved to: {VISUALIZATIONS_DIR}")
    print(f"✓ Insights JSON saved to: {OUTPUT_DIR / 'analysis_insights.json'}")

if __name__ == '__main__':
    main()
