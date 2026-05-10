import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Market Risk", layout="wide")

st.title("Market Risk - Value at Risk Calculator")
st.markdown("Enter any stock ticker to calculate live VaR. Find tickers at [Yahoo Finance](https://finance.yahoo.com)")
st.info("Examples: AAPL (Apple), TSLA (Tesla), JD.L (JD Sports), HSBA.L (HSBC), RELIANCE.NS (Reliance India)")
st.divider()

ticker = st.text_input("Stock Ticker", value="AAPL").upper()
investment = st.number_input("Portfolio Value", value=100000, step=1000)
confidence = st.slider("Confidence Level", min_value=90, max_value=99, value=95)
st.caption("90% = Higher loss estimate | 95% = Industry standard | 99% = Most conservative, used by major banks")

if st.button("Calculate VaR"):
    with st.spinner("Fetching live data..."):
        try:
            data = yf.download(ticker, period="2y", progress=False, auto_adjust=True)

            if data.empty:
                st.error("No data found for ticker: " + ticker)
            else:
                close_prices = data["Close"].squeeze()
                returns = close_prices.pct_change().dropna()
                returns = returns[np.isfinite(returns)]

                if len(returns) < 10:
                    st.error("Not enough data to calculate VaR")
                else:
                    mean_return = float(returns.mean())
                    std_return = float(returns.std())
                    z = 1.645 if confidence == 95 else 2.326

                    hist_var = float(np.percentile(returns, 100 - confidence)) * investment * -1
                    param_var = (mean_return - z * std_return) * investment * -1

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Historical VaR", str(round(hist_var, 2)))
                    col2.metric("Parametric VaR", str(round(param_var, 2)))
                    col3.metric("Daily Volatility", str(round(std_return*100, 2)) + "%")

                    st.success("At " + str(confidence) + "% confidence, maximum 1-day loss is " + str(round(hist_var, 2)))
                    st.info("This means on " + str(100-confidence) + " out of every 100 trading days, losses could exceed this figure.")

        except Exception as e:
            st.error("Error fetching data: " + str(e))