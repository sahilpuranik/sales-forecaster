"""
config.py
A tiny file that just holds settings.
You will IMPORT these constants from other files.
"""
#prophet range is from 90 - 730 days
# ── How many rows count as a “small” CSV? ──
SMALL_MAX = 90          # TODO: experiment later—does 90 still feel right?

# Rows that are still OK for Prophet before we jump to LSTM
MEDIUM_MAX = 730        # about 2 years of daily data

# How long (seconds) we let Streamlit cache things
CACHE_TTL_SEC = 60 * 60   # 1 hour