import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Personal Finance Chatbot",
                   page_icon="💰",
                   layout="wide")

st.markdown(
    """
    <style>
    .title {font-size:38px; font-weight:700; margin-bottom:0; color:#1E293B;}
    .subtitle {color:#475569; margin-top:0; margin-bottom:20px;}
    .user-bubble {background-color:#DCFCE7; padding:10px 15px; border-radius:12px; margin:6px 0; max-width:80%; float:right; clear:both;}
    .bot-bubble {background-color:#F1F5F9; padding:10px 15px; border-radius:12px; margin:6px 0; max-width:80%; float:left; clear:both;}
    .clear {clear:both;}
    .card {background:#ffffff; padding:16px; border-radius:16px; box-shadow:0 2px 10px rgba(0,0,0,0.06);}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">💬 Personal Finance Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your friendly assistant for savings, tax, and investments.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 Profile")
    name = st.text_input("Your Name", "Guest")
    user_type = st.selectbox("Who are you?", ["Student", "Professional"])
    st.write("---")
    st.caption("💡 Tip: Ask me about 'tax', 'budget', 'loan', or 'investment'.")

st.header("📊 Budget Summary")
income = st.number_input("Monthly income (₹)", min_value=0.0, step=1000.0, format="%.2f")
expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, step=1000.0, format="%.2f")

def format_money(x):
    return f"₹{x:,.0f}"

if income > 0:
    savings = income - expenses
    savings_rate = (savings / income * 100) if income > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", format_money(income))
    col2.metric("Expenses", format_money(expenses))
    col3.metric("Savings", format_money(savings), f"{savings_rate:.1f}%")

    if savings < 0:
        st.error("⚠️ You are overspending — expenses are higher than income!")
    elif savings == 0:
        st.warning("😐 You are breaking even. Try to cut a few expenses to start saving.")
    else:
        st.success("🎉 Great! You are saving money every month!")
        if user_type == "Student":
            st.info("✨ As a student, save at least 20% of your pocket money/income. Small SIPs (₹500/month) can grow big over time.")
        else:
            st.info("✨ As a professional, aim to save 30% of income. Use ELSS, PPF, NPS for tax benefits and long-term growth.")

st.header("💬 Chat with your Finance Buddy")
if "messages" not in st.session_state:
    st.session_state.messages = []

def bot_reply(user_msg):
    msg = user_msg.lower()
    if "tax" in msg:
        return "🧾 To save tax, you can invest in ELSS, PPF, NPS, or Insurance under Section 80C."
    elif "investment" in msg or "invest" in msg:
        return "📈 A safe start: Build an emergency fund, then start SIPs in index funds and keep some fixed income."
    elif "loan" in msg or "emi" in msg:
        return "💳 Keep total EMIs below 30% of your income. Pay credit card dues fully each month."
    elif "budget" in msg or "save" in msg:
        return "💡 Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings."
    else:
        return "🤔 I don't know that exactly, but start by tracking expenses and saving a small amount every month."

user_input = st.text_input("Ask me (e.g. 'How to save tax?')")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append({"role": "bot", "text": bot_reply(user_input)})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["text"]}</div><div class="clear"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["text"]}</div><div class="clear"></div>', unsafe_allow_html=True)

st.write("---")
st.caption("Made with ❤️ using Streamlit — your beginner-friendly finance buddy.")
