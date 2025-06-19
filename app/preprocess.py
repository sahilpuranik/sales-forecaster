"""
preprocess.py – Tiny helper to tidy sales CSVs.

Goal:
Find the date column  → call it 'ds'
Find the sales column → call it 'y'
Drop everything else, give back clean df + quick stats

Only needs pandas.
"""

from typing import Dict, Sequence, Tuple, Union

import os
import pandas as pd
from pandas import DataFrame

__all__ = ["clean_data", "diagnose_dataset"]

# ─────────────────────────────────────────────────────────────
# Little detectors
# ─────────────────────────────────────────────────────────────

def _auto_col(df: DataFrame, keys: Sequence[str]) -> str:
    """First column whose name contains any keyword (case-insensitive)."""
    for col in df.columns:
        if any(k in col.lower() for k in keys):
            return col
    return ""


def _is_date(col: pd.Series) -> bool:
    """Does this column look like real dates?"""
    parsed = pd.to_datetime(col, errors="coerce")
    return parsed.notna().mean() > 0.8 and parsed.nunique() > 1


def _is_number(col: pd.Series) -> bool:
    """Does this column look like positive numbers (prices, totals…)?"""
    nums = pd.to_numeric(col.astype(str).str.replace(r"[,$]", "", regex=True), errors="coerce")
    return nums.notna().mean() > 0.6 and nums.mean() > 0


# ─────────────────────────────────────────────────────────────
# Main cleaner
# ─────────────────────────────────────────────────────────────

def clean_data(
    data: Union[str, bytes, DataFrame],
    *,
    date_keys: Tuple[str, ...] = ("date", "day", "time", "timestamp"),
    amount_keys: Tuple[str, ...] = ("total", "sale", "amount", "revenue", "price"),
) -> DataFrame:
    """
    Return a 2-column DataFrame:
    ▸ **ds** → datetime
    ▸ **y**  → float (sales)
    """

    # 1) Load ---------------------------------------------------------------
    if isinstance(data, (str, bytes)):
        df = pd.read_csv(os.path.expanduser(data))
    else:
        df = data.copy(deep=True)

    df.columns = [str(c).strip().lower() for c in df.columns]

    # 2) Guess columns -------------------------------------------------------
    date_col = _auto_col(df, date_keys)
    amount_col = _auto_col(df, amount_keys)

    # Validate guesses; if bad, ignore so fallback can try again
    if date_col and not _is_date(df[date_col]):
        date_col = ""
    if amount_col and not _is_number(df[amount_col]):
        amount_col = ""

    # Fallback search --------------------------------------------------------
    if not date_col:
        for col in df.columns:
            if _is_date(df[col]):
                date_col = col
                break

    if not amount_col:
        for col in df.columns:
            if _is_number(df[col]):
                amount_col = col
                break

    if not date_col or not amount_col:
        raise ValueError("Could not find both a valid date column and a sales column.")

    # 3) Build tidy frame ----------------------------------------------------
    clean_df = pd.DataFrame(
        {
            "ds": pd.to_datetime(df[date_col], errors="coerce"),
            "y": pd.to_numeric(
                df[amount_col].astype(str).str.replace(r"[,$]", "", regex=True),
                errors="coerce",
            ),
        }
    ).dropna().sort_values("ds").reset_index(drop=True)

    if clean_df.empty:
        raise ValueError("No valid rows after cleaning.")

    return clean_df

# Quick stats for dashboards
def diagnose_dataset(df: DataFrame) -> Dict[str, Union[int, float, str]]:
    if {"ds", "y"} - set(df.columns):
        raise ValueError("Need 'ds' and 'y' columns first.")

    start = df["ds"].min()
    end = df["ds"].max()
    days_span = (end - start).days + 1  # inclusive
    gaps = df["ds"].diff().dt.days.gt(1).sum()

    return {
        "rows": int(len(df)),
        "date_start": start.strftime("%Y-%m-%d"),
        "date_end": end.strftime("%Y-%m-%d"),
        "num_days": int(days_span),
        "avg_sales": float(df["y"].mean()),
        "median_sales": float(df["y"].median()),
        "missing_gaps": int(gaps),
    }

# Testing Block
if __name__ == "__main__":
    sample = "data/preprocesstester.csv"
    tidy = clean_data(sample)
    print(tidy.head(), "\n")
    print(diagnose_dataset(tidy))