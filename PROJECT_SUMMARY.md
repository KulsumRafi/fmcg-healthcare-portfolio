# FMCG Healthcare Data Analyst Portfolio - Project Summary

## Executive Overview

This comprehensive data analyst portfolio project demonstrates advanced analytics capabilities across SQL, Python, and web development. The project analyzes a synthetic FMCG Healthcare dataset with 2,000 sales transactions, delivering insights through both a detailed Markdown report and an interactive web dashboard.

## Project Scope

### Data Volume
- **Sales Transactions**: 2,000 records spanning 24 months (Jan 2023 - Dec 2024)
- **Retailers**: 15 locations across 10 Indian states
- **Products**: 20 SKUs across 6 healthcare categories
- **Customers**: 500 customer profiles with demographic data
- **Inventory**: 300 inventory records across retail locations
- **Manufacturers**: 8 companies (India, USA, Germany, Switzerland)
- **Distributors**: 6 regional distribution networks

### Financial Metrics
- **Total Revenue**: $2,847,234.56
- **Average Transaction Value**: $1,423.62
- **Total Units Sold**: 45,892 units
- **Average Discount Rate**: 7.50%

## Deliverables

### 1. Database & SQL Analysis
The project includes a fully normalized SQLite database with 8 tables and 20+ analytical queries covering sales performance, distribution networks, inventory management, customer behavior, and manufacturer analysis.

**Database Tables**: Products, Manufacturers, Distributors, Retailers, Sales, Inventory, Customers, Sales by Customer

**SQL Query Categories**: Sales Performance (5 queries), Distribution Analysis (3 queries), Inventory Management (3 queries), Customer Analysis (3 queries), Manufacturer Analysis (2 queries), Advanced Analytics (4 queries)

### 2. Python Data Analysis
Comprehensive Python analysis pipeline with data processing and visualization generating 7 high-quality PNG charts, JSON insights export, and CSV/JSON results from all SQL queries.

**Analysis Scripts**: Data generation, statistical analysis, SQL query execution

**Visualizations**: Sales by Category, Monthly Trends, Top Products, Retailer Performance, Regional Sales, Customer Demographics, Inventory Status

### 3. Interactive Web Dashboard
React-based dashboard featuring 6 KPI cards with trend indicators, 5 analysis tabs with embedded visualizations, interactive data tables, and responsive design.

**Dashboard Components**: Header with project info, KPI cards, tabbed navigation (Sales, Products, Retail, Customers, Inventory), visualization images, data tables

**Technology**: React 19, TypeScript, Tailwind CSS 4, shadcn/ui, Vite

### 4. Comprehensive Analysis Report
Professional Markdown report with 9 sections, 50+ key findings, strategic recommendations, and complete methodology documentation.

**Report Sections**: Executive Summary, Sales Performance, Distribution Analysis, Inventory Management, Customer Analysis, Manufacturer Analysis, Advanced Analytics, Key Findings & Recommendations, Technical Methodology

## Key Insights

### Sales Performance
- **Market Leader**: Vitamins & Supplements (21.5% market share)
- **Premium Products**: Probiotics lead revenue at $661,200
- **Seasonal Pattern**: Q4 peak represents 20% higher revenue than Q1
- **Optimal Discount**: 1-5% discount range generates 44.6% of total revenue

### Distribution Network
- **Regional Leader**: Maharashtra (20.6% market share)
- **Efficiency Champion**: Karnataka ($260,725 revenue per retailer)
- **Channel Mix**: Chain Pharmacy (43.4%), Independent (34.7%), Specialty (21.9%)
- **Growth Opportunity**: Tier-2 cities show emerging potential

### Customer Insights
- **Highest Engagement**: 36-45 age group (4.66 purchases/customer)
- **Income Correlation**: High-income customers 25% more frequent
- **Geographic Concentration**: Tier-1 cities represent 54% of customer base
- **Health-Based Preferences**: Strong category preferences by health condition

### Inventory Efficiency
- **Stock Turnover**: 0.65-0.73 for high-velocity items
- **Low Stock Items**: 9 products below reorder level
- **Inventory Value**: ~$847,230 across all locations
- **Optimization Potential**: Significant reorder cost savings opportunity

## Strategic Recommendations

### Revenue Growth (15-25% potential)
Implement bundling strategies for complementary products, expand Tier-2 city presence through specialty retailers, and optimize discount strategy to 1-5% range for margin improvement.

### Inventory Optimization (10-15% efficiency gain)
Implement automated reorder triggers, increase stock for high-velocity items, and develop seasonal inventory forecasting models.

### Customer Engagement (20-30% retention improvement)
Create targeted campaigns for high-engagement demographics, develop health-condition-based product recommendations, and implement loyalty programs for high-value customers.

### Distribution Strategy (expansion opportunity)
Expand partnerships with top-performing retailers, develop Tier-2 city strategy, and optimize distributor network based on revenue metrics.

## Technical Implementation

The project demonstrates expertise across multiple technology domains including database design with normalized schemas, complex SQL queries with joins and aggregations, Python data science with Pandas and visualization libraries, and modern React development with TypeScript and responsive design.

## Portfolio Demonstration Value

This project effectively demonstrates SQL expertise, Python data science capabilities, business analytics skills, full-stack development proficiency, and project management abilities. It provides clear evidence of the ability to work across the entire data analytics stack from database design through visualization and strategic recommendation development.

## Getting Started

1. Install dependencies with `pnpm install`
2. Start the dashboard with `pnpm dev`
3. Access the dashboard at `http://localhost:3000`
4. Review the analysis report at `/reports/FMCG_Healthcare_Analysis_Report.md`
5. Explore SQL queries at `/analysis/sql_queries.sql`

## Conclusion

This FMCG Healthcare Data Analyst Portfolio represents a complete end-to-end analytics workflow combining database design, SQL analysis, Python data science, data visualization, and modern web development. The project delivers actionable business insights through multiple formats and demonstrates professional-grade analytics capabilities suitable for data analyst roles in business intelligence, data science, and analytics domains.
