from typing import Literal
from pandas import DataFrame
import warnings

from App.config import ABSOLUTE_MIN, SMALL_MAX

def detect_seasonality(df: DataFrame, lag: int = 7, threshold: float = 0.3) -> bool:
    # Check if there's a weekly pattern in sales (like spikes every Sunday)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return df["y"].autocorr(lag=lag) > threshold

def select_model(df: DataFrame) -> Literal["linear", "prophet"]:
    """
    Pick the right model based on how much data we have and if there's a pattern.
    
    - Not enough rows? Stop and warn.
    - Small dataset? Use simple model unless there's a clear pattern.
    - Bigger dataset? Use fancy model.
    """
    num_rows = len(df)

    if num_rows < ABSOLUTE_MIN:
        raise ValueError(f"Too little data to forecast — please upload at least {ABSOLUTE_MIN} rows.")

    if num_rows <= SMALL_MAX:
        # For small files, check for repeating patterns
        if detect_seasonality(df):
            return "prophet"
        else:
            return "linear"
    else:
        return "prophet"