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
        input, textarea { color: #E5E7EB !important; background-color: #111315 !important; }
        .stButton>button, .stDownloadButton>button { background-color: #1f2937; color: #E5E7EB; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    # Light mode: high-contrast, non-dominating controls
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFFFFF; color: #0F172A; }
        input, textarea { color: #0F172A !important; background-color: #FFFFFF !important; }
        .stButton>button, .stDownloadButton>button { background-color: #0F172A; color: #FFFFFF; border-radius: 6px; }
        .stExpander { background-color: #F8FAFC; color: #0F172A; border-radius: 8px; padding: 6px; }
        .stMetric label { color: #0F172A !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# Title
# -------------------------
st.title("🚀 Finance Buddy – Your AI Money Coach")
st.write("Real-time support, actionable plans, and downloadable advisor-style PDF reports.")

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
    st.session_state.support_history = []
if "last_pdf" not in st.session_state:
    st.session_state.last_pdf = None

# -------------------------
# Inputs: Income + Expenses + Goal
# -------------------------
with st.expander("🧾 Income & Monthly Expenses (expand to edit)", expanded=True):
    income = st.number_input(
        "💵 Monthly Income (₹)", min_value=1000, step=500, value=st.session_state.income
    )
    st.session_state.income = income

    rent = st.slider("🏠 Rent / Housing", 0, int(income), st.session_state.rent, key="rent")
    food = st.slider("🍲 Food & Groceries", 0, int(income), st.session_state.food, key="food")
    shopping = st.slider("🛍️ Shopping & Entertainment", 0, int(income), st.session_state.shopping, key="shopping")
    travel = st.slider("🚖 Travel & Transport", 0, int(income), st.session_state.travel, key="travel")
    others = st.slider("✨ Other Expenses", 0, int(income), st.session_state.others, key="others")

with st.expander("🎯 Savings Goal (optional)", expanded=False):
    goal_name = st.text_input("Goal name (e.g., Bike, Trip, Phone)", value="")
    goal_amount = st.number_input("Goal amount (₹)", min_value=0, step=500, value=0)
    # months_needed computed below (based on current savings)

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
c1, c2, c3 = st.columns(3)
c1.metric("Income", f"₹{income:,}")
c2.metric("Expenses", f"₹{total_expenses:,}")
c3.metric("Savings", f"₹{savings:,} ({savings_pct:.1f}%)")

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

# Save chart to in-memory buffer for direct PNG download
chart_buf = io.BytesIO()
fig.savefig(chart_buf, format="png", bbox_inches="tight", dpi=150)
chart_buf.seek(0)

# -------------------------
# Real-time Support: rule-based solver
# -------------------------
st.subheader("🆘 Live Finance Support")
st.write("Type an urgent problem (debt, job loss, goal), get an immediate practical plan.")

with st.form(key="support_form", clear_on_submit=False):
    user_msg = st.text_input("What's your immediate issue or question?", key="user_msg")
    submit = st.form_submit_button("Get Support")
    if submit and user_msg.strip():
        st.session_state.support_history.append(("user", user_msg))
        text = user_msg.lower()
        reply_lines = []
        severity = "Normal"

        if any(k in text for k in ["lost job", "job loss", "unemployed", "fired"]):
            severity = "High"
            reply_lines.extend([
                "🔴 Immediate: Pause non-essential payments and prioritize essentials.",
                "1. Notify lenders about hardship (request EMI relief).",
                "2. Cut subscriptions and discretionary spending now.",
                "3. Apply for temporary/remote gigs to cover next 1-2 months.",
                "4. Use community or family support if urgently needed."
            ])
        elif any(k in text for k in ["debt", "loan", "can't pay", "overdue", "credit card"]):
            severity = "High"
            reply_lines.extend([
                "🔴 Debt Action Plan:",
                "1. List loans by interest; target highest interest first.",
                "2. Contact lenders: request restructuring or payment holiday.",
                "3. Pay minimums to avoid defaults and prioritize essentials.",
                "4. Cut non-essential spending and create weekly cashflow."
            ])
        elif any(k in text for k in ["goal", "save for", "trip", "phone", "bike", "home", "wedding"]):
            reply_lines.append("🟡 Goal Planner:")
            digits = "".join(ch for ch in user_msg if ch.isdigit())
            if digits:
                g_amt = int(digits)
                months_needed = "∞" if savings <= 0 else math.ceil(g_amt / max(1, savings))
                reply_lines.append(f"1. Goal amount: ₹{g_amt}")
                reply_lines.append(f"2. Timeline at current savings: {months_needed} month(s).")
            else:
                reply_lines.append("1. Provide a target amount (₹) for a precise timeline.")
            reply_lines.append("2. Automate small transfers each payday into a goal account.")
        elif any(k in text for k in ["overspend", "can't save", "impulse", "shopping too much"]):
            reply_lines.extend([
                "🟡 Spend Control Plan:",
                "1. Use a weekly cash envelope for discretionary spending.",
                "2. Unsubscribe from shopping notifications; wait 48 hours before purchases.",
                "3. Automate 10% to SIP each payday."
            ])
        else:
            if savings <= 0:
                severity = "High"
                reply_lines.extend([
                    "🔴 Expenses meet/exceed income. Immediate actions:",
                    "1. Pause discretionary spending.",
                    "2. Reduce shopping/travel to reach small positive savings this month.",
                    "3. Find a short-term income source."
                ])
            elif savings_pct < 10:
                reply_lines.extend([
                    "🟠 You're saving but need more:",
                    "1. Increase SIP by ₹500 increments monthly.",
                    "2. Cut shopping by 30% this month to free funds."
                ])
            else:
                reply_lines.extend([
                    "🟢 Stable finances. To improve:",
                    "1. Diversify: SIP + FD + small gold allocation.",
                    "2. Build a 6-month emergency fund; automate transfers."
                ])

        composed = f"**Support Severity:** {severity}\n\n" + "\n".join(reply_lines)
        st.session_state.support_history.append(("bot", composed))
        st.experimental_rerun()

# Show recent history (reverse chronological)
if st.session_state.support_history:
    st.write("###### Support History (this session, newest first)")
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
    recos.append(("Housing", f"Rent is {rent/income*100:.1f}% — try to reduce to <30% or negotiate."))
if shopping > income * 0.12:
    recos.append(("Shopping", f"Shopping is {shopping/income*100:.1f}% — set a weekly cap and delay purchases 48 hrs."))
if savings <= 0:
    recos.append(("Urgent", "Expenses >= Income. Immediate: cut discretionary spends and find short-term income."))
if savings > 0:
    recos.append(("Grow", f"Invest ₹{int(savings*0.5)}/month in SIP; keep ₹{int(savings*0.3)} in FD/RD; ₹{int(savings*0.2)} emergency."))

for t, m in recos:
    st.info(f"**{t}** — {m}")

# -------------------------
# Calculators
# -------------------------
st.subheader("⚙️ Calculators (Quick)")
required_emergency = total_expenses * 6
st.write(f"• Emergency Fund (6 months): ₹{required_emergency:,}")

# Future value projection
years = st.slider("Project SIP growth for (years)", 1, 30, 10, key="proj_years")
cagr = st.number_input("Expected annual return (CAGR %) for SIP", min_value=1.0, max_value=30.0, value=12.0) / 100.0
if savings > 0:
    fv = savings * (((1 + cagr) ** years - 1) / cagr) * (1 + cagr)
    st.write(f"• If you invest ₹{savings}/month for {years} years at {cagr*100:.1f}%, you'll get ~ ₹{int(fv):,}")
else:
    st.write("• No monthly savings to project — increase savings to use SIP projection.")

# Retirement snapshot
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
# Badges & Progress
# -------------------------
st.subheader("🏆 Badges & Goal Progress")
if savings > income * 0.3:
    st.success("🥇 Gold Saver – excellent discipline!")
elif savings > income * 0.15:
    st.info("🥈 Silver Saver – good progress!")
elif savings > 0:
    st.warning("🥉 Starter Saver – increase savings gradually.")
else:
    st.error("🙈 Overspender — urgent fix needed")

# -------------------------
# PDF Generation Helper (returns bytes)
# -------------------------
def build_pdf_bytes(
    income,
    expenses_dict,
    total_expenses,
    savings,
    savings_pct,
    recos,
    support_history,
    goal_name,
    goal_amount,
    months_needed,
    fig
):
    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Finance Buddy — Personal Finance Report", ln=True, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(4)

    # Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "Summary", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"Income: ₹{income:,}", ln=True)
    pdf.cell(0, 6, f"Total Expenses: ₹{total_expenses:,}", ln=True)
    pdf.cell(0, 6, f"Savings: ₹{savings:,} ({savings_pct:.1f}%)", ln=True)
    pdf.ln(4)

    # Expenses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "Expense Breakdown", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in expenses_dict.items():
        pdf.cell(0, 6, f"{k}: ₹{v:,}", ln=True)
    pdf.ln(4)

    # Goal
    if goal_amount > 0 and goal_name.strip():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, "Goal Plan", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, f"Goal: {goal_name}", ln=True)
        pdf.cell(0, 6, f"Amount: ₹{goal_amount:,}", ln=True)
        pdf.cell(0, 6, f"Estimated months at current savings: {months_needed}", ln=True)
        pdf.ln(4)

    # Recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "Top Recommendations", ln=True)
    pdf.set_font("Arial", size=10)
    if recos:
        for i, (title, msg) in enumerate(recos, 1):
            pdf.multi_cell(0, 5, txt=f"{i}. {title}: {msg}")
    else:
        pdf.cell(0, 6, "No recommendations generated.", ln=True)
    pdf.ln(4)

    # Support chat (latest up to 8 messages)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "Recent Support Chat", ln=True)
    pdf.set_font("Arial", size=9)
    for role, m in support_history[-8:]:
        prefix = "You:" if role == "user" else "Buddy:"
        pdf.multi_cell(0, 5, txt=f"{prefix} {m}")

    # Insert chart image (requires a temp file)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            tmp_path = tmpfile.name
            fig.savefig(tmp_path, format="png", bbox_inches="tight", dpi=150)

        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, "Expense Breakdown Chart", ln=True)
        pdf.ln(2)
        pdf.image(tmp_path, x=15, y=None, w=180)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # Return PDF bytes
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes

# -------------------------
# Prepare data & months_needed for goal
# -------------------------
expenses_dict = {"Rent": rent, "Food": food, "Shopping": shopping, "Travel": travel, "Others": others}
months_needed = "∞"
if goal_amount > 0:
    months_needed = "∞" if savings <= 0 else math.ceil(goal_amount / max(1, savings))

# -------------------------
# Generate & Download PDF (as bytes) - button
# -------------------------
st.subheader("📥 Download Your Detailed Report (PDF)")

report_name = st.text_input("Report file name (without extension)", value=f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M')}")

if st.button("🔍 Generate PDF Report"):
    # Build PDF bytes (this may take a moment)
    pdf_bytes = build_pdf_bytes(
        income=income,
        expenses_dict=expenses_dict,
        total_expenses=total_expenses,
        savings=savings,
        savings_pct=savings_pct,
        recos=recos,
        support_history=st.session_state.support_history,
        goal_name=goal_name,
        goal_amount=goal_amount,
        months_needed=months_needed,
        fig=fig
    )
    st.session_state.last_pdf = pdf_bytes
    st.success("PDF report generated — use the download button below.")

if st.session_state.last_pdf:
    st.download_button(
        "⬇️ Download Report (PDF)",
        data=st.session_state.last_pdf,
        file_name=f"{report_name}.pdf",
        mime="application/pdf",
    )

# -------------------------
# Also provide CSV & PNG downloads
# -------------------------
# CSV summary
csv_buf = io.StringIO()
writer = csv.writer(csv_buf)
writer.writerow(["field", "value"])
for k, v in {
    "income": income,
    "rent": rent,
    "food": food,
    "shopping": shopping,
    "travel": travel,
    "others": others,
    "total_expenses": total_expenses,
    "savings": savings,
    "savings_pct": round(savings_pct, 2),
}.items():
    writer.writerow([k, v])
csv_bytes = csv_buf.getvalue().encode()
st.download_button("⬇️ Download Summary (CSV)", data=csv_bytes, file_name=f"{report_name}.csv", mime="text/csv")

# Chart PNG
st.download_button("⬇️ Download Chart (PNG)", data=chart_buf, file_name=f"{report_name}_chart.png", mime="image/png")

# -------------------------
# Final tips
# -------------------------
st.write("---")
st.info("Tip: Use Live Support for urgent problems. The assistant returns an actionable plan instantly. PDF reports include summary, recommendations, recent chat and the expense chart.")
