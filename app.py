# app.py
import streamlit as st
import matplotlib.pyplot as plt
import random
import io
import tempfile
import os
from fpdf import FPDF
import math
from datetime import datetime
import csv

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Finance Buddy 💰", page_icon="💡", layout="centered")

# -------------------------
# Theme Toggle (Improved Readability)
# -------------------------
theme = st.sidebar.radio("🌗 Choose Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: #E5E7EB; }
        .stTextInput>div>input, .stNumberInput>div>input { color: #E5E7EB; background-color: #111315; }
        .stSlider div, .css-1lsmgbg { color: #E5E7EB; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    # Light mode: high-contrast, non-dominating colors for controls & inputs
    st.markdown(
        """
        <style>
        /* App background and primary text */
        .stApp { background-color: #FFFFFF; color: #0F172A; }

        /* Inputs text color */
        input, textarea, .stTextInput>div>input, .stNumberInput>div>input {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
        }

        /* Buttons, metrics and cards */
        .stButton>button, .stDownloadButton>button {
            background-color: #0F172A;
            color: #FFFFFF;
            border-radius: 8px;
        }

        /* Slightly muted background for expanders / cards to avoid glare */
        .stExpander { background-color: #F8FAFC; color: #0F172A; border-radius: 8px; padding: 6px; }

        /* Chart container */
        .element-container img { background: transparent; }

        /* Metric label fix */
        .stMetric label { color: #0F172A !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# Title
# -------------------------
st.title("🚀 Finance Buddy – Your AI Money Coach")
st.write("Real-time support, actionable plans, and downloadable reports — fast & clear.")

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
if "last_pdf" not in st.session_state:
    st.session_state.last_pdf = None

# -------------------------
# Inputs: Income + Expenses
# -------------------------
with st.expander("🧾 Income & Monthly Expenses (expand to edit)", expanded=True):
    income = st.number_input(
        "💵 Monthly Income (₹)",
        min_value=1000,
        step=500,
        value=st.session_state.income,
    )
    st.session_state.income = income

    rent = st.slider("🏠 Rent / Housing", 0, int(income), st.session_state.rent, key="rent")
    food = st.slider("🍲 Food & Groceries", 0, int(income), st.session_state.food, key="food")
    shopping = st.slider(
        "🛍️ Shopping & Entertainment", 0, int(income), st.session_state.shopping, key="shopping"
    )
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
col3.metric("Savings", f"₹{savings:,} ({savings_pct:.1f}%)")

st.subheader("📌 Expense Breakdown")
labels = ["Rent", "Food", "Shopping", "Travel", "Others", "Savings"]
values = [rent, food, shopping, travel, others, max(0, savings)]

fig, ax = plt.subplots(figsize=(5, 4))
ax.pie(
    [max(0, v) for v in values],
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"linewidth": 0.5, "edgecolor": "white"},
)
ax.axis("equal")
st.pyplot(fig)

# Save chart to in-memory buffer for PNG download
chart_buf = io.BytesIO()
fig.savefig(chart_buf, format="png", bbox_inches="tight", dpi=150)
chart_buf.seek(0)

# -------------------------
# Real-time Support: rule-based solver
# -------------------------
st.subheader("🆘 Live Finance Support")
st.write("Describe a money problem (debt, job loss, goal, overspending) and get a step-by-step plan.")

with st.form(key="support_form", clear_on_submit=False):
    user_msg = st.text_input("What's your immediate issue or question?", key="user_msg")
    submit = st.form_submit_button("Get Support")
    if submit and user_msg.strip():
        # Save to history
        st.session_state.support_history.append(("user", user_msg))

        # RULE-BASED ANALYSIS (context aware)
        reply_lines = []
        severity = "Normal"

        text = user_msg.lower()
        if any(k in text for k in ["i lost job", "lost job", "job loss", "unemployed", "fired"]):
            severity = "High"
            reply_lines.append("🔴 **Immediate**: Pause non-essential payments and move to your emergency fund.")
            reply_lines.append("1. Notify lender/bank about hardship for EMI support.")
            reply_lines.append("2. Cut discretionary expenses (subscriptions, shopping).")
            reply_lines.append("3. Apply for short-term gigs / freelancing to cover next 1-2 months.")
            reply_lines.append("4. Seek state/university/community support if available.")
        elif any(k in text for k in ["debt", "loan", "can't pay", "overdue", "credit card"]):
            severity = "High"
            reply_lines.append("🔴 **Debt Action Plan**:")
            reply_lines.append("1. List loans by interest; focus on highest interest first.")
            reply_lines.append("2. Contact lenders to negotiate short-term relief or restructuring.")
            reply_lines.append("3. Pay minimums to avoid defaults; avoid new high-interest credit.")
            reply_lines.append("4. Build weekly cash flow & cut non-essential spends.")
        elif any(k in text for k in ["goal", "save for", "trip", "phone", "bike", "home", "wedding"]):
            reply_lines.append("🟡 **Goal Planner**:")
            reply_lines.append(f"1. Goal: {user_msg.strip()}")
            # try to extract a number in rupees from the message; fallback to generic
            digits = "".join(ch for ch in user_msg if ch.isdigit())
            if digits:
                goal_amount = int(digits)
                months_needed = "∞" if savings <= 0 else math.ceil(goal_amount / max(1, savings))
                reply_lines.append(f"2. Estimated timeline at current savings: {months_needed} month(s).")
            else:
                reply_lines.append("2. Provide a target amount (₹) for a specific timeline estimate.")
            reply_lines.append("3. Automate small auto-transfers to a dedicated goal account.")
        elif any(k in text for k in ["overspend", "can't save", "impulse", "shopping too much"]):
            reply_lines.append("🟡 **Spend Control Plan**:")
            reply_lines.append("1. Use a weekly cash envelope for discretionary spending.")
            reply_lines.append("2. Unsubscribe from promotional emails/apps and enforce 48hr wait before buys.")
            reply_lines.append("3. Automate 10% of income to SIP on payday.")
        else:
            # Generic contextual advice using current input data
            if savings <= 0:
                severity = "High"
                reply_lines.append("🔴 Your monthly expenses meet/exceed income. Immediate actions:")
                reply_lines.append("1. Pause discretionary spends: shopping, subscriptions, dining out.")
                reply_lines.append("2. Aim to cut costs to reach at least 5% savings within 30 days.")
                reply_lines.append("3. Look for temporary income (freelance/gigs) to cover the shortfall.")
            elif savings_pct < 10:
                reply_lines.append("🟠 You're saving but not enough. Suggestions:")
                reply_lines.append("1. Increase SIP by small increments (₹500) monthly.")
                reply_lines.append("2. Cut shopping by 30% this month to free up savings.")
            else:
                reply_lines.append("🟢 Your finances are relatively stable. Next steps:")
                reply_lines.append("1. Diversify: SIP + FD/RD + small gold allocation.")
                reply_lines.append("2. Build a 6-month emergency fund and automate contributions.")

        # Compose reply
        composed = f"**Support Severity:** {severity}\n\n" + "\n".join(reply_lines)
        st.session_state.support_history.append(("bot", composed))
        # re-run to show updated history immediately
        st.experimental_rerun()

# Display chat history (most recent first)
if st.session_state.support_history:
    st.write("###### Support Chat History (this session, newest first)")
    for role, text in reversed(st.session_state.support_history[-12:]):
        if role == "user":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Buddy:** {text}")

# -------------------------
# Instant Recommendations
# -------------------------
st.subheader("🤖 Instant Recommendations")
recos = []
if rent > income * 0.35:
    recos.append(("Housing", f"Rent is {rent/income*100:.1f}% — try to reduce to <30% or negotiate rent."))
if shopping > income * 0.12:
    recos.append(("Shopping", f"Shopping is {shopping/income*100:.1f}% — set a weekly cap and delay purchases 48 hrs."))
if savings <= 0:
    recos.append(("Urgent", "Expenses >= Income. Immediate: cut discretionary spends and seek short-term income."))
if savings > 0:
    recos.append(("Grow", f"Invest ₹{int(savings*0.5)}/month into SIP; keep ₹{int(savings*0.3)} FD/RD; ₹{int(savings*0.2)} as emergency fund."))
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
if savings > 0 and years_left > 0:
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
# Downloadable Report: PDF generator (fixed to use tempfile for image)
# -------------------------
st.subheader("📥 Download Your Report")
report_name = st.text_input(
    "Give your report a name (optional):", value=f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M')}"
)

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
        # fpdf multi_cell needs str; ensure message is shortened to prevent overflow
        pdf.multi_cell(0, 5, txt=f"{prefix} {msg}")

    # Save the chart to a temporary file and insert into PDF (FPDF expects a filename)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            tmp_path = tmpfile.name
            fig.savefig(tmp_path, format="png", bbox_inches="tight", dpi=150)

        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, txt="Expense Breakdown Chart", ln=True)
        pdf.ln(2)
        pdf.image(tmp_path, x=15, y=None, w=180)  # insert image via path (fixed)

        # produce PDF bytes
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        st.session_state.last_pdf = pdf_bytes
        st.success("PDF generated. Use the download button below to save it.")
    finally:
        # remove temp file if it was created
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

if st.session_state.last_pdf:
    st.download_button(
        "⬇️ Download Report (PDF)",
        data=st.session_state.last_pdf,
        file_name=f"{report_name}.pdf",
        mime="application/pdf",
    )

# also allow CSV/JSON download of raw numbers
summary = {
    "income": income,
    "rent": rent,
    "food": food,
    "shopping": shopping,
    "travel": travel,
    "others": others,
    "total_expenses": total_expenses,
    "savings": savings,
    "savings_pct": round(savings_pct, 2),
}
csv_buf = io.StringIO()
writer = csv.writer(csv_buf)
writer.writerow(["field", "value"])
for k, v in summary.items():
    writer.writerow([k, v])
csv_bytes = csv_buf.getvalue().encode()
st.download_button("⬇️ Download Summary (CSV)", data=csv_bytes, file_name=f"{report_name}.csv", mime="text/csv")

# allow chart download separately
st.download_button("⬇️ Download Chart (PNG)", data=chart_buf, file_name=f"{report_name}_chart.png", mime="image/png")

# -------------------------
# Final tips
# -------------------------
st.write("---")
st.info("Tip: Use Live Support for urgent problems (job loss, debt). The assistant gives pragmatic steps you can act on immediately.")
