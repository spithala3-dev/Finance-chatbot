# app.py
import streamlit as st
import matplotlib.pyplot as plt
import random
import io
from fpdf import FPDF
import math
from datetime import datetime

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Finance Buddy 💰", page_icon="💡", layout="centered")

# -------------------------
# Theme Toggle (Improved)
# -------------------------
theme = st.sidebar.radio("🌗 Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("<style>.stApp { background-color: #0E1117; color: #E5E7EB; }</style>", unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #F8FAFC; color: #0F172A; }
        .stTextInput>div>input { color: #0F172A; }
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# Title
# -------------------------
st.title("🚀 Finance Buddy – Your AI Money Coach")
st.write("Real-time support, step-by-step action plans, and downloadable reports — all in one place.")

# -------------------------
# Session state defaults (persist slider values & chat)
# -------------------------
if "income" not in st.session_state:
    st.session_state.income = 30000
if "rent" not in st.session_state:
    st.session_state.rent = int(st.session_state.income * 0.3)
if "food" not in st.session_state:
    st.session_state.food = int(st.session_state.income * 0.2)
if "shopping" not in st.session_state:
    st.session_state.shopping = int(st.session_state.income * 0.15)
if "travel" not in st.session_state:
    st.session_state.travel = int(st.session_state.income * 0.1)
if "others" not in st.session_state:
    st.session_state.others = int(st.session_state.income * 0.1)
if "support_history" not in st.session_state:
    st.session_state.support_history = []  # list of (role, text) tuples

# -------------------------
# Inputs: Income + Expenses
# -------------------------
with st.expander("🧾 Income & Monthly Expenses (expand to edit)", expanded=True):
    income = st.number_input("💵 Monthly Income (₹)", min_value=1000, step=500, value=st.session_state.income)
    st.session_state.income = income

    rent = st.slider("🏠 Rent / Housing", 0, int(income), st.session_state.rent, key="rent")
    food = st.slider("🍲 Food & Groceries", 0, int(income), st.session_state.food, key="food")
    shopping = st.slider("🛍️ Shopping & Entertainment", 0, int(income), st.session_state.shopping, key="shopping")
    travel = st.slider("🚖 Travel & Transport", 0, int(income), st.session_state.travel, key="travel")
    others = st.slider("✨ Other Expenses", 0, int(income), st.session_state.others, key="others")

# -------------------------
# Computation
# -------------------------
total_expenses = rent + food + shopping + travel + others
savings = income - total_expenses
savings_pct = (savings / income * 100) if income else 0

# -------------------------
# Summary & Chart
# -------------------------
st.subheader("📊 Quick Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{income:,}")
col2.metric("Expenses", f"₹{total_expenses:,}")
col3.metric("Savings", f"₹{savings:,} ({savings_pct:.1f}% )")

st.subheader("📌 Expense Breakdown")
labels = ["Rent", "Food", "Shopping", "Travel", "Others", "Savings"]
values = [rent, food, shopping, travel, others, max(0, savings)]

fig, ax = plt.subplots(figsize=(5,4))
ax.pie([max(0, v) for v in values], labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'})
ax.axis("equal")
st.pyplot(fig)

# Save chart to bytes for PDF/download
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight")
buf.seek(0)

# -------------------------
# Real-time Support: rule-based solver
# -------------------------
st.subheader("🆘 Live Finance Support")
st.write("Describe your problem (budget, goal, debt, unexpected expense) and get an immediate step-by-step plan.")

with st.form(key="support_form", clear_on_submit=False):
    user_msg = st.text_input("What's your immediate issue or question?", key="user_msg")
    submit = st.form_submit_button("Get Support")
    if submit and user_msg.strip():
        # Save to history
        st.session_state.support_history.append(("user", user_msg))

        # RULE-BASED ANALYSIS (context aware)
        reply_lines = []
        severity = "Normal"

        # simple keyword checks
        text = user_msg.lower()
        if any(k in text for k in ["i lost job", "lost job", "job loss", "unemployed", "fired"]):
            severity = "High"
            reply_lines.append("🔴 **Immediate**: Pause non-essential payments and move to your emergency fund.")
            reply_lines.append("1. Notify your bank about temporary hardship if loan/EMI due.")
            reply_lines.append("2. Cut discretionary expenses (shopping, subscriptions).")
            reply_lines.append("3. Apply for short-term gigs / freelancing. Create a prioritized job-application plan.")
            reply_lines.append("4. If you don't have emergency fund, consider family support / community options.")
        elif any(k in text for k in ["debt", "loan", "can't pay", "overdue", "credit card"]):
            severity = "High"
            reply_lines.append("🔴 **Debt Action Plan**:")
            reply_lines.append("1. List all loans & interest rates (highest first).")
            reply_lines.append("2. Contact lenders: ask for hardship plans / negotiate lower EMI.")
            reply_lines.append("3. Pay minimums to avoid defaults. Use balance transfer cautiously.")
            reply_lines.append("4. Create a weekly cash flow sheet—cut non-essentials immediately.")
        elif any(k in text for k in ["goal", "save for", "trip", "phone", "bike", "home", "wedding"]):
            reply_lines.append("🟡 **Goal Planner**:")
            reply_lines.append(f"1. Goal: {user_msg.strip()}")
            reply_lines.append(f"2. With current savings ₹{savings:,}/month, timeline estimate: {('∞' if savings<=0 else str(math.ceil( (int(''.join(filter(str.isdigit, user_msg)) or 0))/savings ) + ' months'))}")
            reply_lines.append("3. Small wins: set auto-transfer each salary day to a goal account.")
        elif any(k in text for k in ["overspend", "can't save", "impulse", "shopping too much"]):
            reply_lines.append("🟡 **Spend Control Plan**:")
            reply_lines.append("1. Set a weekly spending cash envelope for discretionary buys.")
            reply_lines.append("2. Unsubscribe from shopping apps' notifications; delay purchases 48 hrs.")
            reply_lines.append("3. Setup a small automations: 10% to SIP on payday.")
        else:
            # Generic contextual advice using current input data
            if savings <= 0:
                severity = "High"
                reply_lines.append("🔴 Your monthly expenses exceed or equal income. Immediate actions:")
                reply_lines.append("1. Reduce discretionary categories: shopping & travel.")
                reply_lines.append("2. Re-budget: try to get savings to at least 5% within 1 month.")
                reply_lines.append("3. Consider temporary side work to cover the gap.")
            elif savings_pct < 10:
                reply_lines.append("🟠 You are saving but not enough. Try these steps:")
                reply_lines.append("1. Increase SIP by small incremental amounts (₹500) monthly.")
                reply_lines.append("2. Aim to lower shopping by 30% this month for quick gains.")
            else:
                reply_lines.append("🟢 Your finances look stable. For improvement:")
                reply_lines.append("1. Diversify savings: SIP, FD, and small gold allocation.")
                reply_lines.append("2. Setup 6-month emergency fund target and automatic transfers.")

        # Create a composed reply
        composed = f"**Support Severity:** {severity}\n\n" + "\n".join(reply_lines)
        st.session_state.support_history.append(("bot", composed))
        st.experimental_rerun()

# Display chat history
if st.session_state.support_history:
    st.write("###### Support Chat History (persisted this session)")
    for role, text in st.session_state.support_history[::-1]:
        if role == "user":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Buddy:** {text}")

# -------------------------
# Automated Personalized Recommendations (live)
# -------------------------
st.subheader("🤖 Instant Recommendations")
recos = []
if rent > income * 0.35:
    recos.append(("Housing", f"Rent is {rent/income*100:.1f}% — reduce to <30% or negotiate."))
if shopping > income * 0.12:
    recos.append(("Shopping", f"Shopping at {shopping/income*100:.1f}% — cut impulsive buys, set a weekly cap."))
if savings <= 0:
    recos.append(("Urgent", "Expenses >= Income. Immediate: cut discretionary spends; find short-term income."))
if savings > 0:
    recos.append(("Grow", f"Invest ₹{int(savings*0.5)}/month into SIP; keep ₹{int(savings*0.3)} for FD/RD; ₹{int(savings*0.2)} emergency savings."))
for t, m in recos:
    st.info(f"**{t}** — {m}")

# -------------------------
# Calculators: Emergency, Future, Retirement (compact)
# -------------------------
st.subheader("⚙️ Calculators (Quick)")
required_emergency = total_expenses * 6
st.write(f"• Emergency Fund (6 months): ₹{required_emergency:,}")

# Future value monthly SIP formula
years = st.slider("Project SIP growth for (years)", 1, 30, 10, key="proj_years")
cagr = st.number_input("Expected annual return (CAGR %) for SIP", min_value=1.0, max_value=30.0, value=12.0) / 100.0
if savings > 0:
    fv = savings * (((1 + cagr) ** years - 1) / cagr) * (1 + cagr)
    st.write(f"• If you invest ₹{savings}/month for {years} years at {cagr*100:.1f}%, you'll get ~ ₹{int(fv):,}")
else:
    st.write("• No monthly savings to project. Increase savings to use the SIP projection.")

# Retirement quick calc
st.subheader("👴 Retirement Snapshot")
current_age = st.number_input("Your current age", min_value=18, max_value=70, value=25, key="age")
retire_age = st.number_input("Planned retirement age", min_value=40, max_value=80, value=60, key="retire_age")
years_left = max(0, retire_age - current_age)
if savings > 0:
    corp = savings * (((1 + cagr) ** years_left - 1) / cagr) * (1 + cagr)
    st.write(f"• Estimated corpus at {retire_age}: ₹{int(corp):,}")
else:
    st.write("• Increase monthly savings to build retirement corpus.")

# -------------------------
# Badges & Progress (visual)
# -------------------------
st.subheader("🏆 Badges & Goal Progress")
if savings > income * 0.3:
    st.success("🥇 Gold Saver")
elif savings > income * 0.15:
    st.info("🥈 Silver Saver")
elif savings > 0:
    st.warning("🥉 Starter Saver")
else:
    st.error("🙈 Overspender — urgent fix needed")

# -------------------------
# Downloadable Report: PDF generator
# -------------------------
st.subheader("📥 Download Your Report")
report_name = st.text_input("Give your report a name (optional):", value=f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M')}")
if st.button("🔍 Generate & Preview Report (PDF)"):
    # build a simple PDF using fpdf
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 8, txt="Finance Buddy - Report", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(4)

    # summary table
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, txt=f"Income: ₹{income:,}", ln=True)
    pdf.cell(0, 6, txt=f"Total Expenses: ₹{total_expenses:,}", ln=True)
    pdf.cell(0, 6, txt=f"Savings: ₹{savings:,} ({savings_pct:.1f}%)", ln=True)
    pdf.cell(0, 6, txt=f"Emergency Fund (6m): ₹{required_emergency:,}", ln=True)
    pdf.ln(4)

    # Recommendations
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, txt="Top Recommendations:", ln=True)
    pdf.set_font("Arial", size=10)
    for i, (t, m) in enumerate(recos, 1):
        pdf.multi_cell(0, 5, txt=f"{i}. {t} - {m}")

    pdf.ln(6)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, txt="Recent Support Chat (latest first):", ln=True)
    pdf.set_font("Arial", size=9)
    # include last 6 messages
    for role, msg in st.session_state.support_history[-6:][::-1]:
        prefix = "You:" if role == "user" else "Buddy:"
        pdf.multi_cell(0, 5, txt=f"{prefix} {msg}")

    # Insert chart image
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, txt="Expense Breakdown Chart", ln=True)
    pdf.ln(2)
    # write image from buffer
    img_buf = buf
    img_buf.seek(0)
    # save image to a temporary in-memory PNG then embed
    pdf.image(img_buf, x=15, y=None, w=180)

    # output pdf bytes
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.session_state.last_pdf = pdf_output
    st.success("PDF generated. Use the download button below to save it.")

if "last_pdf" in st.session_state:
    st.download_button("⬇️ Download Report (PDF)", data=st.session_state.last_pdf, file_name=f"{report_name}.pdf", mime="application/pdf")

# also allow CSV/JSON download of raw numbers
import json, csv
summary = {
    "income": income,
    "rent": rent,
    "food": food,
    "shopping": shopping,
    "travel": travel,
    "others": others,
    "total_expenses": total_expenses,
    "savings": savings,
    "savings_pct": round(savings_pct, 2)
}
csv_buf = io.StringIO()
writer = csv.writer(csv_buf)
writer.writerow(["field", "value"])
for k, v in summary.items():
    writer.writerow([k, v])
csv_bytes = csv_buf.getvalue().encode()
st.download_button("⬇️ Download Summary (CSV)", data=csv_bytes, file_name=f"{report_name}.csv", mime="text/csv")

# allow chart download separately
st.download_button("⬇️ Download Chart (PNG)", data=buf, file_name=f"{report_name}_chart.png", mime="image/png")

# -------------------------
# Final tips
# -------------------------
st.write("---")
st.info("Tip: Use the Live Support to describe urgent problems (job loss, debt, overdue). The assistant will give you a practical step-by-step plan immediately.")
