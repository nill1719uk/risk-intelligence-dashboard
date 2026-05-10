import streamlit as st
import numpy as np

st.set_page_config(page_title="Credit Risk", page_icon="💳", layout="wide")

st.title("💳 Credit Risk — Loan Default Probability")
st.markdown("Enter applicant details to generate a risk decision")
st.divider()

col1, col2 = st.columns(2)

with col1:
    annual_income = st.number_input("Annual Income (£)", value=50000, step=1000)
    loan_amount = st.number_input("Loan Amount (£)", value=15000, step=500)
    credit_score = st.slider("Credit Score", 300, 850, 650)

with col2:
    employment_years = st.slider("Years Employed", 0, 30, 5)
    existing_debts = st.number_input("Existing Debts (£)", value=5000, step=500)
    age = st.slider("Age", 18, 75, 35)

st.divider()

if st.button("Assess Credit Risk"):
    debt_to_income = existing_debts / annual_income if annual_income > 0 else 0

    score = (
        -0.700 * ((credit_score - 650) / 100) +
         0.423 * (debt_to_income - 0.3) +
        -0.358 * ((employment_years - 5) / 5) +
         0.340 * ((existing_debts - 5000) / 5000)
    )

    pd_score = 1 / (1 + np.exp(-score))

    col1, col2, col3 = st.columns(3)
    col1.metric("Probability of Default", f"{pd_score*100:.1f}%")
    col2.metric("Debt-to-Income Ratio", f"{debt_to_income*100:.1f}%")
    col3.metric("Credit Score Band", 
        "Excellent" if credit_score >= 750 else "Good" if credit_score >= 650 else "Poor")

    st.divider()

    if pd_score < 0.30:
        st.success("✅ DECISION: APPROVE — Low default risk")
    elif pd_score < 0.60:
        st.warning("⚠️ DECISION: REVIEW — Moderate risk, manual assessment required")
    else:
        st.error("❌ DECISION: REJECT — High default probability")
