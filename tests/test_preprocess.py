import pandas as pd
from app.preprocess import preprocess_csv

def test_preprocess_detects_correct_columns():
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5),
        'sales': [10, 20, 30, 25, 15]
    })
    cleaned_df, diagnostics = preprocess_csv(df)
    
    assert list(cleaned_df.columns) == ['ds', 'y']
    assert cleaned_df.shape == (5, 2)
    assert diagnostics['date_column'] == 'date'
    assert diagnostics['sales_column'] == 'sales'

def test_preprocess_handles_missing_values():
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5),
        'sales': [10, None, 30, None, 15]
    })
    cleaned_df, diagnostics = preprocess_csv(df)
    
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape[0] == 3  # dropped rows with None