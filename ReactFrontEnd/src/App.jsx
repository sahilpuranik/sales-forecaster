import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import PreviewTable from "./components/PreviewTable";
import ForecastChart from "./components/ForecastChart";
import { forecast } from "./api";

export default function App() {
  const [previewRows, setPreviewRows] = useState([]);
  const [forecastRows, setForecastRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runForecast = async () => {
    setLoading(true);
    setError("");
    try {
      const { forecast: rows } = await forecast(previewRows);
      setForecastRows(rows);
    } catch (err) {
      const errorMessage = err?.response?.data?.message ?? "Forecast failed. Please try again.";
      setError(errorMessage);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              📊 Sales Forecaster
            </h1>
            <p className="text-lg text-gray-600">
              Upload your sales data and get AI-powered forecasts in seconds
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Step 1: Upload */}
        <div className="mb-12">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full mb-4">
              <span className="text-2xl">📁</span>
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Step 1: Upload Your Data</h2>
            <p className="text-gray-600">
              Upload a CSV file with your sales data. We'll automatically detect date and sales columns.
            </p>
          </div>
          <UploadForm onPreview={setPreviewRows} />
        </div>

        {/* Step 2: Preview */}
        {previewRows.length > 0 && (
          <div className="mb-12">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mb-4">
                <span className="text-2xl">👀</span>
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Step 2: Review Your Data</h2>
              <p className="text-gray-600">
                Here's how your data looks after cleaning. Make sure everything looks correct.
              </p>
            </div>
            <PreviewTable rows={previewRows} />
          </div>
        )}

        {/* Step 3: Forecast */}
        {previewRows.length > 0 && (
          <div className="mb-12">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-100 rounded-full mb-4">
                <span className="text-2xl">🔮</span>
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Step 3: Generate Forecast</h2>
              <p className="text-gray-600">
                Click the button below to generate your sales forecast using AI.
              </p>
            </div>
            
            <div className="text-center">
              <button
                onClick={runForecast}
                disabled={loading}
                className="inline-flex items-center px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-lg hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating Forecast...
                  </>
                ) : (
                  <>
                    <span className="mr-2">🚀</span>
                    Generate Forecast
                  </>
                )}
              </button>
              
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Step 4: Results */}
        {forecastRows.length > 0 && (
          <div className="mb-12">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-emerald-100 rounded-full mb-4">
                <span className="text-2xl">📈</span>
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Step 4: Your Forecast Results</h2>
              <p className="text-gray-600">
                Here's your AI-generated sales forecast with confidence intervals.
              </p>
            </div>
            <ForecastChart data={forecastRows} />
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>Built with ❤️ for small businesses</p>
            <p className="mt-1">Upload your CSV • Get instant forecasts • Make better decisions</p>
          </div>
        </div>
      </div>
    </div>
  );
}