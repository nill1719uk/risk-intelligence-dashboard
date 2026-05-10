import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Unified Risk Score", layout="wide")

st.title("Unified Risk Score - Client Risk Intelligence")
st.markdown("Composite scoring across Market, Credit and AML domains")
st.divider()

st.sidebar.header("Weight Configuration")
aml_weight = st.sidebar.slider("AML Weight %", 0, 100, 40)
credit_weight = st.sidebar.slider("Credit Weight %", 0, 100, 35)
market_weight = st.sidebar.slider("Market Weight %", 0, 100, 25)

total = aml_weight + credit_weight + market_weight
if total != 100:
    st.sidebar.warning(f"Weights sum to {total}% - adjust to reach 100%")

@st.cache_data
def load_data():
    df = pd.read_csv("data/aml_alerts.csv", encoding="utf-8")
    clients = df.groupby("client_id").agg(
        aml_score=("ml_suspicion_score", "mean"),
        alert_count=("alert_id", "count")
    ).reset_index()
    clients["aml_score"] = clients["aml_score"] * 100
    np.random.seed(42)
    clients["credit_score"] = np.random.uniform(20, 80, len(clients))
    clients["market_score"] = np.random.uniform(20, 80, len(clients))
    return clients

clients = load_data()

if total == 100:
    clients["unified_score"] = (
        clients["aml_score"] * (aml_weight/100) +
        clients["credit_score"] * (credit_weight/100) +
        clients["market_score"] * (market_weight/100)
    ).round(1)

    clients["risk_band"] = pd.cut(clients["unified_score"],
        bins=[0, 30, 50, 70, 100],
        labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    clients = clients.sort_values("unified_score", ascending=False).reset_index(drop=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", len(clients))
    col2.metric("Critical", len(clients[clients["risk_band"] == "CRITICAL"]))
    col3.metric("High Risk", len(clients[clients["risk_band"] == "HIGH"]))
    col4.metric("Avg Score", f"{clients['unified_score'].mean():.1f}")

    st.divider()
    st.markdown("### Client Risk Register")
    st.dataframe(clients[["client_id","unified_score","risk_band","aml_score","credit_score","market_score","alert_count"]],
        use_container_width=True)
else:
    st.warning("Please adjust weights in the sidebar to total exactly 100%")