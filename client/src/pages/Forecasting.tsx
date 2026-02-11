import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TrendingUp, AlertCircle, Target, Package } from 'lucide-react';
import Navigation from '@/components/Navigation';
import {
  loadForecastData,
  getRevenueForecastChartData,
  getCategoryForecastChartData,
  getInventoryForecastData,
  getQuarterlyComparisonData,
  getAccuracyMetrics,
  formatCurrency,
  formatNumber,
  formatPercentage,
  ForecastData,
} from '@/lib/forecastData';

export default function Forecasting() {
  const [forecast, setForecast] = useState<ForecastData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const data = await loadForecastData();
        setForecast(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load forecast data');
        console.error('Forecasting error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading forecast data...</p>
        </div>
      </div>
    );
  }

  if (error || !forecast) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Error Loading Forecasts</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error || 'Failed to load forecast data'}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const accuracyMetrics = getAccuracyMetrics(forecast);
  const revenueForecast = forecast.revenue_forecast;
  const quarterlyMetrics = forecast.quarterly_metrics;

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container py-6">
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <TrendingUp className="h-8 w-8 text-primary" />
            Predictive Analytics & Forecasting
          </h1>
          <p className="text-muted-foreground mt-2">Next Quarter Revenue and Inventory Forecasts</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-8">
        {/* Key Forecast Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Forecast Period
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{forecast.forecast_period}</p>
              <p className="text-xs text-muted-foreground mt-1">{forecast.forecast_horizon}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Forecast Revenue
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">
                {formatCurrency(forecast.summary.total_forecast_revenue)}
              </p>
              <p className={`text-xs mt-1 ${
                quarterlyMetrics.qoq_change_percent > 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {quarterlyMetrics.qoq_change_percent > 0 ? '+' : ''}
                {formatPercentage(quarterlyMetrics.qoq_change_percent)} QoQ
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Model Accuracy (MAE)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{accuracyMetrics.mae}</p>
              <p className="text-xs text-muted-foreground mt-1">
                MAPE: {accuracyMetrics.mape}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Confidence Level
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{accuracyMetrics.confidence}</p>
              <p className="text-xs text-muted-foreground mt-1">ARIMA(1,1,1) Model</p>
            </CardContent>
          </Card>
        </div>

        {/* Forecast Details Tabs */}
        <Tabs defaultValue="revenue" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="revenue">Revenue</TabsTrigger>
            <TabsTrigger value="category">Categories</TabsTrigger>
            <TabsTrigger value="inventory">Inventory</TabsTrigger>
            <TabsTrigger value="quarterly">Quarterly</TabsTrigger>
          </TabsList>

          {/* Revenue Forecast Tab */}
          <TabsContent value="revenue" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Revenue Forecast - Next 3 Months</CardTitle>
                <CardDescription>
                  ARIMA time-series forecast with 95% confidence intervals
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {/* Forecast Table */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b">
                          <th className="text-left py-2 px-2 font-semibold">Month</th>
                          <th className="text-right py-2 px-2 font-semibold">Forecast</th>
                          <th className="text-right py-2 px-2 font-semibold">Lower Bound</th>
                          <th className="text-right py-2 px-2 font-semibold">Upper Bound</th>
                        </tr>
                      </thead>
                      <tbody>
                        {revenueForecast.forecast_dates.map((date, idx) => (
                          <tr key={idx} className="border-b hover:bg-muted/50">
                            <td className="py-2 px-2">{date}</td>
                            <td className="text-right py-2 px-2 font-semibold">
                              {formatCurrency(revenueForecast.forecast_values[idx])}
                            </td>
                            <td className="text-right py-2 px-2 text-muted-foreground">
                              {formatCurrency(revenueForecast.lower_bound[idx])}
                            </td>
                            <td className="text-right py-2 px-2 text-muted-foreground">
                              {formatCurrency(revenueForecast.upper_bound[idx])}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Model Information */}
                  <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                    <div>
                      <p className="text-sm text-muted-foreground">Historical Average</p>
                      <p className="text-lg font-semibold">
                        {formatCurrency(revenueForecast.model_info.historical_avg)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Last Month Value</p>
                      <p className="text-lg font-semibold">
                        {formatCurrency(revenueForecast.model_info.last_value)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Standard Deviation</p>
                      <p className="text-lg font-semibold">
                        {formatCurrency(revenueForecast.model_info.historical_std)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Model Type</p>
                      <p className="text-lg font-semibold">{revenueForecast.model_info.model_type}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Accuracy Metrics */}
            <Card>
              <CardHeader>
                <CardTitle>Model Accuracy Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">MAE</p>
                    <p className="text-lg font-semibold">{accuracyMetrics.mae}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">RMSE</p>
                    <p className="text-lg font-semibold">
                      {formatCurrency(revenueForecast.rmse)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">MAPE</p>
                    <p className="text-lg font-semibold">{accuracyMetrics.mape}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Confidence</p>
                    <p className="text-lg font-semibold">{accuracyMetrics.confidence}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Category Forecast Tab */}
          <TabsContent value="category" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Revenue Forecast by Category</CardTitle>
                <CardDescription>
                  Predicted revenue for each product category in the next quarter
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {forecast.summary.top_forecast_categories.map(([category, data], idx) => (
                    <div key={idx} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-lg">{category}</h3>
                          <p className="text-sm text-muted-foreground">
                            Forecast Revenue: {formatCurrency(data.total_forecast)}
                          </p>
                        </div>
                        <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          data.growth_rate > 0
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {data.growth_rate > 0 ? '+' : ''}{formatPercentage(data.growth_rate)}
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Avg Monthly</p>
                          <p className="font-semibold">{formatCurrency(data.avg_monthly)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Growth Rate</p>
                          <p className="font-semibold">{formatPercentage(data.growth_rate)}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Inventory Forecast Tab */}
          <TabsContent value="inventory" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Inventory Requirements Forecast</CardTitle>
                <CardDescription>
                  Recommended stock levels for next quarter based on demand forecasts
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {getInventoryForecastData(forecast).map((item, idx) => (
                    <div key={idx} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold flex items-center gap-2">
                            <Package className="h-4 w-4" />
                            {item.product_name}
                          </h3>
                          <p className="text-sm text-muted-foreground">{item.category}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-lg">{formatNumber(item.total_required)}</p>
                          <p className="text-xs text-muted-foreground">units required</p>
                        </div>
                      </div>
                      <div className="grid grid-cols-3 gap-3 text-sm pt-3 border-t">
                        <div>
                          <p className="text-muted-foreground">Avg Monthly</p>
                          <p className="font-semibold">{formatNumber(item.avg_monthly_demand)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Reorder Point</p>
                          <p className="font-semibold">{formatNumber(item.reorder_point)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Safety Stock</p>
                          <p className="font-semibold">{formatNumber(item.safety_stock)}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Quarterly Comparison Tab */}
          <TabsContent value="quarterly" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Quarterly Performance Comparison</CardTitle>
                <CardDescription>
                  Historical quarterly data vs. forecasted Q1 2025
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {/* Quarterly Summary */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border rounded-lg p-4">
                      <p className="text-sm text-muted-foreground mb-2">Last Quarter Revenue</p>
                      <p className="text-3xl font-bold">
                        {formatCurrency(quarterlyMetrics.last_quarter_revenue)}
                      </p>
                    </div>
                    <div className="border rounded-lg p-4 bg-green-50">
                      <p className="text-sm text-muted-foreground mb-2">Forecast Q1 2025 Revenue</p>
                      <p className="text-3xl font-bold text-green-700">
                        {formatCurrency(quarterlyMetrics.forecast_quarter_revenue)}
                      </p>
                    </div>
                  </div>

                  {/* QoQ Change */}
                  <div className="border rounded-lg p-4 bg-blue-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground mb-2">Quarter-over-Quarter Change</p>
                        <p className="text-2xl font-bold text-blue-700">
                          {quarterlyMetrics.qoq_change_percent > 0 ? '+' : ''}
                          {formatPercentage(quarterlyMetrics.qoq_change_percent)}
                        </p>
                      </div>
                      <TrendingUp className={`h-12 w-12 ${
                        quarterlyMetrics.qoq_change_percent > 0 ? 'text-green-600' : 'text-red-600'
                      }`} />
                    </div>
                  </div>

                  {/* Monthly Average */}
                  <div className="border rounded-lg p-4">
                    <p className="text-sm text-muted-foreground mb-2">Forecast Monthly Average</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(quarterlyMetrics.forecast_monthly_avg)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Historical Quarters Table */}
            <Card>
              <CardHeader>
                <CardTitle>Historical Quarterly Data</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2 px-2 font-semibold">Quarter</th>
                        <th className="text-right py-2 px-2 font-semibold">Revenue</th>
                        <th className="text-right py-2 px-2 font-semibold">Units Sold</th>
                        <th className="text-right py-2 px-2 font-semibold">Transactions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {quarterlyMetrics.historical_quarters.map((quarter: any, idx: number) => (
                        <tr key={idx} className="border-b hover:bg-muted/50">
                          <td className="py-2 px-2">{quarter.quarter.toString()}</td>
                          <td className="text-right py-2 px-2 font-semibold">
                            {formatCurrency(quarter.revenue)}
                          </td>
                          <td className="text-right py-2 px-2">
                            {formatNumber(quarter.units_sold)}
                          </td>
                          <td className="text-right py-2 px-2">
                            {formatNumber(quarter.transaction_count)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Forecast Insights */}
        <Card className="mt-8 border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-blue-900">
              <AlertCircle className="h-5 w-5" />
              Forecast Insights & Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent className="text-blue-900">
            <ul className="space-y-2 list-disc list-inside">
              <li>
                Revenue is forecasted to grow by {formatPercentage(quarterlyMetrics.qoq_change_percent)} QoQ,
                reaching {formatCurrency(quarterlyMetrics.forecast_quarter_revenue)} in Q1 2025
              </li>
              <li>
                The ARIMA(1,1,1) model shows strong accuracy with MAE of {accuracyMetrics.mae},
                providing reliable forecasts at {accuracyMetrics.confidence} confidence level
              </li>
              <li>
                Top forecast categories are {forecast.summary.top_forecast_categories[0][0]},
                {forecast.summary.top_forecast_categories[1][0]}, and
                {forecast.summary.top_forecast_categories[2][0]}
              </li>
              <li>
                Inventory planning should prioritize high-demand items with adequate safety stock
                to meet forecasted demand while minimizing carrying costs
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="mt-12 pt-8 border-t text-center text-muted-foreground text-sm">
          <p>Predictive Analytics Report | Generated: {new Date(forecast.timestamp).toLocaleDateString()}</p>
          <p className="mt-2">ARIMA Time-Series Forecasting Model | 95% Confidence Intervals</p>
        </div>
      </div>
    </div>
  );
}
