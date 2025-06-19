# ui.py  (run it with:  streamlit run app/ui.py)
import streamlit as st
import pandas as pd

from preprocess import clean_data, diagnose_dataset

st.title("Streamlit Week 1 Product demo")

# ── upload widget ──
file = st.sidebar.file_uploader()

