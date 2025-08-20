import pandas as pd
import pytest
from App.preprocess import clean_data, validate_data_quality, get_data_insights

def test_clean_data_with_valid_csv():
    """Test data cleaning with valid CSV data."""
    df = pd.DataFrame({
        'Order Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Total Amount': [100.0, 150.0, 200.0]
    })
    
    result = clean_data(df)
    
    assert len(result) == 3
    assert 'ds' in result.columns
    assert 'y' in result.columns
    assert result['ds'].dtype == 'datetime64[ns]'
    assert result['y'].dtype == 'float64'

def test_clean_data_with_currency_symbols():
    """Test data cleaning with currency symbols."""
    df = pd.DataFrame({
        'Date': ['2024-01-01', '2024-01-02'],
        'Sales': ['$100.50', '$200.75']
    })
    
    result = clean_data(df)
    
    assert len(result) == 2
    assert result['y'].iloc[0] == 100.50
    assert result['y'].iloc[1] == 200.75

def test_clean_data_missing_columns():
    """Test error handling for missing required columns."""
    df = pd.DataFrame({
        'Name': ['John', 'Jane'],
        'Age': [25, 30]
    })
    
    with pytest.raises(ValueError, match="Could not find both a date column and a sales column"):
        clean_data(df)

def test_validate_data_quality_no_issues():
    """Test data quality validation with clean data."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=10, freq='D'),
        'y': [100 + i * 10 for i in range(10)]
    })
    
    result = validate_data_quality(df)
    
    assert 'issues' in result
    assert 'insights' in result
    assert len(result['issues']) == 0
    assert result['insights']['total_records'] == 10

def test_validate_data_quality_with_missing_values():
    """Test data quality validation with missing values."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=5, freq='D'),
        'y': [100, None, 120, 130, 140]
    })
    
    result = validate_data_quality(df)
    
    assert len(result['issues']) > 0
    assert any('missing' in issue.lower() for issue in result['issues'])

def test_validate_data_quality_with_outliers():
    """Test data quality validation with outliers."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=10, freq='D'),
        'y': [100, 110, 120, 130, 140, 150, 160, 170, 180, 1000]  # 1000 is outlier
    })
    
    result = validate_data_quality(df)
    
    assert len(result['issues']) > 0
    assert any('outlier' in issue.lower() for issue in result['issues'])

def test_get_data_insights_weekly_pattern():
    """Test pattern detection with weekly data."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=14, freq='D'),
        'y': [100, 110, 120, 130, 140, 150, 200,  # Week 1
              100, 110, 120, 130, 140, 150, 200]  # Week 2 (same pattern)
    })
    
    result = get_data_insights(df)
    
    assert 'weekly_pattern' in result
    assert 'Sunday' in result['weekly_pattern']  # Sunday has highest sales

def test_get_data_insights_trend():
    """Test trend detection."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=14, freq='D'),
        'y': [100, 110, 120, 130, 140, 150, 160,  # First week
              170, 180, 190, 200, 210, 220, 230]  # Second week (upward trend)
    })
    
    result = get_data_insights(df)
    
    assert 'trend' in result
    assert 'upward' in result['trend']

def test_diagnose_dataset():
    """Test dataset diagnostics."""
    df = pd.DataFrame({
        'ds': pd.date_range('2024-01-01', periods=10, freq='D'),
        'y': [100 + i * 10 for i in range(10)]
    })
    
    result = diagnose_dataset(df)
    
    assert result['rows'] == 10
    assert result['date_start'] == '2024-01-01'
    assert result['date_end'] == '2024-01-10'
    assert result['avg_sales'] == 145.0