import streamlit as st
import pandas as pd

st.set_page_config(page_title="AML Detection", page_icon="??", layout="wide")

st.title("?? AML Detection — Transaction Alert Monitor")
st.markdown("Live alert register with rule-based flags and ML risk scores")
st.divider()

@st.cache_data
def load_alerts():
    return pd.read_csv("data/aml_alerts.csv")

df = load_alerts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Alerts", len(df))
col2.metric("Critical", len(df[df["alert_confidence"] == "CRITICAL"]))
col3.metric("High", len(df[df["alert_confidence"] == "HIGH"]))
col4.metric("Medium", len(df[df["alert_confidence"] == "MEDIUM"]))

st.divider()

alert_filter = st.selectbox("Filter by Alert Level", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])

if alert_filter == "ALL":
    filtered = df
else:
    filtered = df[df["alert_confidence"] == alert_filter]

st.markdown(f"**Showing {len(filtered)} alerts**")
st.dataframe(filtered, use_container_width=True)
