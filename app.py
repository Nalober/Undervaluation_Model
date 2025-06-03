import streamlit as st
import pandas as pd

st.title("Undervalued Stock Screener")
st.caption("Based on P/E Ratio < 15")

df = pd.read_csv("undervalued.csv")
st.dataframe(df)
