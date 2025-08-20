import pandas as pd
import pytest
from App.forecast import run_forecast, run_prophet, run_linear_regression, ForecastingError

def test_forecast_with_sufficient_data_prophet():
    """Test Prophet forecasting with sufficient data."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'y': [i + 10 + (i % 7) * 5 for i in range(100)]  # Add weekly pattern
    })
    
    result = run_forecast(df)
    
    assert 'forecast' in result
    assert not result['low_confidence']
    assert isinstance(result['forecast'], pd.DataFrame)
    assert 'ds' in result['forecast'].columns
    assert 'yhat' in result['forecast'].columns
    assert 'model_used' in result['forecast'].columns
    assert result['insights']['model_used'] == 'prophet'

def test_forecast_with_small_data_uses_linear():
    """Test linear regression with small dataset."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=15, freq='D'),
        'y': [5, 10, 9, 8, 11, 13, 12, 14, 15, 16, 17, 18, 19, 20, 21]
    })
    
    result = run_forecast(df)
    
    assert 'forecast' in result
    assert isinstance(result['forecast'], pd.DataFrame)
    assert result['forecast'].shape[0] > 0
    assert 'yhat' in result['forecast'].columns
    assert result['insights']['model_used'] == 'linear'

def test_forecast_insufficient_data():
    """Test error handling for insufficient data."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=3, freq='D'),
        'y': [5, 10, 9]
    })
    
    result = run_forecast(df)
    
    assert 'warning_msg' in result
    assert 'insufficient' in result['warning_msg'].lower()

def test_forecast_identical_values():
    """Test error handling for identical sales values."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'y': [100] * 10  # All identical values
    })
    
    with pytest.raises(ForecastingError, match="identical"):
        run_forecast(df)

def test_forecast_too_few_points():
    """Test error handling for too few data points."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=2, freq='D'),
        'y': [5, 10]
    })
    
    with pytest.raises(ForecastingError, match="at least 5 data points"):
        run_forecast(df)

def test_prophet_model():
    """Test Prophet model directly."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=30, freq='D'),
        'y': [i + 10 + (i % 7) * 5 for i in range(30)]
    })
    
    result = run_prophet(df)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert 'ds' in result.columns
    assert 'yhat' in result.columns
    assert 'yhat_lower' in result.columns
    assert 'yhat_upper' in result.columns
    assert 'model_used' in result.columns
    assert result['model_used'].iloc[0] == 'prophet'

def test_linear_regression_model():
    """Test linear regression model directly."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=20, freq='D'),
        'y': [i + 10 for i in range(20)]
    })
    
    result = run_linear_regression(df)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 7  # Default 7 days forecast
    assert 'ds' in result.columns
    assert 'yhat' in result.columns
    assert 'yhat_lower' in result.columns
    assert 'yhat_upper' in result.columns
    assert 'model_used' in result.columns
    assert result['model_used'].iloc[0] == 'linear'

def test_linear_regression_insufficient_data():
    """Test linear regression with insufficient data."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'y': [i + 10 for i in range(5)]
    })
    
    with pytest.raises(ForecastingError, match="at least 10 rows"):
        run_linear_regression(df)

def test_forecast_confidence_assessment():
    """Test confidence assessment in forecasts."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=50, freq='D'),
        'y': [i + 10 + (i % 7) * 5 for i in range(50)]
    })
    
    result = run_forecast(df)
    
    assert 'low_confidence' in result
    assert isinstance(result['low_confidence'], bool)
    assert 'low_confidence' in result['forecast'].columns

def test_forecast_insights():
    """Test educational insights generation."""
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=40, freq='D'),
        'y': [i + 10 + (i % 7) * 5 for i in range(40)]
    })
    
    result = run_forecast(df)
    
    assert 'insights' in result
    assert 'model_used' in result['insights']
    assert 'model_explanation' in result['insights']
    assert 'forecast_periods' in result['insights']
    assert 'confidence_level' in result['insights']
    assert 'data_points_used' in result['insights']