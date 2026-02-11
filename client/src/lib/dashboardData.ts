/**
 * Dashboard Data Utilities
 * Handles loading and processing of analysis data for the dashboard
 */

export interface KPI {
  label: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
}

export interface ChartData {
  name: string;
  value: number;
  percentage?: number;
}

export interface TableRow {
  [key: string]: string | number;
}

export interface AnalysisInsights {
  statistical_summary: any;
  sales_by_category: any[];
  monthly_trends: any[];
  top_products: any[];
  retailer_performance: any[];
  regional_sales: any[];
  customer_demographics: any[];
  inventory_status: any[];
}

let cachedInsights: AnalysisInsights | null = null;

export async function loadAnalysisInsights(): Promise<AnalysisInsights> {
  if (cachedInsights) {
    return cachedInsights as AnalysisInsights;
  }

  try {
    const response = await fetch('/analysis_insights.json');
    if (!response.ok) {
      throw new Error(`Failed to load insights: ${response.statusText}`);
    }
    const data = await response.json();
    cachedInsights = data;
    return data;
  } catch (error) {
    console.error('Error loading analysis insights:', error);
    throw error;
  }
}

export function getBusinessKPIs(insights: AnalysisInsights): KPI[] {
  const summary = insights.statistical_summary;
  
  return [
    {
      label: 'Total Revenue',
      value: `$${(summary.total_revenue / 1000000).toFixed(2)}M`,
      trend: 'up',
      change: '+12.5%'
    },
    {
      label: 'Total Transactions',
      value: summary.total_transactions.toLocaleString(),
      trend: 'up',
      change: '+8.3%'
    },
    {
      label: 'Avg Order Value',
      value: `$${summary.avg_transaction_value.toFixed(2)}`,
      trend: 'neutral',
      change: '+2.1%'
    },
    {
      label: 'Active Retailers',
      value: summary.active_retailers,
      trend: 'up',
      change: '+3'
    },
    {
      label: 'Products Sold',
      value: summary.products_sold,
      trend: 'neutral',
      change: '20 SKUs'
    },
    {
      label: 'Avg Discount Rate',
      value: `${summary.avg_discount_rate}%`,
      trend: 'down',
      change: '-0.5%'
    }
  ];
}

export function getSalesByCategoryData(insights: AnalysisInsights): ChartData[] {
  return insights.sales_by_category.map(item => ({
    name: item.category,
    value: item.revenue,
    percentage: item.revenue_pct
  }));
}

export function getTopProductsData(insights: AnalysisInsights): any[] {
  return insights.top_products.slice(0, 10).map(product => ({
    name: product.product_name,
    revenue: product.total_revenue,
    units: product.total_quantity,
    category: product.category
  }));
}

export function getMonthlyTrendsData(insights: AnalysisInsights): any[] {
  return insights.monthly_trends.map(item => ({
    month: item.month,
    revenue: item.monthly_revenue,
    transactions: item.transaction_count,
    units: item.units_sold,
    avgOrderValue: item.avg_order_value
  }));
}

export function getRetailerPerformanceData(insights: AnalysisInsights): any[] {
  return insights.retailer_performance.slice(0, 10).map(retailer => ({
    name: retailer.retailer_name,
    revenue: retailer.revenue,
    transactions: retailer.transactions,
    type: retailer.retailer_type,
    city: retailer.city
  }));
}

export function getRegionalSalesData(insights: AnalysisInsights): any[] {
  return insights.regional_sales.map(region => ({
    state: region.state,
    revenue: region.revenue,
    retailers: region.retailer_count,
    marketShare: region.market_share,
    revenuePerRetailer: region.revenue_per_retailer
  }));
}

export function getCustomerDemographicsData(insights: AnalysisInsights): any[] {
  return insights.customer_demographics.map(item => ({
    ageGroup: item.age_group,
    incomeLevel: item.income_level,
    customers: item.customer_count,
    purchases: item.total_purchases,
    avgPurchases: item.avg_purchases_per_customer
  }));
}

export function getInventoryStatusData(insights: AnalysisInsights): any[] {
  return insights.inventory_status.slice(0, 10).map(item => ({
    product: item.product_name,
    category: item.category,
    stock: item.total_stock,
    locations: item.retailer_locations,
    belowReorder: item.locations_below_reorder
  }));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(2)}%`;
}
