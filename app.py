import streamlit as st
import matplotlib.pyplot as plt
import random

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
        """
        <style>
        .stApp { background-color: #0E1117; color: white; }
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFFFFF; color: black; }
        </style>
        """, unsafe_allow_html=True
    )

# -------------------------
# App Title
# -------------------------
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
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{income}")
col2.metric("Expenses", f"₹{total_expenses}")
col3.metric("Savings", f"₹{savings}")

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
# Expanded Finance Topics
# -------------------------
st.subheader("📘 Explore Finance Topics")
topic = st.selectbox("Choose a topic:", [
    "💰 Tax Saving Tips",
    "👴 Retirement Planning",
    "💼 Side Income Ideas",
    "🛡️ Insurance Importance",
    "🏦 Loan Management",
    "📚 Education Planning",
    "🏡 Buying vs Renting Home",
    "🌍 Travel & Lifestyle Planning",
    "📊 Stock Market Basics (India)",
    "💳 Credit Score & Credit Card Management",
    "🧘 Money & Mental Health",
    "🎓 Student Finance Tips"
])

if topic == "💰 Tax Saving Tips":
    st.info("💡 Use ELSS, PPF, and NPS to save taxes under Section 80C.")
elif topic == "👴 Retirement Planning":
    st.info("💡 Start investing early in mutual funds and NPS for a stress-free retirement.")
elif topic == "💼 Side Income Ideas":
    st.info("💡 Freelancing, Blogging, Online Courses, or Small E-commerce can boost your income.")
elif topic == "🛡️ Insurance Importance":
    st.info("💡 Term Insurance protects your family; Health Insurance saves medical costs.")
elif topic == "🏦 Loan Management":
    st.info("💡 Pay high-interest loans first; avoid taking loans for luxury spending.")
elif topic == "📚 Education Planning":
    st.info("💡 Start SIPs for your child’s education; education inflation is ~10% per year in India.")
elif topic == "🏡 Buying vs Renting Home":
    st.info("💡 Renting is better short-term, but buying gives long-term stability. EMI should be <30% of income.")
elif topic == "🌍 Travel & Lifestyle Planning":
    st.info("💡 Keep travel budget <10% of income; use credit card rewards for flights/hotels.")
elif topic == "📊 Stock Market Basics (India)":
    st.info("💡 Begin with Index Funds (Nifty 50, Sensex). Avoid intraday if you’re new.")
elif topic == "💳 Credit Score & Credit Card Management":
    st.info("💡 Pay bills on time. Keep credit usage <30% to maintain a good CIBIL score.")
elif topic == "🧘 Money & Mental Health":
    st.info("💡 Financial stress is real – budget planning reduces anxiety. Emergency fund = peace of mind.")
elif topic == "🎓 Student Finance Tips":
    st.info("💡 Students should learn budgeting early. Use scholarships & part-time work to avoid debt.")

# -------------------------
# Gamification: Rewards
# -------------------------
st.subheader("🏆 Your Money Badge")
if savings > income * 0.2:
    st.success("🥇 Smart Saver Badge Earned!")
elif savings > 0:
    st.info("🥈 Consistent Saver Badge Earned!")
else:
    st.error("🙈 Overspender Badge – Time to improve!")

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
