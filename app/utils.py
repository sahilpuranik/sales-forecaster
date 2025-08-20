import pandas as pd
import numpy as np
from typing import Literal

def detect_seasonality(df):
    """Check if data has weekly patterns by looking at day-of-week sales"""
    df_copy = df.copy()
    df_copy['ds'] = pd.to_datetime(df_copy['ds'])
    df_copy['day_of_week'] = df_copy['ds'].dt.dayofweek
    
    # Calculate average sales for each day of the week
    daily_avg = df_copy.groupby('day_of_week')['y'].mean()
    
    # If there's significant variation between days, it's seasonal
    variation = daily_avg.std() / daily_avg.mean()
    return variation > 0.2

def select_model(df, model_choice):
    """Choose which forecasting model to use based on data and user choice"""
    if model_choice != "auto":
        return model_choice
    
    # For small datasets, use linear regression
    if len(df) < 30:
        return "linear"
    
    # For seasonal data, use Prophet
    if detect_seasonality(df):
        return "prophet"
    
    # Default to linear regression for simplicity
    return "linear"