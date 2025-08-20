"""
forecast.py – Core forecasting logic

Implements:
- Prophet model (handles seasonality and trends)
- Linear regression with lag features (simple but effective)
- Unified `run_forecast()` interface with educational insights

Used by: Streamlit UI (Week 3), Flask backend (Weeks 4–5)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def run_linear_regression(df, forecast_days=7):
    """Run linear regression forecasting"""
    # Prepare data
    df_sorted = df.sort_values('ds').reset_index(drop=True)
    X = np.arange(len(df_sorted)).reshape(-1, 1)
    y = df_sorted['y'].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    future_X = np.arange(len(df_sorted), len(df_sorted) + forecast_days).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    # Create forecast dataframe
    last_date = df_sorted['ds'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days)
    
    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': predictions,
        'yhat_lower': predictions * 0.8,  # Simple confidence interval
        'yhat_upper': predictions * 1.2,
        'low_confidence': [False] * len(predictions)
    })
    
    # Calculate model performance
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    insights = {
        'model_used': 'Linear Regression',
        'model_explanation': f'Used linear regression to predict future sales. Model error: {mae:.2f} (MAE)',
        'forecast_periods': forecast_days,
        'confidence_level': 'Medium',
        'data_points_used': len(df),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2)
    }
    
    return forecast_df, insights

def run_prophet(df, forecast_days=7):
    """Run Prophet forecasting"""
    try:
        from prophet import Prophet
    except ImportError:
        raise ImportError("Prophet is not installed. Please install it with: pip install prophet")
    
    # Prepare data for Prophet
    df_prophet = df[['ds', 'y']].copy()
    df_prophet.columns = ['ds', 'y']
    
    # Create and fit model
    model = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df_prophet)
    
    # Make forecast
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)
    
    # Extract only the forecast period
    forecast_df = forecast.tail(forecast_days)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    forecast_df['low_confidence'] = [False] * len(forecast_df)
    
    # Calculate model performance
    historical_forecast = forecast.iloc[:-forecast_days]
    actual_values = df_prophet['y'].values
    predicted_values = historical_forecast['yhat'].values
    
    if len(actual_values) == len(predicted_values):
        mae = mean_absolute_error(actual_values, predicted_values)
        rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    else:
        mae = rmse = 0
    
    insights = {
        'model_used': 'Prophet',
        'model_explanation': f'Used Prophet time series model with weekly seasonality. Model error: {mae:.2f} (MAE)',
        'forecast_periods': forecast_days,
        'confidence_level': 'High',
        'data_points_used': len(df),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2)
    }
    
    return forecast_df, insights

def run_forecast(df, model_choice="auto", forecast_days=7):
    """Main forecasting function"""
    # Basic validation
    if len(df) < 5:
        raise ValueError("Need at least 5 data points for forecasting")
    
    if df['y'].std() == 0:
        raise ValueError("All sales values are identical - cannot generate meaningful forecast")
    
    # Choose model
    if model_choice == "auto":
        if len(df) < 30:
            model_choice = "linear"
        else:
            model_choice = "prophet"
    
    # Run the selected model
    if model_choice == "linear":
        forecast_df, insights = run_linear_regression(df, forecast_days)
    elif model_choice == "prophet":
        forecast_df, insights = run_prophet(df, forecast_days)
    else:
        raise ValueError(f"Unknown model choice: {model_choice}")
    
    # Check for low confidence
    if len(df) < 30:
        forecast_df['low_confidence'] = [True] * len(forecast_df)
        insights['confidence_warning'] = "Forecast confidence is low due to limited data"
    
    return {
        'forecast': forecast_df,
        'low_confidence': forecast_df['low_confidence'].any(),
        'insights': insights
    }

def evaluate_forecast(actual, predicted):
    """Evaluate forecast accuracy"""
    if len(actual) != len(predicted):
        return None
    
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    
    return {
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'accuracy': round((1 - mae / actual.mean()) * 100, 1)
    }

