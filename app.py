import streamlit as st
import matplotlib.pyplot as plt
import random
import math

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Finance Buddy 💰", page_icon="💡", layout="centered")

# -------------------------
# Theme Toggle
# -------------------------
theme = st.sidebar.radio("🌗 Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        "<style>.stApp { background-color: #0E1117; color: white; }</style>", 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<style>.stApp { background-color: #FFFFFF; color: black; }</style>", 
        unsafe_allow_html=True
    )

# -------------------------
# App Title
# -------------------------
st.title("🚀 Finance Buddy – Your AI Money Coach (India Edition 🇮🇳)")
st.write("Plan smarter, save better, and grow wealth 💰")

# -------------------------
# User Inputs
# -------------------------
income = st.number_input("💵 Enter your Monthly Income (₹)", min_value=1000, step=500)

st.subheader("🛒 Enter Your Monthly Expenses")
rent = st.slider("🏠 Rent / Housing", 0, int(income), int(income * 0.3))
food = st.slider("🍲 Food & Groceries", 0, int(income), int(income * 0.2))
shopping = st.slider("🛍️ Shopping & Entertainment", 0, int(income), int(income * 0.15))
travel = st.slider("🚖 Travel & Transport", 0, int(income), int(income * 0.1))
others = st.slider("✨ Other Expenses", 0, int(income), int(income * 0.1))

total_expenses = rent + food + shopping + travel + others
savings = income - total_expenses

# -------------------------
# Display Summary
# -------------------------
st.subheader("📊 Your Money Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{income}")
col2.metric("Expenses", f"₹{total_expenses}")
col3.metric("Savings", f"₹{savings}")

# -------------------------
# Expense Breakdown Chart
# -------------------------
st.subheader("📌 Expense Breakdown")
labels = ["Rent", "Food", "Shopping", "Travel", "Others", "Savings"]
values = [rent, food, shopping, travel, others, savings]
fig, ax = plt.subplots()
ax.pie([max(0, v) for v in values], labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# -------------------------
# AI-Style Personalized Advice
# -------------------------
st.subheader("🤖 Personalized Finance Advice")
if rent > income * 0.3:
    st.warning(f"🏠 Your rent is {rent/income*100:.1f}% of income (too high). Try to keep it <30%.")
if savings < income * 0.2:
    st.error(f"💰 You’re saving only {savings/income*100:.1f}% (too low). Aim for 20%+ of income.")
else:
    st.success("✅ Good job! Your savings rate looks healthy.")

# -------------------------
# Emergency Fund Calculator
# -------------------------
st.subheader("🛡️ Emergency Fund Check")
required_fund = total_expenses * 6
st.write(f"👉 Your monthly expense = ₹{total_expenses}. You need **₹{required_fund}** as an emergency fund (6 months).")

# -------------------------
# Future Growth Simulator
# -------------------------
st.subheader("📈 Future Value of Your Savings")
years = st.slider("Select Years to Project", 1, 30, 10)
cagr = 0.12  # 12% SIP assumption
future_value = savings * (((1 + cagr) ** years - 1) / cagr) * (1 + cagr)
st.info(f"👉 If you invest ₹{savings}/month in SIP at 12% CAGR, you’ll have **₹{int(future_value):,}** in {years} years.")

# -------------------------
# Retirement Calculator
# -------------------------
st.subheader("👴 Retirement Planning")
current_age = st.number_input("Your Current Age", min_value=18, max_value=70, value=25)
retire_age = st.number_input("Planned Retirement Age", min_value=40, max_value=80, value=60)
years_left = retire_age - current_age
retirement_corpus = savings * (((1 + cagr) ** years_left - 1) / cagr) * (1 + cagr)
st.write(f"👉 By {retire_age}, you may accumulate around **₹{int(retirement_corpus):,}** if you save ₹{savings}/month.")

# -------------------------
# Gamification: Badges
# -------------------------
st.subheader("🏆 Your Money Badge")
if savings > income * 0.3:
    st.success("🥇 Gold Saver Badge – Amazing discipline!")
elif savings > income * 0.15:
    st.info("🥈 Consistent Saver Badge – Keep it up!")
elif savings > 0:
    st.warning("🥉 Starter Saver Badge – Try to save more.")
else:
    st.error("🙈 Overspender Badge – Time to fix spending.")

# -------------------------
# Extra Finance Topics
# -------------------------
st.subheader("📘 Explore Finance Topics")
topic = st.selectbox("Choose a topic:", [
    "💰 Tax Saving Tips",
    "📚 Education Planning",
    "💳 Credit Score & Cards",
    "🏡 Buying vs Renting",
    "🌍 Travel & Lifestyle",
    "🧘 Money & Mental Health",
    "🎓 Student Finance",
])

if topic == "💰 Tax Saving Tips":
    st.info("💡 Use ELSS, PPF, and NPS to save taxes under Section 80C.")
elif topic == "📚 Education Planning":
    st.info("💡 Start SIPs for education early – costs rise ~10% yearly in India.")
elif topic == "💳 Credit Score & Cards":
    st.info("💡 Pay bills on time & keep usage <30% for a good CIBIL score.")
elif topic == "🏡 Buying vs Renting":
    st.info("💡 Renting is flexible; buying builds long-term equity. EMI <30% of income.")
elif topic == "🌍 Travel & Lifestyle":
    st.info("💡 Keep travel <10% of income. Use credit card points for free trips.")
elif topic == "🧘 Money & Mental Health":
    st.info("💡 Overspending causes stress. Budgeting = peace of mind.")
elif topic == "🎓 Student Finance":
    st.info("💡 Use scholarships, part-time jobs. Avoid loans for luxury items.")

# -------------------------
# Motivational Tip
# -------------------------
tips = [
    "💡 Little drops make an ocean – start saving today!",
    "🌱 Investing early is like planting a tree – shade comes later.",
    "🪙 Gold, SIP, and FD are your best friends in India.",
    "📉 Avoid debt traps – credit card bills can grow like wildfire!",
    "🚀 Budgeting is telling money where to go, not wondering where it went.",
]
st.subheader("🌟 Finance Tip of the Day")
st.info(random.choice(tips))
