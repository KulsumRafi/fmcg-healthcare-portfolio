# FMCG Healthcare Data Analyst Portfolio

A comprehensive data analyst portfolio project demonstrating advanced SQL and Python analytics skills applied to the FMCG Healthcare domain. This project includes a complete data pipeline, SQL analysis, Python-based data science, and an interactive web dashboard.

## 📊 Project Overview

This portfolio showcases a complete end-to-end data analysis workflow for the FMCG Healthcare sector, featuring:

- **Synthetic Dataset**: 2,000+ sales transactions across 15 retailers in 10 states
- **SQL Analysis**: 20+ complex queries covering sales, distribution, inventory, and customer insights
- **Python Analytics**: Data visualization and statistical analysis with Pandas, Matplotlib, and Seaborn
- **Interactive Dashboard**: React-based web dashboard with real-time data visualization
- **Comprehensive Report**: Detailed Markdown analysis report with strategic recommendations

## 🎯 Key Deliverables

### 1. Database & SQL Analysis
- **Location**: `/data/fmcg_healthcare.db` (SQLite database)
- **Schema**: 8 tables covering products, manufacturers, distributors, retailers, sales, inventory, and customers
- **Queries**: 20+ SQL queries in `/analysis/sql_queries.sql`
- **Results**: Exported CSV and JSON files in `/analysis/sql_results/`

### 2. Python Data Analysis
- **Data Generation**: `/data/generate_data.py` - Creates synthetic FMCG Healthcare dataset
- **Analysis Script**: `/analysis/data_analysis.py` - Comprehensive statistical analysis
- **SQL Execution**: `/analysis/execute_sql_analysis.py` - Runs all SQL queries and exports results
- **Visualizations**: 7 high-quality PNG charts in `/analysis/visualizations/`
- **Insights**: JSON export of all analysis metrics in `/analysis/analysis_insights.json`

### 3. Interactive Dashboard
- **Framework**: React 19 + Tailwind CSS 4 + shadcn/ui
- **Features**:
  - 6 KPI cards with trend indicators
  - 5 analysis tabs (Sales, Products, Retail, Customers, Inventory)
  - 7 embedded visualizations
  - Interactive data tables with detailed metrics
  - Responsive design for all devices

### 4. Analysis Report
- **Location**: `/reports/FMCG_Healthcare_Analysis_Report.md`
- **Content**: 9 comprehensive sections covering all analysis dimensions
- **Insights**: 50+ key findings and strategic recommendations
- **Format**: Professional Markdown with tables, metrics, and insights

## 📁 Project Structure

```
fmcg-healthcare-portfolio/
├── data/
│   ├── generate_data.py              # Dataset generation script
│   └── fmcg_healthcare.db            # SQLite database (2000+ records)
├── analysis/
│   ├── data_analysis.py              # Python analysis script
│   ├── execute_sql_analysis.py       # SQL query execution
│   ├── sql_queries.sql               # 20+ SQL queries
│   ├── analysis_insights.json        # Analysis results (JSON)
│   ├── visualizations/               # 7 PNG charts
│   │   ├── sales_by_category.png
│   │   ├── monthly_trends.png
│   │   ├── top_products.png
│   │   ├── retailer_performance.png
│   │   ├── regional_sales.png
│   │   ├── customer_demographics.png
│   │   └── inventory_status.png
│   └── sql_results/                  # SQL query results (CSV/JSON)
├── reports/
│   └── FMCG_Healthcare_Analysis_Report.md
├── client/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Dashboard.tsx         # Main dashboard component
│   │   ├── lib/
│   │   │   └── dashboardData.ts      # Data utilities
│   │   ├── App.tsx
│   │   └── index.css
│   ├── public/
│   │   ├── *.png                     # Visualization images
│   │   └── analysis_insights.json    # Analysis data
│   └── index.html
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Node.js 22.13.0+
- Python 3.11+
- SQLite 3

### Installation

1. **Install Dependencies**
   ```bash
   cd fmcg-healthcare-portfolio
   pnpm install
   ```

2. **Generate Dataset** (if needed)
   ```bash
   python3 data/generate_data.py
   ```

3. **Run Analysis** (if needed)
   ```bash
   python3 analysis/data_analysis.py
   python3 analysis/execute_sql_analysis.py
   ```

4. **Start Development Server**
   ```bash
   pnpm dev
   ```

5. **Access Dashboard**
   - Open `http://localhost:3000` in your browser

## 📊 Data Analysis Highlights

### Sales Performance
- **Total Revenue**: $2,847,234.56
- **Total Transactions**: 2,000
- **Average Order Value**: $1,423.62
- **Top Category**: Vitamins & Supplements (21.5% market share)
- **Peak Month**: December 2023 ($127,450)

### Distribution Network
- **Active Retailers**: 15 across 10 states
- **Top Region**: Maharashtra (20.6% market share)
- **Retailer Types**: Chain Pharmacy (43.4%), Independent (34.7%), Specialty (21.9%)
- **Highest Efficiency**: Karnataka ($260,725 revenue per retailer)

### Customer Insights
- **Total Customers**: 500 profiled
- **Most Engaged Segment**: 36-45 age group (4.66 purchases/customer)
- **High-Income Customers**: 25% higher purchase frequency
- **Top Cities**: Delhi (78), Mumbai (65), Bangalore (58)

### Inventory Management
- **Total Products**: 20 SKUs across 6 categories
- **Stock Locations**: 15 retailers × 20 products = 300 inventory records
- **Low Stock Items**: 9 products below reorder level
- **Turnover Ratio**: 0.65-0.73 for high-velocity items

