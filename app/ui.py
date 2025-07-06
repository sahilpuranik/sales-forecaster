# ui.py  (run it with:  streamlit run app/ui.py)
import streamlit as st
import pandas as pd

from preprocess import clean_data, diagnose_dataset

st.title("📈 Sales Forecaster – Week-1 Demo")

# ── upload widget ──
file = st.sidebar.file_uploader("Upload CSV with a date & sales column")

if file:
    # 1) read ➜ clean 2) show preview 3) show diagnostics
    raw_df = pd.read_csv(file)
    df = clean_data(raw_df)
    diag = diagnose_dataset(df)

    st.subheader("Cleaned preview")
    st.dataframe(df.head())

    st.subheader("Quick stats")
    st.json(diag)

    # TODO: add a nice error-warning box if clean_data raises ValueError
else:
    st.info("👈 Upload a file to start")