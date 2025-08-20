"""preprocess.py – Simple helpers to clean messy sales data

This script:
1. Finds the date and sales columns in a messy CSV or DataFrame
2. Cleans it into a tidy 2‑column format:  'ds' (date),  'y' (sales)
3. Returns quick summary stats for the UI

Dependency footprint: **just pandas**.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Union

__all__ = ["clean_data", "diagnose_dataset", "validate_data_quality", "get_data_insights"]

def clean_data(df):
    """Clean and prepare sales data for forecasting"""
    # Make a copy to avoid modifying original data
    df_clean = df.copy()
    
    # Find date and sales columns
    date_col = None
    sales_col = None
    
    for col in df_clean.columns:
        col_lower = col.lower()
        if any(word in col_lower for word in ['date', 'time', 'day']):
            date_col = col
        elif any(word in col_lower for word in ['sales', 'revenue', 'amount', 'value']):
            sales_col = col
    
    if not date_col or not sales_col:
        raise ValueError("Could not find date and sales columns. Please ensure your CSV has columns for dates and sales values.")
    
    # Rename columns to standard format
    df_clean = df_clean.rename(columns={date_col: 'ds', sales_col: 'y'})
    
    # Convert date column to datetime
    df_clean['ds'] = pd.to_datetime(df_clean['ds'])
    
    # Remove currency symbols and convert sales to numeric
    if df_clean['y'].dtype == 'object':
        df_clean['y'] = df_clean['y'].astype(str).str.replace('$', '').str.replace(',', '')
        df_clean['y'] = pd.to_numeric(df_clean['y'], errors='coerce')
    
    # Remove rows with missing values
    df_clean = df_clean.dropna()
    
    # Sort by date
    df_clean = df_clean.sort_values('ds')
    
    # Keep only the required columns
    df_clean = df_clean[['ds', 'y']]
    
    if len(df_clean) == 0:
        raise ValueError("No valid data rows found after cleaning.")
    
    return df_clean

def diagnose_dataset(df):
    """Get basic statistics about the dataset"""
    stats = {
        'total_rows': len(df),
        'date_range': f"{df['ds'].min().strftime('%Y-%m-%d')} to {df['ds'].max().strftime('%Y-%m-%d')}",
        'avg_sales': round(df['y'].mean(), 2),
        'min_sales': round(df['y'].min(), 2),
        'max_sales': round(df['y'].max(), 2),
        'total_sales': round(df['y'].sum(), 2)
    }
    return stats

def validate_data_quality(df):
    """Check for common data quality issues"""
    issues = []
    insights = {}
    
    # Check for missing values
    missing_count = df['y'].isnull().sum()
    if missing_count > 0:
        issues.append(f"Found {missing_count} missing sales values")
    
    # Check for zero variance
    if df['y'].std() == 0:
        issues.append("All sales values are identical")
    
    # Check for outliers (values more than 3 standard deviations from mean)
    mean_sales = df['y'].mean()
    std_sales = df['y'].std()
    outliers = df[abs(df['y'] - mean_sales) > 3 * std_sales]
    if len(outliers) > 0:
        issues.append(f"Found {len(outliers)} potential outliers")
    
    # Check for date gaps
    df_sorted = df.sort_values('ds')
    date_diffs = df_sorted['ds'].diff().dt.days
    large_gaps = date_diffs[date_diffs > 7]
    if len(large_gaps) > 0:
        issues.append(f"Found {len(large_gaps)} gaps larger than 7 days in data")
    
    insights = {
        'total_records': len(df),
        'date_range_days': (df['ds'].max() - df['ds'].min()).days,
        'avg_daily_sales': round(df['y'].mean(), 2),
        'sales_volatility': round(df['y'].std() / df['y'].mean(), 3)
    }
    
    return {"issues": issues, "insights": insights}

def get_data_insights(df):
    """Analyze data patterns and provide insights"""
    insights = {}
    
    # Weekly pattern analysis
    df_copy = df.copy()
    df_copy['day_of_week'] = df_copy['ds'].dt.dayofweek
    daily_avg = df_copy.groupby('day_of_week')['y'].mean()
    
    best_day_idx = daily_avg.idxmax()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    best_day = day_names[best_day_idx]
    
    insights['weekly_pattern'] = f"Best sales day: {best_day}"
    
    # Trend analysis
    df_sorted = df.sort_values('ds')
    if len(df_sorted) > 10:
        first_half = df_sorted.iloc[:len(df_sorted)//2]['y'].mean()
        second_half = df_sorted.iloc[len(df_sorted)//2:]['y'].mean()
        
        if second_half > first_half * 1.1:
            insights['trend'] = "Sales appear to be increasing over time"
        elif second_half < first_half * 0.9:
            insights['trend'] = "Sales appear to be decreasing over time"
        else:
            insights['trend'] = "Sales appear to be stable over time"
    
    return insights
