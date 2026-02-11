import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TrendingUp, TrendingDown, BarChart3, Users, Package, MapPin } from 'lucide-react';
import Navigation from '@/components/Navigation';
import {
  loadAnalysisInsights,
  getBusinessKPIs,
  getSalesByCategoryData,
  getTopProductsData,
  getMonthlyTrendsData,
  getRetailerPerformanceData,
  getRegionalSalesData,
  getCustomerDemographicsData,
  getInventoryStatusData,
  formatCurrency,
  formatNumber,
  AnalysisInsights,
  KPI
} from '@/lib/dashboardData';

export default function Dashboard() {
  const [insights, setInsights] = useState<AnalysisInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [kpis, setKpis] = useState<KPI[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const data = await loadAnalysisInsights();
        setInsights(data);
        setKpis(getBusinessKPIs(data));
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
        console.error('Dashboard error:', err);
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
          <p className="text-muted-foreground">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error || !insights) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Error Loading Dashboard</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error || 'Failed to load analysis data'}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container py-6">
          <h1 className="text-3xl font-bold tracking-tight">FMCG Healthcare Analytics</h1>
          <p className="text-muted-foreground mt-2">Comprehensive data analysis dashboard</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {kpis.map((kpi, index) => (
            <Card key={index}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {kpi.label}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-end justify-between">
                  <div>
                    <p className="text-2xl font-bold">{kpi.value}</p>
                    {kpi.change && (
                      <p className={`text-xs mt-1 ${
                        kpi.trend === 'up' ? 'text-green-600' : 
                        kpi.trend === 'down' ? 'text-red-600' : 
                        'text-gray-600'
                      }`}>
                        {kpi.change}
                      </p>
                    )}
                  </div>
                  <div className="text-muted-foreground">
                    {kpi.trend === 'up' && <TrendingUp className="h-4 w-4 text-green-600" />}
                    {kpi.trend === 'down' && <TrendingDown className="h-4 w-4 text-red-600" />}
                    {kpi.trend === 'neutral' && <BarChart3 className="h-4 w-4" />}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Tabs for different analysis sections */}
        <Tabs defaultValue="sales" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="sales">Sales</TabsTrigger>
            <TabsTrigger value="products">Products</TabsTrigger>
            <TabsTrigger value="retail">Retail</TabsTrigger>
            <TabsTrigger value="customers">Customers</TabsTrigger>
            <TabsTrigger value="inventory">Inventory</TabsTrigger>
          </TabsList>

          {/* Sales Tab */}
          <TabsContent value="sales" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Sales by Category</CardTitle>
                <CardDescription>Revenue distribution across product categories</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/sales_by_category.png" 
                    alt="Sales by Category" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Monthly Sales Trends</CardTitle>
                <CardDescription>24-month revenue and transaction analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/monthly_trends.png" 
                    alt="Monthly Trends" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Sales Performance Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {insights.sales_by_category.map((category, idx) => (
                    <div key={idx} className="flex items-center justify-between pb-2 border-b last:border-0">
                      <div>
                        <p className="font-medium">{category.category}</p>
                        <p className="text-sm text-muted-foreground">
                          {formatNumber(category.transactions)} transactions
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{formatCurrency(category.revenue)}</p>
                        <p className="text-sm text-muted-foreground">{category.revenue_pct}%</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Products Tab */}
          <TabsContent value="products" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Top Products</CardTitle>
                <CardDescription>Best-performing products by revenue</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/top_products.png" 
                    alt="Top Products" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Top 10 Products Detail</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {getTopProductsData(insights).map((product, idx) => (
                    <div key={idx} className="flex items-center justify-between pb-3 border-b last:border-0">
                      <div>
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-muted-foreground">{product.category}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{formatCurrency(product.revenue)}</p>
                        <p className="text-sm text-muted-foreground">{formatNumber(product.units)} units</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Retail Tab */}
          <TabsContent value="retail" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Retailer Performance</CardTitle>
                <CardDescription>Top retailers by revenue and efficiency</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/retailer_performance.png" 
                    alt="Retailer Performance" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Regional Sales Distribution</CardTitle>
                <CardDescription>Sales performance by state</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/regional_sales.png" 
                    alt="Regional Sales" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Regional Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {getRegionalSalesData(insights).map((region, idx) => (
                    <div key={idx} className="flex items-center justify-between pb-3 border-b last:border-0">
                      <div>
                        <p className="font-medium flex items-center gap-2">
                          <MapPin className="h-4 w-4" />
                          {region.state}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {formatNumber(region.retailers)} retailers
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{formatCurrency(region.revenue)}</p>
                        <p className="text-sm text-muted-foreground">{region.marketShare}% share</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Customers Tab */}
          <TabsContent value="customers" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Customer Demographics</CardTitle>
                <CardDescription>Customer segmentation and purchasing behavior</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/customer_demographics.png" 
                    alt="Customer Demographics" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Customer Segments</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {getCustomerDemographicsData(insights).slice(0, 10).map((segment, idx) => (
                    <div key={idx} className="flex items-center justify-between pb-3 border-b last:border-0">
                      <div>
                        <p className="font-medium flex items-center gap-2">
                          <Users className="h-4 w-4" />
                          {segment.ageGroup} - {segment.incomeLevel}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {formatNumber(segment.customers)} customers
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{formatNumber(segment.purchases)} purchases</p>
                        <p className="text-sm text-muted-foreground">
                          {segment.avgPurchases.toFixed(2)} avg
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Inventory Tab */}
          <TabsContent value="inventory" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Inventory Status</CardTitle>
                <CardDescription>Current stock levels and reorder analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full">
                  <img 
                    src="/inventory_status.png" 
                    alt="Inventory Status" 
                    className="w-full h-auto rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Product Inventory</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {getInventoryStatusData(insights).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between pb-3 border-b last:border-0">
                      <div>
                        <p className="font-medium flex items-center gap-2">
                          <Package className="h-4 w-4" />
                          {item.product}
                        </p>
                        <p className="text-sm text-muted-foreground">{item.category}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{formatNumber(item.stock)} units</p>
                        <p className="text-sm text-muted-foreground">
                          {item.locations} locations
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="mt-12 pt-8 border-t text-center text-muted-foreground text-sm">
          <p>FMCG Healthcare Analytics Dashboard | Data Analysis Period: Jan 2023 - Dec 2024</p>
          <p className="mt-2">Synthetic dataset for portfolio demonstration</p>
        </div>
      </div>
    </div>
  );
}
