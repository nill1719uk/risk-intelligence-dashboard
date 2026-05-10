import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Market Risk", page_icon="📈", layout="wide")

st.title("📈 Market Risk — Value at Risk Calculator")
st.markdown("Enter any stock ticker to calculate live VaR")
st.divider()

ticker = st.text_input("Stock Ticker", value="AAPL").upper()
investment = st.number_input("Portfolio Value (£)", value=100000, step=1000)
confidence = st.slider("Confidence Level", min_value=90, max_value=99, value=95)

if st.button("Calculate VaR"):
    with st.spinner("Fetching live data..."):
        data = yf.download(ticker, period="2y", progress=False)
        close_prices = data["Close"].squeeze()
        returns = close_prices.pct_change().dropna()

        mean_return = float(returns.mean())
        std_return = float(returns.std())

        z = 1.645 if confidence == 95 else 2.326
        hist_var = float(np.percentile(returns, 100 - confidence)) * investment * -1
        param_var = (mean_return - z * std_return) * investment * -1

        col1, col2, col3 = st.columns(3)
        col1.metric("Historical VaR", f"£{hist_var:,.2f}", f"{hist_var/investment*100:.2f}%")
        col2.metric("Parametric VaR", f"£{param_var:,.2f}", f"{param_var/investment*100:.2f}%")
        col3.metric("Daily Volatility", f"{std_return*100:.2f}%")

        st.success(f"At {confidence}% confidence, maximum 1-day loss is £{hist_var:,.2f}")
