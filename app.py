


import streamlit as st
import pandas as pd
from scanner import get_nasdaq_tickers, scan_tickers

st.title("Undervalued Stock Screener")
st.caption("Based on P/E Ratio < 15")

with st.spinner("Scanning tickers... please wait (~1–2 mins)"):
    tickers = get_nasdaq_tickers()
    df = scan_tickers(tickers)
    
    
if df.empty:
    st.warning("No undervalued stocks found.")
else:
    st.success(f"Found {len(df)} undervalued stocks")
    st.dataframe(df)

    # Optionally offer download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "undervalued.csv", "text/csv")    

