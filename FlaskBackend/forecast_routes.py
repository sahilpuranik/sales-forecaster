"""
Blueprint handling the /forecast endpoint.
"""

import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, request, jsonify
from App.forecast import run_forecast

forecast_bp = Blueprint("forecast", __name__)

def validate_forecast_data(data):
    """Validate that data is suitable for forecasting"""
    if not data or len(data) < 5:
        return False, "Need at least 5 data points for forecasting"
    
    # Check for required columns
    if not all('ds' in row and 'y' in row for row in data):
        return False, "Data must have 'ds' (date) and 'y' (sales) columns"
    
    # Check for numeric sales values
    try:
        sales_values = [float(row['y']) for row in data]
        if all(x == sales_values[0] for x in sales_values):
            return False, "All sales values are identical - cannot forecast"
    except (ValueError, TypeError):
        return False, "Sales values must be numeric"
    
    return True, ""

@forecast_bp.route("/", methods=["POST"])
def generate_forecast():
    """Generate sales forecast from cleaned data"""
    
    try:
        # Get request data
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"error": "No data provided"}), 400
        
        data = request_data.get('data', [])
        model_choice = request_data.get('model', 'auto')
        forecast_days = request_data.get('periods', 7)
        
        # Validate input data
        is_valid, error_msg = validate_forecast_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        df['ds'] = pd.to_datetime(df['ds'])
        df['y'] = pd.to_numeric(df['y'])
        
        # Generate forecast
        result = run_forecast(df, model_choice, forecast_days)
        
        # Convert forecast to list of dictionaries
        forecast_list = []
        for _, row in result['forecast'].iterrows():
            forecast_dict = {
                'ds': row['ds'].strftime('%Y-%m-%d'),
                'yhat': float(row['yhat']),
                'yhat_lower': float(row['yhat_lower']),
                'yhat_upper': float(row['yhat_upper']),
                'low_confidence': bool(row['low_confidence'])
            }
            forecast_list.append(forecast_dict)
        
        response = {
            "success": True,
            "forecast": forecast_list,
            "message": f"Successfully generated {len(forecast_list)} days of forecasts",
            "insights": result['insights']
        }
        
        # Add warning if confidence is low
        if result['low_confidence']:
            response['warning'] = "Forecast confidence is low due to limited data"
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error generating forecast: {str(e)}"}), 500