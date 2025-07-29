import React from "react";

export default function PreviewTable({ rows }) {
  if (!rows?.length) return null;

  const formatValue = (key, value) => {
    if (key === 'ds') {
      return new Date(value).toLocaleDateString();
    }
    if (key === 'y' && typeof value === 'number') {
      return `$${value.toFixed(2)}`;
    }
    return value;
  };

  const getColumnLabel = (key) => {
    return key === 'ds' ? 'Date' : key === 'y' ? 'Sales Amount' : key;
  };

  const headers = Object.keys(rows[0]);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800">Cleaned Data Preview</h3>
        <p className="text-sm text-gray-600 mt-1">
          Your data has been automatically cleaned and formatted for forecasting
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {headers.map((h) => (
                <th
                  key={h}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {getColumnLabel(h)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {rows.slice(0, 10).map((row, i) => (
              <tr key={i} className="hover:bg-gray-50 transition-colors">
                {headers.map((h) => (
                  <td key={h} className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {formatValue(h, row[h])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Showing first {Math.min(10, rows.length)} of {rows.length} rows
          {rows.length > 10 && " • All data will be used for forecasting"}
        </p>
      </div>
    </div>
  );
}