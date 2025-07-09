import pandas as pd
from app.forecast import forecast_sales

def test_forecast_with_sufficient_data_prophet():
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'y': [i + 10 for i in range(100)]
    })
    result = forecast_sales(df)
    
    assert 'forecast' in result
    assert not result['low_confidence']
    assert isinstance(result['forecast'], pd.DataFrame)
    assert 'ds' in result['forecast'].columns and 'yhat' in result['forecast'].columns

def test_forecast_with_small_data_uses_regression():
    df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=8, freq='D'),
        'y': [5, 10, 9, 8, 11, 13, 12, 14]
    })
    result = forecast_sales(df)
    
    assert 'forecast' in result
    assert isinstance(result['forecast'], pd.DataFrame)
    assert result['forecast'].shape[0] > 0
    assert 'yhat' in result['forecast'].columns