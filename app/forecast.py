"""
forecast.py – Core forecasting logic

Implements:
- Prophet model
- Linear regression with lag features
- Unified `run_forecast()` interface

Used by: Streamlit UI (Week 3), Flask backend (Weeks 4–5)
"""

from typing import Literal, Tuple
import pandas as pd
from pandas import DataFrame

# --- ML models ---
from prophet import Prophet
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# --- Utils ---
from utils import select_model
from config import MIN_RELIABLE_ROWS

# Prophet Forecast – predicts future using seasonality/trends
def run_prophet(df: DataFrame, periods: int = 30) -> DataFrame:
    model = Prophet(daily_seasonality=True, seasonality_mode="additive")
    model.fit(df[["ds", "y"]])
    future = model.make_future_dataframe(periods=periods, freq="D")
    forecast = model.predict(future)

    forecast_only = forecast[forecast["ds"] > df["ds"].max()]
    forecast_only = forecast_only[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast_only["model_used"] = "prophet"

    return forecast_only.reset_index(drop=True)

# Add past values (lag features) to use in prediction
def add_lag_features(df: DataFrame, lags: Tuple[int] = (1, 2, 3)) -> DataFrame:
    for lag in lags:
        df[f"lag_{lag}"] = df["y"].shift(lag)
    return df

# Linear Regression – simpler model using past 3 days to predict next 7
def run_linear_regression(df: DataFrame, days: int = 7) -> DataFrame:
    lags = (1, 2, 3)
    df = add_lag_features(df.copy(), lags)
    df = df.dropna().reset_index(drop=True)

    feature_cols = [f"lag_{lag}" for lag in lags]
    X = df[feature_cols]
    y = df["y"]

    model = Ridge(alpha=1.0)
    model.fit(X, y)

    last_known_date = df["ds"].max()
    temp_df = df.copy()
    forecasts = []

    for i in range(days):
        latest_lags = [temp_df["y"].iloc[-lag] for lag in lags]
        X_pred = pd.DataFrame([latest_lags], columns=feature_cols)
        yhat = model.predict(X_pred)[0]

        next_date = last_known_date + pd.Timedelta(days=i+1)
        forecasts.append({
            "ds": next_date,
            "yhat": yhat,
            "yhat_lower": yhat * 0.95,
            "yhat_upper": yhat * 1.05,
            "model_used": "linear"
        })

        temp_df = pd.concat([temp_df, pd.DataFrame({"ds": [next_date], "y": [yhat]})], ignore_index=True)

    return pd.DataFrame(forecasts)

# Main forecast function – picks model and runs it
def run_forecast(df: DataFrame, model: Literal["auto", "linear", "prophet"] = "auto") -> DataFrame:
    if len(df) < MIN_RELIABLE_ROWS:
        return pd.DataFrame({
            "warning_msg": ["Insufficient data (need ≥30 rows for meaningful forecast)"]
        })

    if model == "auto":
        model = select_model(df)

    if model == "linear":
        forecast_df = run_linear_regression(df)
    else:
        forecast_df = run_prophet(df)

    # Add a flag if the prediction range is too wide (low confidence)
    margin = forecast_df["yhat_upper"] - forecast_df["yhat_lower"]
    forecast_df["low_confidence"] = margin > (2 * forecast_df["yhat"].abs())

    return forecast_df

# How good is the forecast? Measures error
def evaluate_forecast(y_true, y_pred) -> dict:
    mape = (abs((y_true - y_pred) / y_true)).mean() * 100
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "n": len(y_true)
    }

# ──────────────────────────────────────────────────────────────────────────────
# TESTING
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pass