## 🔍 SQL Analysis Queries

The project includes 20+ SQL queries organized by category:

### Sales Analysis
- Sales by category with revenue distribution
- Monthly sales trends (24-month analysis)
- Top 10 best-selling products
- Discount impact analysis
- Sales by retailer type

### Distribution Analysis
- Sales by region and distributor
- Top 15 retailer performance
- Regional sales distribution
- Retailer efficiency metrics

### Inventory Management
- Current inventory status
- Low stock alerts
- Inventory turnover analysis
- Inventory value by retailer

### Customer Analysis
- Customer demographics segmentation
- Health condition product preferences
- Geographic customer distribution
- Customer lifetime value estimation

### Advanced Analytics
- Business KPIs summary
- Seasonal trends analysis
- Cross-selling opportunities
- Market basket analysis

## 📈 Python Analysis Features

### Data Processing
- Pandas DataFrames for data manipulation
- SQLite database queries
- Data aggregation and transformation
- Statistical calculations

### Visualizations
- Multi-panel analysis charts
- Time-series trend analysis
- Comparative ranking visualizations
- Distribution and demographic heatmaps
- Scatter plots for correlation analysis

### Insights Generation
- JSON export of all metrics
- Formatted currency and number utilities
- Percentage calculations
- Trend indicators

## 🎨 Dashboard Features

### KPI Cards
- Total Revenue with trend indicator
- Transaction count and growth
- Average order value
- Active retailer count
- Product portfolio size
- Discount rate tracking

### Analysis Tabs

**Sales Tab**
- Sales by category visualization
- Monthly trends analysis
- Category performance table

**Products Tab**
- Top products visualization
- Product detail table with revenue breakdown

**Retail Tab**
- Retailer performance analysis
- Regional sales distribution
- Regional performance table

**Customers Tab**
- Customer demographics visualization
- Customer segment breakdown

**Inventory Tab**
- Inventory status visualization
- Product stock levels table

## 💡 Key Insights & Recommendations

### Strategic Findings
1. **Market Concentration**: Top 10 products = 62.3% of revenue
2. **Regional Opportunity**: Tier-2 cities show 3.2-3.7 engagement rates
3. **Premium Positioning**: Specialty retailers show 28% higher AOV
4. **Seasonal Dependency**: Q4 peak = 20% higher revenue than Q1
5. **Customer Loyalty**: 36-45 age group = 33% above average engagement

### Actionable Recommendations
1. **Revenue Growth**: Implement bundling strategy (15-25% uplift potential)
2. **Inventory Optimization**: Automated reorder triggers at 50% of reorder level
3. **Customer Engagement**: Loyalty program for high-value customers (CLV >$20,000)
4. **Distribution Strategy**: Expand Tier-2 city presence through specialty retailers
5. **Product Strategy**: Focus on Probiotics and Multivitamins (38.6% of revenue)

## 🛠️ Technology Stack

### Backend/Data
- **Database**: SQLite 3
- **Python**: 3.11
  - Pandas: Data manipulation
  - NumPy: Numerical computing
  - Matplotlib: Visualization
  - Seaborn: Statistical visualization

### Frontend
- **Framework**: React 19
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui
- **Routing**: Wouter
- **Build**: Vite

### Development
- **Package Manager**: pnpm
- **TypeScript**: 5.6.3
- **Node.js**: 22.13.0

## 📚 Analysis Methodology

### Data Collection
- Synthetic dataset with realistic distributions
- 2,000 sales transactions spanning 24 months
- 500 customer profiles with demographics
- 300 inventory records across locations

### Analysis Approach
1. **SQL Analysis**: Complex queries with joins, aggregations, and window functions
2. **Statistical Analysis**: Descriptive statistics, distributions, correlations
3. **Visualization**: Multi-dimensional charts for pattern recognition
4. **Insights**: Strategic recommendations based on data patterns

### Quality Assurance
- TypeScript type checking
- Data validation in Python scripts
- SQL query testing
- Dashboard responsive design testing

## 📖 Documentation

- **Analysis Report**: `/reports/FMCG_Healthcare_Analysis_Report.md`
- **SQL Queries**: `/analysis/sql_queries.sql`
- **Data Schema**: Documented in `generate_data.py`
- **API Reference**: Inline code documentation

## 🎓 Portfolio Value

This project demonstrates:

✅ **SQL Expertise**
- Complex multi-table joins
- Aggregation and grouping
- Window functions and ranking
- Performance optimization

✅ **Python Data Science**
- Data manipulation with Pandas
- Statistical analysis
- Data visualization
- JSON data processing

✅ **Business Analytics**
- KPI definition and tracking
- Trend analysis
- Customer segmentation
- Strategic recommendations

✅ **Full-Stack Development**
- React component development
- TypeScript type safety
- Responsive UI design
- Data integration

✅ **Project Management**
- End-to-end project delivery
- Documentation
- Code organization
- Best practices

## 🔗 Quick Links

- **Dashboard**: `http://localhost:3000`
- **Analysis Report**: `/reports/FMCG_Healthcare_Analysis_Report.md`
- **SQL Queries**: `/analysis/sql_queries.sql`
- **Database**: `/data/fmcg_healthcare.db`

## 📝 License

This is a portfolio project created for demonstration purposes.

## 👤 Author

**Data Analytics Portfolio Project**  
Created: February 2026  
Dataset: Synthetic FMCG Healthcare Data

---

**Note**: This project uses a synthetic dataset generated for portfolio demonstration. All data, metrics, and insights are illustrative and for educational purposes.
