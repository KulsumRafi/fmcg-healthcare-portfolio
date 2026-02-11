"""
Predictive Analytics Module for FMCG Healthcare Portfolio
Implements ARIMA time-series forecasting for revenue and inventory requirements
"""

import sqlite3
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Database path
DB_PATH = '/home/ubuntu/fmcg-healthcare-portfolio/data/fmcg_healthcare.db'

def load_monthly_data():
    """Load monthly sales data from database"""
    conn = sqlite3.connect(DB_PATH)
    
    query = """
    SELECT 
        strftime('%Y-%m', sale_date) as month,
        SUM(total_amount) as revenue,
        SUM(quantity_sold) as units_sold,
        COUNT(*) as transaction_count,
        AVG(total_amount) as avg_order_value
    FROM sales
    GROUP BY strftime('%Y-%m', sale_date)
    ORDER BY month
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['month'] = pd.to_datetime(df['month'])
    return df.sort_values('month')

def load_product_monthly_data():
    """Load monthly product-level inventory data"""
    conn = sqlite3.connect(DB_PATH)
    
    query = """
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        strftime('%Y-%m', s.sale_date) as month,
        SUM(s.quantity_sold) as units_sold,
        SUM(s.total_amount) as revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.product_id, strftime('%Y-%m', s.sale_date)
    ORDER BY p.product_id, month
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['month'] = pd.to_datetime(df['month'])
    return df

def fit_arima_model(timeseries, order=(1, 1, 1)):
    """Fit ARIMA model to time series data"""
    try:
        model = ARIMA(timeseries, order=order)
        fitted_model = model.fit()
        return fitted_model
    except Exception as e:
        print(f"Error fitting ARIMA model: {e}")
        return None

def forecast_revenue(monthly_data, periods=3):
    """Forecast revenue for next 3 months using ARIMA"""
    revenue_series = monthly_data['revenue'].values
    
    # Fit ARIMA model
    model = fit_arima_model(revenue_series, order=(1, 1, 1))
    
    if model is None:
        return None
    
    forecast_result = model.get_forecast(steps=periods)
    forecast_values = forecast_result.predicted_mean
    conf_int = forecast_result.conf_int()
    
    last_month = monthly_data['month'].max()
    forecast_dates = [last_month + timedelta(days=30*i) for i in range(1, periods+1)]
    
    mae = mean_absolute_error(revenue_series[-3:], model.fittedvalues[-3:])
    rmse = np.sqrt(mean_squared_error(revenue_series[-3:], model.fittedvalues[-3:]))
    
    if hasattr(conf_int, 'iloc'):
        lower_bound = conf_int.iloc[:, 0].tolist()
        upper_bound = conf_int.iloc[:, 1].tolist()
    else:
        lower_bound = conf_int[:, 0].tolist()
        upper_bound = conf_int[:, 1].tolist()
    
    return {
        'forecast_dates': [d.strftime('%Y-%m') for d in forecast_dates],
        'forecast_values': forecast_values.tolist(),
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'mae': float(mae),
        'rmse': float(rmse),
        'model_info': {
            'model_type': 'ARIMA(1,1,1)',
            'historical_avg': float(revenue_series.mean()),
            'historical_std': float(revenue_series.std()),
            'last_value': float(revenue_series[-1])
        }
    }

def forecast_inventory_requirements(monthly_data, product_data, periods=3):
    """Forecast inventory requirements for next quarter"""
    
    # Group by product and forecast top products
    top_products = product_data.groupby('product_id')['units_sold'].sum().nlargest(10).index.tolist()
    
    forecasts = {}
    
    for product_id in top_products:
        product_series = product_data[product_data['product_id'] == product_id].sort_values('month')
        
        if len(product_series) < 3:
            continue
        
        product_name = product_series['product_name'].iloc[0]
        category = product_series['category'].iloc[0]
        units_series = product_series['units_sold'].values
        
        # Fit ARIMA model
        model = fit_arima_model(units_series, order=(1, 1, 1))
        
        if model is None:
            continue
        
        # Forecast
        forecast_result = model.get_forecast(steps=periods)
        forecast_values = forecast_result.predicted_mean
        
        # Calculate reorder point (mean + 1 std dev)
        avg_units = units_series.mean()
        std_units = units_series.std()
        reorder_point = avg_units + std_units
        
        # Calculate safety stock
        safety_stock = std_units * 1.65  # 95% service level
        
        forecasts[str(product_id)] = {
            'product_name': product_name,
            'category': category,
            'forecast_units': forecast_values.tolist(),
            'avg_monthly_demand': float(avg_units),
            'reorder_point': float(reorder_point),
            'safety_stock': float(safety_stock),
            'total_required': float(forecast_values.sum() + safety_stock)
        }
    
    return forecasts

def forecast_by_category(product_data, periods=3):
    """Forecast revenue by category for next quarter"""
    categories = product_data['category'].unique()
    category_forecasts = {}
    
    for category in categories:
        category_data = product_data[product_data['category'] == category].sort_values('month')
        category_revenue = category_data.groupby('month')['revenue'].sum().values
        
        if len(category_revenue) < 3:
            continue
        
        model = fit_arima_model(category_revenue, order=(1, 1, 1))
        
        if model is None:
            continue
        
        forecast_result = model.get_forecast(steps=periods)
        forecast_values = forecast_result.predicted_mean
        
        category_forecasts[category] = {
            'forecast_revenue': forecast_values.tolist(),
            'total_forecast': float(forecast_values.sum()),
            'avg_monthly': float(category_revenue.mean()),
            'growth_rate': float((forecast_values.mean() - category_revenue.mean()) / category_revenue.mean() * 100)
        }
    
    return category_forecasts

