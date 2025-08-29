import streamlit as st
import matplotlib.pyplot as plt
import random

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Finance Buddy 💰", page_icon="💡", layout="centered")

st.title("🚀 Finance Buddy – Your Indian Money Planner")
st.write("Welcome! Let's plan your money smartly 🇮🇳💰")

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
# Display Results
# -------------------------
st.subheader("📊 Your Money Summary")
st.write(f"**Total Income:** ₹{income}")
st.write(f"**Total Expenses:** ₹{total_expenses}")
st.write(f"**Savings:** ₹{savings}")

# -------------------------
# Chart Visualization
# -------------------------
st.subheader("📌 Expense Breakdown")
labels = ["Rent", "Food", "Shopping", "Travel", "Others", "Savings"]
values = [rent, food, shopping, travel, others, savings]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# -------------------------
# Finance Suggestions (Indian Style)
# -------------------------
st.subheader("💡 Smart Suggestions for You")

if savings > 0:
    st.success("Great job! You are saving money ✅")
    st.write(f"👉 Put **₹{int(savings*0.5)}** in SIP (Mutual Funds)")
    st.write(f"👉 Put **₹{int(savings*0.3)}** in Fixed Deposit / RD")
    st.write(f"👉 Keep **₹{int(savings*0.2)}** as Emergency Fund")
else:
    st.error("⚠️ You are overspending! Try reducing shopping or travel expenses.")

# -------------------------
# Motivational Tips
# -------------------------
tips = [
    "💡 Little drops make an ocean – start saving today!",
    "🌱 Investing early is like planting a tree – shade comes later.",
    "🪙 Gold, SIP, and FD are your best friends in India.",
    "📉 Avoid debt traps – credit card bills can grow like wildfire!",
    "🚀 A budget is telling your money where to go, instead of wondering where it went."
]

st.subheader("🌟 Finance Tip of the Day")
st.info(random.choice(tips))
