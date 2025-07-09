"""preprocess.py – Simple helpers to clean messy sales data

This script:
1. Finds the date and sales columns in a messy CSV or DataFrame
2. Cleans it into a tidy 2‑column format:  'ds' (date),  'y' (sales)
3. Returns quick summary stats for the UI

Dependency footprint: **just pandas**.
"""

from typing import Dict, Sequence, Tuple, Union

import pandas as pd
from pandas import DataFrame

__all__ = ["clean_data", "diagnose_dataset"]

# Helpers
def _auto_col(df: DataFrame, keys: Sequence[str]) -> str:
    """Return the first column whose name contains one of *keys* (case‑insensitive)."""
    for col in df.columns:
        if any(k in col.lower() for k in keys):
            return col
    return ""

# Core cleaning logic
def clean_data(
    data: Union[str, bytes, DataFrame],
    *,
    date_keys: Tuple[str, ...] = ("date", "order", "day", "time", "timestamp"),
    amount_keys: Tuple[str, ...] = ("total", "sale", "amount", "revenue", "price"),
) -> DataFrame:
    """Return a tidy dataframe with columns **ds** (datetime) and **y** (float)."""

    # ── 1 · Load --------------------------------------------------------------
    df = pd.read_csv(data) if isinstance(data, (str, bytes)) else data.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    # ── 2 · Identify columns --------------------------------------------------
    date_col = _auto_col(df, date_keys)
    amount_col = _auto_col(df, amount_keys)

    # Fallback: heuristics only if name matching failed
    if not date_col:
        # Prefer object / string columns; numeric columns are seldom dates
        for col in df.select_dtypes(include="object").columns:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.9 and parsed.dt.normalize().nunique() > 1:
                date_col = col
                break

    if not amount_col:
        for col in df.columns:  # any dtype
            nums = pd.to_numeric(
                df[col].astype(str).str.replace(r"[,$]", "", regex=True), errors="coerce"
            )
            if nums.notna().mean() > 0.5 and nums.mean() > 0:
                amount_col = col
                break

    if not date_col or not amount_col:
        raise ValueError("Could not find both a date column and a sales column.")

    # ── 3 · Build tidy frame --------------------------------------------------
    clean_df = pd.DataFrame(
        {
            "ds": pd.to_datetime(df[date_col], errors="coerce"),
            "y": pd.to_numeric(
                df[amount_col].astype(str).str.replace(r"[,$]", "", regex=True),
                errors="coerce",
            ),
        }
    )

    clean_df = clean_df.dropna().sort_values("ds").reset_index(drop=True)
    if clean_df.empty:
        raise ValueError("No valid rows after cleaning.")

    return clean_df

# Diagnostics for model selection + dashboard display
def diagnose_dataset(df: DataFrame) -> Dict[str, Union[int, float, str]]:
    """Return basic stats for dashboard display."""
    if {"ds", "y"} - set(df.columns):
        raise ValueError("Data must have 'ds' and 'y' columns.")

    gaps = df["ds"].diff().dt.days.gt(1).sum()
    return {
        "rows": len(df),
        "date_start": df["ds"].min().strftime("%Y-%m-%d"),
        "date_end": df["ds"].max().strftime("%Y-%m-%d"),
        "avg_sales": float(df["y"].mean()),
        "median_sales": float(df["y"].median()),
        "missing_date_gaps": int(gaps),
    }

# Minimal self‑test
if __name__ == "__main__":
    df = clean_data("data/preProcessTester.csv")
    print(df.head(), "\n")
    print(diagnose_dataset(df))