def calculate_quarterly_metrics(monthly_data, revenue_forecast):
    """Calculate quarterly metrics and comparisons"""
    
    # Historical quarterly data
    monthly_data['quarter'] = monthly_data['month'].dt.to_period('Q')
    quarterly_data = monthly_data.groupby('quarter').agg({
        'revenue': 'sum',
        'units_sold': 'sum',
        'transaction_count': 'sum',
        'avg_order_value': 'mean'
    }).reset_index()
    
    # Calculate forecast quarter metrics
    forecast_revenue_total = sum(revenue_forecast['forecast_values'])
    forecast_avg = forecast_revenue_total / 3
    
    # Compare with last quarter
    last_quarter_revenue = quarterly_data['revenue'].iloc[-1]
    qoq_change = ((forecast_revenue_total - last_quarter_revenue) / last_quarter_revenue) * 100
    
    return {
        'forecast_quarter_revenue': float(forecast_revenue_total),
        'forecast_monthly_avg': float(forecast_avg),
        'last_quarter_revenue': float(last_quarter_revenue),
        'qoq_change_percent': float(qoq_change),
        'historical_quarters': quarterly_data.to_dict('records')
    }

def generate_forecasting_report():
    """Generate comprehensive forecasting report"""
    
    print("Loading data...")
    monthly_data = load_monthly_data()
    product_data = load_product_monthly_data()
    
    print("Forecasting revenue...")
    revenue_forecast = forecast_revenue(monthly_data, periods=3)
    
    print("Forecasting inventory requirements...")
    inventory_forecast = forecast_inventory_requirements(monthly_data, product_data, periods=3)
    
    print("Forecasting by category...")
    category_forecast = forecast_by_category(product_data, periods=3)
    
    print("Calculating quarterly metrics...")
    quarterly_metrics = calculate_quarterly_metrics(monthly_data, revenue_forecast)
    
    # Compile report
    report = {
        'timestamp': datetime.now().isoformat(),
        'forecast_period': 'Q1 2025 (Next Quarter)',
        'forecast_horizon': '3 months',
        'revenue_forecast': revenue_forecast,
        'inventory_forecast': inventory_forecast,
        'category_forecast': category_forecast,
        'quarterly_metrics': quarterly_metrics,
        'summary': {
            'total_forecast_revenue': revenue_forecast['forecast_values'][0] + 
                                     revenue_forecast['forecast_values'][1] + 
                                     revenue_forecast['forecast_values'][2],
            'confidence_level': '95%',
            'model_accuracy': {
                'mae': revenue_forecast['mae'],
                'rmse': revenue_forecast['rmse']
            },
            'top_forecast_categories': sorted(
                category_forecast.items(),
                key=lambda x: x[1]['total_forecast'],
                reverse=True
            )[:3]
        }
    }
    
    return report

def save_forecast_report(report, output_path):
    """Save forecast report to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"Forecast report saved to {output_path}")

def main():
    """Main execution"""
    print("="*60)
    print("FMCG Healthcare Predictive Analytics")
    print("Revenue and Inventory Forecasting")
    print("="*60)
    
    # Generate report
    report = generate_forecasting_report()
    
    # Save report
    output_path = '/home/ubuntu/fmcg-healthcare-portfolio/analysis/forecast_report.json'
    save_forecast_report(report, output_path)
    
    # Print summary
    print("\n" + "="*60)
    print("FORECAST SUMMARY")
    print("="*60)
    print(f"\nRevenue Forecast (Next 3 Months):")
    for date, value in zip(report['revenue_forecast']['forecast_dates'],
                           report['revenue_forecast']['forecast_values']):
        print(f"  {date}: ${value:,.2f}")
    
    print(f"\nTotal Forecast Revenue: ${report['summary']['total_forecast_revenue']:,.2f}")
    print(f"Last Quarter Revenue: ${report['quarterly_metrics']['last_quarter_revenue']:,.2f}")
    print(f"QoQ Change: {report['quarterly_metrics']['qoq_change_percent']:.2f}%")
    
    print(f"\nModel Accuracy:")
    print(f"  MAE: ${report['summary']['model_accuracy']['mae']:,.2f}")
    print(f"  RMSE: ${report['summary']['model_accuracy']['rmse']:,.2f}")
    
    print(f"\nTop Forecast Categories:")
    for i, (category, forecast) in enumerate(report['summary']['top_forecast_categories'], 1):
        print(f"  {i}. {category}: ${forecast['total_forecast']:,.2f}")
    
    print(f"\nTop Inventory Forecast Items (by required units):")
    sorted_inventory = sorted(
        report['inventory_forecast'].items(),
        key=lambda x: x[1]['total_required'],
        reverse=True
    )[:5]
    for product_id, forecast in sorted_inventory:
        print(f"  {forecast['product_name']}: {forecast['total_required']:.0f} units")
    
    print("\n" + "="*60)
    print("Forecast report saved successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
