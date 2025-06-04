
import streamlit as st
import pandas as pd



st.title("Undervalued Stock Screener")
st.caption("Updated every 2 weeks — via scheduled GitHub Action")

import time
st.write("App loaded at:", time.ctime())


try:
    df = pd.read_csv("undervalued.csv")  # or .pkl if you're using that
    if df.empty:
        st.warning("No undervalued stocks found in last scan.")
    else:
        st.success(f"Found {len(df)} undervalued stocks.")
        st.dataframe(df)
        st.download_button("Download CSV", df.to_csv(index=False), "undervalued.csv", "text/csv")
except FileNotFoundError:
    st.error("Data file not found. Please check back after the next scheduled update.")
