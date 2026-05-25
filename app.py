import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Retirement Planner", layout="wide")

st.title("💰 AI Multi-Asset Retirement Calculator")

# Sidebar Inputs
st.sidebar.header("👤 Basic Details")

current_age = st.sidebar.number_input("Current Age", 18, 60, 35)
retirement_age = st.sidebar.number_input("Retirement Age", 50, 75, 60)

years = retirement_age - current_age

st.sidebar.header("💸 Monthly Investment")

monthly_investment = st.sidebar.number_input("Monthly SIP (₹)", 0, 1000000, 50000)
step_up = st.sidebar.slider("Annual SIP Step-up (%)", 0.0, 20.0, 5.0)

st.sidebar.header("📊 Expected Annual Returns (%)")

equity_return = st.sidebar.slider("Stocks / MF (%)", 5.0, 18.0, 12.0)
gold_return = st.sidebar.slider("Gold/Silver (%)", 3.0, 12.0, 7.0)
nps_return = st.sidebar.slider("NPS (%)", 6.0, 12.0, 9.0)
epf_return = st.sidebar.slider("EPF (%)", 7.0, 9.0, 8.1)
fd_return = st.sidebar.slider("FD (%)", 4.0, 8.0, 6.5)

st.sidebar.header("🏦 Current Asset Values (₹)")

stocks_value = st.sidebar.number_input("Stocks / Mutual Funds", 0, 100000000, 1000000)
gold_value = st.sidebar.number_input("Gold / Silver", 0, 100000000, 500000)
nps_value = st.sidebar.number_input("NPS", 0, 100000000, 2000000)
epf_value = st.sidebar.number_input("EPF", 0, 100000000, 1500000)
fd_value = st.sidebar.number_input("Fixed Deposits", 0, 100000000, 500000)

# Future Value Calculation Function
def future_value(principal, rate, years):
    return principal * ((1 + rate / 100) ** years)

# Calculate asset growth
stocks_future = future_value(stocks_value, equity_return, years)
gold_future = future_value(gold_value, gold_return, years)
nps_future = future_value(nps_value, nps_return, years)
epf_future = future_value(epf_value, epf_return, years)
fd_future = future_value(fd_value, fd_return, years)

# SIP Growth
monthly_r = equity_return / 12 / 100
sip = monthly_investment
sip_corpus = 0

for year in range(years):
    for month in range(12):
        sip_corpus = (sip_corpus + sip) * (1 + monthly_r)
    sip *= (1 + step_up / 100)

# Total corpus
total_corpus = (
    stocks_future +
    gold_future +
    nps_future +
    epf_future +
    fd_future +
    sip_corpus
)

# Output
st.subheader("📈 Retirement Summary")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Corpus", f"₹ {total_corpus:,.0f}")
col2.metric("📊 SIP Contribution", f"₹ {sip_corpus:,.0f}")
col3.metric("🏦 Existing Assets Future Value", f"₹ {(total_corpus - sip_corpus):,.0f}")

# Asset breakdown
st.subheader("📊 Asset Contribution Breakdown")

data = {
    "Asset": ["Stocks", "Gold/Silver", "NPS", "EPF", "FD", "SIP"],
    "Value": [
        stocks_future,
        gold_future,
        nps_future,
        epf_future,
        fd_future,
        sip_corpus
    ]
}

df = pd.DataFrame(data)

st.bar_chart(df.set_index("Asset"))

# Insight
st.subheader("🧠 Insight")

if total_corpus > 50000000:
    st.success("✅ Strong retirement plan! You are on track.")
elif total_corpus > 20000000:
    st.warning("⚠️ Moderate plan. Consider increasing SIP or equity exposure.")
else:
    st.error("🚨 Low corpus. Immediate action recommended!")

st.markdown("---")
st.markdown("🚀 Built live using AI to demonstrate real-world impact")
