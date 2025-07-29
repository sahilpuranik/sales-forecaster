import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Area,
  ComposedChart,
} from "recharts";

export default function ForecastChart({ data }) {
  if (!data?.length) return null;

  // Format dates for better display
  const formattedData = data.map(item => ({
    ...item,
    ds: new Date(item.ds).toLocaleDateString(),
    y: item.y || null, // Historical data
    yhat: item.yhat || null, // Forecast
    yhat_lower: item.yhat_lower || null,
    yhat_upper: item.yhat_upper || null,
  }));

  return (
    <div className="w-full bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Sales Forecast</h3>
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis 
              dataKey="ds" 
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
            />
            <YAxis fontSize={12} />
            <Tooltip 
              formatter={(value, name) => [
                value ? `$${value.toFixed(2)}` : 'N/A',
                name === 'y' ? 'Historical Sales' : 
                name === 'yhat' ? 'Forecast' : 
                name === 'yhat_lower' ? 'Lower Bound' :
                name === 'yhat_upper' ? 'Upper Bound' : name
              ]}
            />
            <Legend />
            
            {/* Historical data */}
            <Line 
              type="monotone" 
              dataKey="y" 
              stroke="#3b82f6" 
              strokeWidth={3} 
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              name="Historical Sales"
            />
            
            {/* Forecast line */}
            <Line 
              type="monotone" 
              dataKey="yhat" 
              stroke="#10b981" 
              strokeWidth={3} 
              strokeDasharray="5 5"
              dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              name="Forecast"
            />
            
            {/* Confidence interval */}
            <Area
              dataKey="yhat_upper"
              stackId="confidence"
              stroke="none"
              fill="#10b981"
              fillOpacity={0.1}
              name="Confidence Interval"
            />
            <Area
              dataKey="yhat_lower"
              stackId="confidence"
              stroke="none"
              fill="#10b981"
              fillOpacity={0.1}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>• <span className="text-blue-600 font-medium">Blue line:</span> Your historical sales data</p>
        <p>• <span className="text-green-600 font-medium">Green dashed line:</span> Predicted future sales</p>
        <p>• <span className="text-green-600 font-medium">Shaded area:</span> Confidence interval (prediction range)</p>
      </div>
    </div>
  );
}