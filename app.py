import streamlit as st

# --- Page Settings ---
st.set_page_config(page_title="Personal Finance Chatbot", page_icon="💰", layout="centered")

# --- Custom CSS for colors & style ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        color: #000000;
        font-family: 'Arial';
    }
    h1, h2, h3 {
        color: #1a73e8;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 8px;
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 8px;
    }
    .stInfo {
        background-color: #e7f3fe;
        color: #0c5460;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("💬 Personal Finance Chatbot (India)")
st.caption("Simple & friendly guidance for savings, taxes, and investments 🇮🇳")

# --- User Info ---
st.header("📝 User Information")
user_type = st.selectbox("Are you a student or professional?", ["Student", "Professional"])
income = st.number_input("Enter your monthly income (₹)", min_value=0.0, step=1000.0, format="%.2f")
expenses = st.number_input("Enter your monthly expenses (₹)", min_value=0.0, step=1000.0, format="%.2f")

# --- Budget Summary ---
if income > 0:
    savings = income - expenses
    st.header("📊 Budget Summary")
    st.write(f"💵 **Income**: ₹{income:,.2f}")
    st.write(f"💸 **Expenses**: ₹{expenses:,.2f}")
    st.write(f"💰 **Savings**: ₹{savings:,.2f}")

    st.header("💡 Suggestions")
    if savings <= 0:
        st.warning("⚠️ You are overspending! Reduce unnecessary expenses.")
    else:
        st.success("✅ You are saving money!")
        if user_type == "Student":
            st.write("- Save at least 20% of income.")
            st.write("- Start a small **Recurring Deposit (RD)** or **SIP**.")
        else:
            st.write("- Save at least 30% of income.")
            st.write("- Invest in **ELSS, PPF, NPS** for tax savings.")
            st.write("- Maintain an **emergency fund** (6 months expenses).")

# --- Chatbot Section ---
st.header("💬 Ask a finance question (India Focus)")

user_q = st.text_input("Type your question here:")

if user_q:
    q = user_q.lower()

    if "tax" in q:
        st.info("👉 Save tax with **ELSS, PPF, NPS**, and insurance under **80C**. Also claim HRA, 80D (medical insurance).")
    elif "investment" in q:
        st.info("👉 Best for beginners: SIPs in mutual funds, FDs for safety, and an emergency fund.")
    elif "loan" in q:
        st.info("👉 Take a loan only if necessary. Compare interest rates. Home loan is better than personal loan.")
    elif "savings" in q:
        st.info("👉 Rule of thumb: Save **30% of income**. Use RDs, FDs, or SIPs depending on your goal.")
    elif "insurance" in q:
        st.info("👉 Buy a **term life insurance** (not endowment). Always take **health insurance** for family.")
    elif "stock" in q:
        st.info("👉 Start small with mutual funds SIP. Direct stocks are risky for beginners.")
    elif "retirement" in q:
        st.info("👉 Start investing early in **NPS + Mutual Funds** for long term.")
    elif "gold" in q:
        st.info("👉 Instead of physical gold, consider **Gold ETF or Sovereign Gold Bonds**.")
    else:
        st.info("👉 I don’t know that yet. But always save regularly and invest wisely!")
