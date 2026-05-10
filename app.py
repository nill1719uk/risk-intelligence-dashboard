import streamlit as st

st.set_page_config(page_title="Risk Intelligence Dashboard", page_icon="🏦", layout="wide")

st.title("🏦 Risk Intelligence Dashboard")
st.markdown("### Integrated Market · Credit · AML Risk Framework")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📈 **Market Risk**")

with col2:
    st.warning("💳 **Credit Risk**")

with col3:
    st.error("🚨 **AML Detection**")

st.divider()
st.success("👈 Use the sidebar to navigate between modules")
