import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download, TrendingUp, Target, Calendar } from 'lucide-react';

const generateForecastData = (days: number) => {
  const historicalData = [
    { date: '2023-01-01', historical: 1500, forecast: null },
    { date: '2023-01-02', historical: 1800, forecast: null },
    { date: '2023-01-03', historical: 1200, forecast: null },
    { date: '2023-01-04', historical: 2100, forecast: null },
    { date: '2023-01-05', historical: 1900, forecast: null },
    { date: '2023-01-06', historical: 1750, forecast: null },
    { date: '2023-01-07', historical: 2200, forecast: null },
    { date: '2023-01-08', historical: 1650, forecast: null },
    { date: '2023-01-09', historical: 1950, forecast: null },
    { date: '2023-01-10', historical: 2050, forecast: null },
    { date: '2023-01-11', historical: 1400, forecast: null },
    { date: '2023-01-12', historical: 1600, forecast: null },
    { date: '2023-01-13', historical: 1850, forecast: null },
    { date: '2023-01-14', historical: 2300, forecast: null },
    { date: '2023-01-15', historical: 1700, forecast: null }
  ];

  const forecastData = [];
  const baseValue = 1800;
  const trend = 20;
  
  for (let i = 0; i < days; i++) {
    const date = new Date(2023, 0, 16 + i);
    const formattedDate = date.toISOString().split('T')[0];
    const forecastValue = Math.round(
      baseValue + (trend * i) + (Math.sin(i * 0.5) * 200) + (Math.random() - 0.5) * 100
    );
    
    forecastData.push({
      date: formattedDate,
      historical: null,
      forecast: forecastValue
    });
  }

  return [...historicalData, ...forecastData];
};

export function ForecastPage() {
  const [forecastDays, setForecastDays] = useState('7');
  const [data, setData] = useState(() => generateForecastData(7));

  const handleForecastDaysChange = (value: string) => {
    setForecastDays(value);
    setData(generateForecastData(parseInt(value)));
  };

  const forecastValues = data.filter(d => d.forecast !== null).map(d => d.forecast!);
  const avgForecast = Math.round(forecastValues.reduce((sum, val) => sum + val, 0) / forecastValues.length);
  const totalForecast = forecastValues.reduce((sum, val) => sum + val, 0);

  const handleDownloadCSV = () => {
    const csv = [
      'date,type,value',
      ...data.map(d => {
        if (d.historical !== null) {
          return `${d.date},historical,${d.historical}`;
        } else {
          return `${d.date},forecast,${d.forecast}`;
        }
      })
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sales_forecast_${forecastDays}_days.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Sales Forecast</h2>
        <div className="flex items-center gap-4">
          <Select value={forecastDays} onValueChange={handleForecastDaysChange}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Forecast period" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">7 days</SelectItem>
              <SelectItem value="14">14 days</SelectItem>
              <SelectItem value="30">30 days</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleDownloadCSV} variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Download CSV
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="h-[500px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => new Date(value).toLocaleDateString()} 
                />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip 
                  formatter={(value, name) => [
                    typeof value === 'number' ? value.toLocaleString() : value,
                    name === 'historical' ? 'Historical Sales' : 'Forecasted Sales'
                  ]}
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="historical" 
                  stroke="hsl(var(--chart-1))" 
                  strokeWidth={3}
                  name="Historical Sales"
                  dot={{ fill: 'hsl(var(--chart-1))', strokeWidth: 2, r: 4 }}
                  connectNulls={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="forecast" 
                  stroke="hsl(var(--chart-2))" 
                  strokeWidth={3}
                  strokeDasharray="5 5"
                  name="Forecasted Sales"
                  dot={{ fill: 'hsl(var(--chart-2))', strokeWidth: 2, r: 4 }}
                  connectNulls={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg">Average Daily Sales</CardTitle>
            <TrendingUp className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{avgForecast.toLocaleString()}</div>
            <p className="text-muted-foreground">Next {forecastDays} days</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg">Total Forecast</CardTitle>
            <Target className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{totalForecast.toLocaleString()}</div>
            <p className="text-muted-foreground">{forecastDays} day period</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg">Forecast Period</CardTitle>
            <Calendar className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{forecastDays}</div>
            <p className="text-muted-foreground">Days ahead</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
