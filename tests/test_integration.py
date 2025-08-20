"""
Integration tests for the complete SalesForecaster application.
Tests the full workflow from data upload to forecast generation.
"""

import pytest
import pandas as pd
import tempfile
import os
from io import StringIO

# Import application components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from App.preprocess import clean_data, validate_data_quality, get_data_insights
from App.forecast import run_forecast

def create_test_csv():
    """Create a test CSV file with realistic sales data."""
    data = """Order Date,Total Amount
2024-01-01,100.50
2024-01-02,150.75
2024-01-03,120.25
2024-01-04,180.00
2024-01-05,200.50
2024-01-06,250.75
2024-01-07,300.00
2024-01-08,275.25
2024-01-09,225.50
2024-01-10,175.75"""
    
    return StringIO(data)

def test_full_workflow_integration():
    """Test complete workflow: CSV → Clean → Validate → Forecast."""
    
    # Step 1: Create test data
    csv_data = create_test_csv()
    
    # Step 2: Clean data
    cleaned_df = clean_data(csv_data)
    
    assert len(cleaned_df) == 10
    assert 'ds' in cleaned_df.columns
    assert 'y' in cleaned_df.columns
    assert cleaned_df['ds'].dtype == 'datetime64[ns]'
    assert cleaned_df['y'].dtype == 'float64'
    
    # Step 3: Validate data quality
    quality_report = validate_data_quality(cleaned_df)
    
    assert 'issues' in quality_report
    assert 'insights' in quality_report
    assert quality_report['insights']['total_records'] == 10
    assert quality_report['insights']['avg_daily_sales'] > 0
    
    # Step 4: Get pattern insights
    pattern_insights = get_data_insights(cleaned_df)
    
    assert isinstance(pattern_insights, dict)
    
    # Step 5: Generate forecast
    forecast_result = run_forecast(cleaned_df)
    
    assert 'forecast' in forecast_result
    assert 'low_confidence' in forecast_result
    assert 'insights' in forecast_result
    assert isinstance(forecast_result['forecast'], pd.DataFrame)
    assert len(forecast_result['forecast']) > 0

def test_workflow_with_weekly_pattern():
    """Test workflow with data containing weekly patterns."""
    
    # Create data with weekly pattern (higher sales on weekends)
    dates = pd.date_range('2024-01-01', periods=21, freq='D')
    sales = []
    for i, date in enumerate(dates):
        if date.weekday() >= 5:  # Weekend
            sales.append(200 + i * 5)
        else:  # Weekday
            sales.append(100 + i * 5)
    
    df = pd.DataFrame({'ds': dates, 'y': sales})
    
    # Test data quality validation
    quality_report = validate_data_quality(df)
    assert len(quality_report['issues']) == 0  # Clean data
    
    # Test pattern detection
    pattern_insights = get_data_insights(df)
    assert 'weekly_pattern' in pattern_insights
    
    # Test forecasting
    forecast_result = run_forecast(df)
    assert forecast_result['insights']['model_used'] == 'prophet'

def test_workflow_with_data_issues():
    """Test workflow with problematic data."""
    
    # Create data with issues
    dates = pd.date_range('2024-01-01', periods=10, freq='D')
    sales = [100, None, 120, 130, 140, 150, 160, 170, 180, 1000]  # Missing value + outlier
    
    df = pd.DataFrame({'ds': dates, 'y': sales})
    
    # Test data quality validation
    quality_report = validate_data_quality(df)
    assert len(quality_report['issues']) > 0
    assert any('missing' in issue.lower() for issue in quality_report['issues'])
    assert any('outlier' in issue.lower() for issue in quality_report['issues'])

def test_workflow_with_insufficient_data():
    """Test workflow with insufficient data for reliable forecasting."""
    
    # Create minimal data
    dates = pd.date_range('2024-01-01', periods=5, freq='D')
    sales = [100, 110, 120, 130, 140]
    
    df = pd.DataFrame({'ds': dates, 'y': sales})
    
    # Test forecasting with insufficient data
    forecast_result = run_forecast(df)
    assert 'warning_msg' in forecast_result
    assert 'insufficient' in forecast_result['warning_msg'].lower()

def test_error_handling_integration():
    """Test error handling throughout the workflow."""
    
    # Test with invalid data
    with pytest.raises(ValueError):
        clean_data(StringIO("Invalid,Data\nNot,CSV"))
    
    # Test with empty data
    with pytest.raises(ValueError):
        clean_data(StringIO(""))
    
    # Test with missing required columns
    with pytest.raises(ValueError):
        clean_data(StringIO("Name,Age\nJohn,25\nJane,30"))

def test_data_export_format():
    """Test that forecast data is in correct format for export."""
    
    # Create test data
    csv_data = create_test_csv()
    cleaned_df = clean_data(csv_data)
    forecast_result = run_forecast(cleaned_df)
    
    forecast_df = forecast_result['forecast']
    
    # Check export format
    assert 'ds' in forecast_df.columns
    assert 'yhat' in forecast_df.columns
    assert 'yhat_lower' in forecast_df.columns
    assert 'yhat_upper' in forecast_df.columns
    assert 'model_used' in forecast_df.columns
    assert 'low_confidence' in forecast_df.columns
    
    # Check data types
    assert forecast_df['ds'].dtype == 'datetime64[ns]'
    assert forecast_df['yhat'].dtype == 'float64'
    assert forecast_df['yhat_lower'].dtype == 'float64'
    assert forecast_df['yhat_upper'].dtype == 'float64'

def test_model_selection_logic():
    """Test that appropriate models are selected for different data types."""
    
    # Test small dataset → linear regression
    small_dates = pd.date_range('2024-01-01', periods=15, freq='D')
    small_sales = [i + 100 for i in range(15)]
    small_df = pd.DataFrame({'ds': small_dates, 'y': small_sales})
    
    small_result = run_forecast(small_df)
    assert small_result['insights']['model_used'] == 'linear'
    
    # Test large dataset → Prophet
    large_dates = pd.date_range('2024-01-01', periods=50, freq='D')
    large_sales = [i + 100 + (i % 7) * 10 for i in range(50)]  # Add weekly pattern
    large_df = pd.DataFrame({'ds': large_dates, 'y': large_sales})
    
    large_result = run_forecast(large_df)
    assert large_result['insights']['model_used'] == 'prophet'
