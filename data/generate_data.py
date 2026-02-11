#!/usr/bin/env python3
"""
Synthetic FMCG Healthcare Dataset Generator
Generates realistic healthcare product sales and distribution data for portfolio analysis
"""

import sqlite3
import random
import pandas as pd
from datetime import datetime, timedelta
import json

# Set random seed for reproducibility
random.seed(42)

# Database setup
DB_PATH = '/home/ubuntu/fmcg-healthcare-portfolio/data/fmcg_healthcare.db'

def create_database():
    """Create SQLite database with FMCG Healthcare schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        unit_price REAL NOT NULL,
        manufacturer_id INTEGER NOT NULL
    )
    ''')
    
    # Manufacturers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS manufacturers (
        manufacturer_id INTEGER PRIMARY KEY,
        manufacturer_name TEXT NOT NULL,
        country TEXT NOT NULL,
        founded_year INTEGER
    )
    ''')
    
    # Distributors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS distributors (
        distributor_id INTEGER PRIMARY KEY,
        distributor_name TEXT NOT NULL,
        region TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        established_year INTEGER
    )
    ''')
    
    # Retailers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS retailers (
        retailer_id INTEGER PRIMARY KEY,
        retailer_name TEXT NOT NULL,
        retailer_type TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        distributor_id INTEGER,
        FOREIGN KEY (distributor_id) REFERENCES distributors(distributor_id)
    )
    ''')
    
    # Sales transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        retailer_id INTEGER NOT NULL,
        sale_date DATE NOT NULL,
        quantity_sold INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        discount_percent REAL DEFAULT 0,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (retailer_id) REFERENCES retailers(retailer_id)
    )
    ''')
    
    # Inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        retailer_id INTEGER NOT NULL,
        stock_quantity INTEGER NOT NULL,
        reorder_level INTEGER NOT NULL,
        last_updated DATE NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (retailer_id) REFERENCES retailers(retailer_id)
    )
    ''')
    
    # Customer demographics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_demographics (
        customer_id INTEGER PRIMARY KEY,
        age_group TEXT NOT NULL,
        gender TEXT NOT NULL,
        income_level TEXT NOT NULL,
        health_condition TEXT,
        city TEXT NOT NULL
    )
    ''')
    
    # Sales by customer table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_by_customer (
        transaction_id INTEGER PRIMARY KEY,
        sale_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_date DATE NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
        FOREIGN KEY (customer_id) REFERENCES customer_demographics(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_manufacturers(cursor):
    """Insert manufacturer data"""
    manufacturers = [
        (1, 'HealthCare Pharma Ltd', 'India', 1995),
        (2, 'Global Wellness Corp', 'USA', 2005),
        (3, 'Ayurveda Plus', 'India', 2000),
        (4, 'Nutrition World', 'Germany', 1998),
        (5, 'Wellness Innovations', 'Switzerland', 2008),
        (6, 'Natural Health Solutions', 'India', 2002),
        (7, 'Biotech Pharma', 'USA', 2010),
        (8, 'Herbal Remedies Inc', 'India', 1999),
    ]
    cursor.executemany('''
    INSERT INTO manufacturers (manufacturer_id, manufacturer_name, country, founded_year)
    VALUES (?, ?, ?, ?)
    ''', manufacturers)

def insert_products(cursor):
    """Insert product data"""
    products = [
        # Vitamins & Supplements
        (1, 'Vitamin C 500mg', 'Vitamins & Supplements', 'Vitamin C', 150, 1),
        (2, 'Vitamin D3 1000IU', 'Vitamins & Supplements', 'Vitamin D', 200, 2),
        (3, 'Multivitamin Daily', 'Vitamins & Supplements', 'Multivitamin', 250, 1),
        (4, 'Calcium Supplement', 'Vitamins & Supplements', 'Minerals', 180, 4),
        (5, 'Iron Supplement', 'Vitamins & Supplements', 'Minerals', 160, 3),
        
        # Digestive Health
        (6, 'Probiotic Capsules', 'Digestive Health', 'Probiotics', 350, 5),
        (7, 'Digestive Enzymes', 'Digestive Health', 'Enzymes', 280, 6),
        (8, 'Antacid Tablets', 'Digestive Health', 'Antacids', 120, 1),
        
        # Pain Relief
        (9, 'Ibuprofen 400mg', 'Pain Relief', 'Analgesics', 80, 2),
        (10, 'Aspirin 75mg', 'Pain Relief', 'Analgesics', 90, 1),
        (11, 'Muscle Relaxant Cream', 'Pain Relief', 'Topical', 220, 7),
        
        # Respiratory Health
        (12, 'Cough Syrup', 'Respiratory Health', 'Cough & Cold', 140, 3),
        (13, 'Throat Lozenges', 'Respiratory Health', 'Cough & Cold', 100, 8),
        (14, 'Asthma Inhaler', 'Respiratory Health', 'Respiratory', 450, 2),
        
        # Skin Care
        (15, 'Moisturizing Cream', 'Skin Care', 'Creams', 280, 5),
        (16, 'Anti-Acne Gel', 'Skin Care', 'Acne Treatment', 200, 6),
        (17, 'Sunscreen SPF 50', 'Skin Care', 'Sun Protection', 320, 4),
        
        # Immunity Boosters
        (18, 'Immunity Booster Drink', 'Immunity Boosters', 'Beverages', 180, 1),
        (19, 'Zinc Supplement', 'Immunity Boosters', 'Minerals', 170, 3),
        (20, 'Herbal Immunity Tea', 'Immunity Boosters', 'Herbal', 150, 8),
    ]
    cursor.executemany('''
    INSERT INTO products (product_id, product_name, category, subcategory, unit_price, manufacturer_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', products)

def insert_distributors(cursor):
    """Insert distributor data"""
    distributors = [
        (1, 'Metro Distribution', 'North', 'Delhi', 'Delhi', 2005),
        (2, 'Regional Pharma', 'South', 'Bangalore', 'Karnataka', 2008),
        (3, 'Eastern Healthcare', 'East', 'Kolkata', 'West Bengal', 2010),
        (4, 'Western Wellness', 'West', 'Mumbai', 'Maharashtra', 2006),
        (5, 'Central Supply Chain', 'Central', 'Indore', 'Madhya Pradesh', 2009),
        (6, 'National Distribution', 'Pan-India', 'Pune', 'Maharashtra', 2004),
    ]
    cursor.executemany('''
    INSERT INTO distributors (distributor_id, distributor_name, region, city, state, established_year)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', distributors)

def insert_retailers(cursor):
    """Insert retailer data"""
    retailers = [
        (1, 'MediCare Pharmacy', 'Chain Pharmacy', 'Delhi', 'Delhi', 1),
        (2, 'Health Plus Store', 'Independent', 'Delhi', 'Delhi', 1),
        (3, 'Wellness Hub', 'Chain Pharmacy', 'Bangalore', 'Karnataka', 2),
        (4, 'Local Chemist', 'Independent', 'Bangalore', 'Karnataka', 2),
        (5, 'City Health Center', 'Chain Pharmacy', 'Mumbai', 'Maharashtra', 4),
        (6, 'Neighborhood Pharmacy', 'Independent', 'Mumbai', 'Maharashtra', 4),
        (7, 'Health Mart', 'Chain Pharmacy', 'Kolkata', 'West Bengal', 3),
        (8, 'Wellness Express', 'Independent', 'Kolkata', 'West Bengal', 3),
        (9, 'Ayurveda Store', 'Specialty', 'Pune', 'Maharashtra', 6),
        (10, 'Modern Pharmacy', 'Chain Pharmacy', 'Hyderabad', 'Telangana', 2),
        (11, 'Health World', 'Independent', 'Chennai', 'Tamil Nadu', 2),
        (12, 'Wellness Center', 'Chain Pharmacy', 'Ahmedabad', 'Gujarat', 5),
        (13, 'Organic Health', 'Specialty', 'Jaipur', 'Rajasthan', 5),
        (14, 'Care Pharmacy', 'Independent', 'Lucknow', 'Uttar Pradesh', 1),
        (15, 'Health Store', 'Chain Pharmacy', 'Chandigarh', 'Chandigarh', 1),
    ]
    cursor.executemany('''
    INSERT INTO retailers (retailer_id, retailer_name, retailer_type, city, state, distributor_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', retailers)

def insert_customer_demographics(cursor):
    """Insert customer demographic data"""
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    genders = ['Male', 'Female']
    income_levels = ['Low', 'Middle', 'High']
    health_conditions = ['Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 'None', 'Allergy', 'Thyroid']
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    
    customers = []
    for i in range(1, 501):
        customers.append((
            i,
            random.choice(age_groups),
            random.choice(genders),
            random.choice(income_levels),
            random.choice(health_conditions),
            random.choice(cities)
        ))
    
    cursor.executemany('''
    INSERT INTO customer_demographics (customer_id, age_group, gender, income_level, health_condition, city)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', customers)

def insert_sales(cursor):
    """Insert sales transaction data"""
    sales = []
    sale_id = 1
    start_date = datetime(2023, 1, 1)
    
    for _ in range(2000):
        product_id = random.randint(1, 20)
        retailer_id = random.randint(1, 15)
        sale_date = start_date + timedelta(days=random.randint(0, 730))
        quantity = random.randint(1, 50)
        
        # Get unit price from products (we'll use a fixed mapping for simplicity)
        unit_prices = {i: 100 + i*10 for i in range(1, 21)}
        unit_price = unit_prices[product_id]
        
        discount = random.choice([0, 0, 0, 5, 10, 15])
        total_amount = quantity * unit_price * (1 - discount/100)
        
        sales.append((
            sale_id,
            product_id,
            retailer_id,
            sale_date.strftime('%Y-%m-%d'),
            quantity,
            unit_price,
            total_amount,
            discount
        ))
        sale_id += 1
    
    cursor.executemany('''
    INSERT INTO sales (sale_id, product_id, retailer_id, sale_date, quantity_sold, unit_price, total_amount, discount_percent)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sales)

def insert_inventory(cursor):
    """Insert inventory data"""
    inventory = []
    inv_id = 1
    
    for retailer_id in range(1, 16):
        for product_id in range(1, 21):
            inventory.append((
                inv_id,
                product_id,
                retailer_id,
                random.randint(10, 500),
                random.randint(5, 50),
                datetime.now().strftime('%Y-%m-%d')
            ))
            inv_id += 1
    
    cursor.executemany('''
    INSERT INTO inventory (inventory_id, product_id, retailer_id, stock_quantity, reorder_level, last_updated)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', inventory)

def insert_sales_by_customer(cursor):
    """Insert customer-level sales data"""
    sales_by_customer = []
    trans_id = 1
    
    for sale_id in range(1, 2001):
        customer_id = random.randint(1, 500)
        product_id = random.randint(1, 20)
        quantity = random.randint(1, 10)
        purchase_date = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')
        
        sales_by_customer.append((
            trans_id,
            sale_id,
            customer_id,
            product_id,
            quantity,
            purchase_date
        ))
        trans_id += 1
    
    cursor.executemany('''
    INSERT INTO sales_by_customer (transaction_id, sale_id, customer_id, product_id, quantity, purchase_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sales_by_customer)

def main():
    """Main function to generate dataset"""
    print("Creating FMCG Healthcare database...")
    conn, cursor = create_database()
    
    print("Inserting manufacturers...")
    insert_manufacturers(cursor)
    
    print("Inserting products...")
    insert_products(cursor)
    
    print("Inserting distributors...")
    insert_distributors(cursor)
    
    print("Inserting retailers...")
    insert_retailers(cursor)
    
    print("Inserting customer demographics...")
    insert_customer_demographics(cursor)
    
    print("Inserting sales transactions...")
    insert_sales(cursor)
    
    print("Inserting inventory...")
    insert_inventory(cursor)
    
    print("Inserting customer sales data...")
    insert_sales_by_customer(cursor)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database created successfully at {DB_PATH}")
    print("✓ Total records inserted:")
    print("  - 8 Manufacturers")
    print("  - 20 Products")
    print("  - 6 Distributors")
    print("  - 15 Retailers")
    print("  - 500 Customers")
    print("  - 2000 Sales Transactions")
    print("  - 300 Inventory Records")
    print("  - 2000 Customer Sales Records")

if __name__ == '__main__':
    main()
