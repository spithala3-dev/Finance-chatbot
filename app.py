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
values_for_chart = [max(0, v) for v in values]

fig, ax = plt.subplots()
ax.pie(values_for_chart, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# -------------------------
# Finance Suggestions
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
# Goal Planning
# -------------------------
st.subheader("🎯 Set Your Savings Goals")
goal_name = st.text_input("Enter your goal (e.g., Bike, Trip, Phone)")
goal_amount = st.number_input("How much do you want to save for this goal? (₹)", min_value=0, step=500)

if goal_amount > 0:
    months_needed = int(goal_amount / max(savings, 1)) if savings > 0 else "∞"
    st.write(f"To achieve **{goal_name}**, you will need **{months_needed} month(s)** of current savings.")

# -------------------------
# Investment Ideas
# -------------------------
st.subheader("📈 Investment Ideas for You")
invest_options = ["SIP in Mutual Funds", "Gold / Sovereign Gold Bonds", "FD / RD", "PPF / NSC", "Stocks (Beginner friendly)"]
chosen_investment = random.choice(invest_options)
st.info(f"💡 Consider investing in **{chosen_investment}** with your savings!")

# -------------------------
# Expense Advice
# -------------------------
st.subheader("💬 Expense Advice")
expenses_dict = {"Rent": rent, "Food": food, "Shopping": shopping, "Travel": travel, "Others": others}
max_expense_category = max(expenses_dict, key=expenses_dict.get)

if max_expense_category == "Shopping":
    st.info("💡 Try limiting online shopping and impulsive buys!")
elif max_expense_category == "Travel":
    st.info("💡 Use public transport or share rides to save money!")
elif max_expense_category == "Food":
    st.info("💡 Cooking at home more often can reduce expenses.")

# -------------------------
# Quick Finance Quiz
# -------------------------
st.subheader("📝 Quick Finance Quiz")
quiz_question = "Which is safer for long-term savings in India?"
quiz_options = ["Stocks", "Gold", "FD / RD", "Cryptocurrency"]
user_answer = st.radio(quiz_question, quiz_options)

if user_answer:
    if user_answer == "FD / RD":
        st.success("✅ Correct! FD / RD is safe for long-term savings in India.")
    else:
        st.warning("⚠️ Not quite! FD / RD is safest for guaranteed returns.")

# -------------------------
# Motivational Tips
# -------------------------
tips = [
    "💡 Little drops make an ocean – start saving today!",
    "🌱 Investing early is like planting a tree – shade comes later.",
    "🪙 Gold, SIP, and FD are your best friends in India.",
    "📉 Avoid debt traps – credit card bills can grow like wildfire!",
    "🚀 A budget is telling your money where to go, instead of wondering where it went.",
    "🍎 Save on groceries by planning meals weekly.",
    "🏦 Keep a separate account for emergency funds.",
    "📊 Track every expense for better awareness.",
    "🎁 Avoid borrowing for luxury items – plan ahead instead."
]

st.subheader("🌟 Finance Tip of the Day")
st.info(random.choice(tips))
