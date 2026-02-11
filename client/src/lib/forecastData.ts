/**
 * Forecasting Data Utilities
 * Handles loading and processing of predictive analytics forecast data
 */

export interface ForecastData {
  timestamp: string;
  forecast_period: string;
  forecast_horizon: string;
  revenue_forecast: {
    forecast_dates: string[];
    forecast_values: number[];
    lower_bound: number[];
    upper_bound: number[];
    mae: number;
    rmse: number;
    model_info: {
      model_type: string;
      historical_avg: number;
      historical_std: number;
      last_value: number;
    };
  };
  inventory_forecast: {
    [key: string]: {
      product_name: string;
      category: string;
      forecast_units: number[];
      avg_monthly_demand: number;
      reorder_point: number;
      safety_stock: number;
      total_required: number;
    };
  };
  category_forecast: {
    [key: string]: {
      forecast_revenue: number[];
      total_forecast: number;
      avg_monthly: number;
      growth_rate: number;
    };
  };
  quarterly_metrics: {
    forecast_quarter_revenue: number;
    forecast_monthly_avg: number;
    last_quarter_revenue: number;
    qoq_change_percent: number;
    historical_quarters: any[];
  };
  summary: {
    total_forecast_revenue: number;
    confidence_level: string;
    model_accuracy: {
      mae: number;
      rmse: number;
    };
    top_forecast_categories: [string, any][];
  };
}

let cachedForecast: ForecastData | null = null;

export async function loadForecastData(): Promise<ForecastData> {
  if (cachedForecast) {
    return cachedForecast as ForecastData;
  }

  try {
    const response = await fetch('/forecast_report.json');
    if (!response.ok) {
      throw new Error(`Failed to load forecast data: ${response.statusText}`);
    }
    const data = await response.json();
    cachedForecast = data;
    return data;
  } catch (error) {
    console.error('Error loading forecast data:', error);
    throw error;
  }
}

export function getRevenueForecastChartData(forecast: ForecastData) {
  return {
    labels: forecast.revenue_forecast.forecast_dates,
    datasets: [
      {
        label: 'Forecast Revenue',
        data: forecast.revenue_forecast.forecast_values,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Upper Bound (95% CI)',
        data: forecast.revenue_forecast.upper_bound,
        borderColor: '#10b981',
        borderDash: [5, 5],
        borderWidth: 1,
        fill: false,
        tension: 0.4,
      },
      {
        label: 'Lower Bound (95% CI)',
        data: forecast.revenue_forecast.lower_bound,
        borderColor: '#ef4444',
        borderDash: [5, 5],
        borderWidth: 1,
        fill: false,
        tension: 0.4,
      },
    ],
  };
}

export function getCategoryForecastChartData(forecast: ForecastData) {
  const categories = Object.keys(forecast.category_forecast);
  const revenues = categories.map(cat => forecast.category_forecast[cat].total_forecast);

  return {
    labels: categories,
    datasets: [
      {
        label: 'Forecast Revenue by Category',
        data: revenues,
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#ef4444',
          '#8b5cf6',
          '#ec4899',
        ],
        borderColor: '#fff',
        borderWidth: 2,
      },
    ],
  };
}

export function getInventoryForecastData(forecast: ForecastData) {
  const items = Object.entries(forecast.inventory_forecast)
    .map(([id, data]) => ({
      id,
      ...data,
    }))
    .sort((a, b) => b.total_required - a.total_required)
    .slice(0, 10);

  return items;
}

export function getQuarterlyComparisonData(forecast: ForecastData) {
  const historical = forecast.quarterly_metrics.historical_quarters;
  const lastQuarter = historical[historical.length - 1];
  const forecastQuarter = {
    quarter: 'Q1 2025 (Forecast)',
    revenue: forecast.quarterly_metrics.forecast_quarter_revenue,
    units_sold: 0,
    transaction_count: 0,
    avg_order_value: 0,
  };

  return {
    labels: [...historical.slice(-4).map((q: any) => q.quarter.toString()), forecastQuarter.quarter],
    datasets: [
      {
        label: 'Quarterly Revenue',
        data: [
          ...historical.slice(-4).map((q: any) => q.revenue),
          forecastQuarter.revenue,
        ],
        backgroundColor: [
          '#3b82f6',
          '#3b82f6',
          '#3b82f6',
          '#3b82f6',
          '#10b981',
        ],
        borderColor: '#fff',
        borderWidth: 2,
      },
    ],
  };
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(2)}%`;
}

export function getAccuracyMetrics(forecast: ForecastData) {
  const mae = forecast.revenue_forecast.mae;
  const rmse = forecast.revenue_forecast.rmse;
  const avgRevenue = forecast.revenue_forecast.model_info.historical_avg;

  return {
    mae: formatCurrency(mae),
    rmse: formatCurrency(rmse),
    mape: formatPercentage((mae / avgRevenue) * 100),
    confidence: forecast.summary.confidence_level,
  };
}
