
import streamlit as st
import pandas as pd
import time
from scanner import get_nasdaq_tickers, scan_tickers
from streamlit.runtime.scriptrunner import add_script_run_ctx

st.title("Undervalued Stock Screener")
st.caption("Updated every 2 weeks — via scheduled GitHub Action")

st.write("App loaded at:", time.ctime())

if st.button(" Refresh Data Now"):
    st.cache_data.clear()
    st.experimental_rerun()

# This function caches results for 2 weeks
@st.cache_data(ttl=60 * 60 * 24 * 14)
def get_cached_results():
    tickers = get_nasdaq_tickers()
    return scan_tickers(tickers, limit=100)

with st.spinner("Scanning tickers... please wait (~1–2 mins)"):
    df = get_cached_results()

if df.empty:
    st.warning("No undervalued stocks found.")
else:
    st.success(f"Found {len(df)} undervalued stocks")
    st.dataframe(df)

    # Fix the variable name here
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "undervalued.csv", "text/csv")