import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { ScrollArea } from './ui/scroll-area';
import { Database, CheckCircle, TrendingUp } from 'lucide-react';

const sampleData = [
  { ds: '2023-01-01', y: 1500 },
  { ds: '2023-01-02', y: 1800 },
  { ds: '2023-01-03', y: 1200 },
  { ds: '2023-01-04', y: 2100 },
  { ds: '2023-01-05', y: 1900 },
  { ds: '2023-01-06', y: 1750 },
  { ds: '2023-01-07', y: 2200 },
  { ds: '2023-01-08', y: 1650 },
  { ds: '2023-01-09', y: 1950 },
  { ds: '2023-01-10', y: 2050 },
];

export function PreviewPage() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle>Sales Data Preview</CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[500px]">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date (ds)</TableHead>
                      <TableHead>Sales Value (y)</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sampleData.map((row, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-mono">{row.ds}</TableCell>
                        <TableCell>{row.y.toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Dataset Summary
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Records</span>
                <span className="text-lg font-semibold">15</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Date Range</span>
                <span className="text-lg font-semibold">15 days</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Average Sales</span>
                <span className="text-lg font-semibold">$1,800</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Data Quality
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Missing Values</span>
                <Badge variant="secondary">0%</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Outliers</span>
                <Badge variant="secondary">2 detected</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Data Consistency</span>
                <Badge variant="secondary" className="bg-green-100 text-green-800">Excellent</Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Forecast Readiness
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Dataset Size</span>
                <Badge variant="secondary" className="bg-green-100 text-green-800">Good</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Seasonality</span>
                <Badge variant="secondary">Weekly</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Confidence Level</span>
                <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">Medium</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
