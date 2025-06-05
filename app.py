
import streamlit as st
import pandas as pd
from scanner import get_nasdaq_tickers, scan_tickers

st.title("Undervalued Stock Screener")
st.caption("Updated every 2 weeks — via scheduled GitHub Action")

import time
st.write("App loaded at:", time.ctime())


tickers = get_nasdaq_tickers()
df = scan_tickers(tickers, limit=100)  # Or load a saved version

# Optionally save
df.to_csv("undervalued.csv", index=False)