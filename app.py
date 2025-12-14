# =========================================================
# JEE ELITE ADVANCED SYSTEM — PURE DARK MONK UI
# Single File • Fully Fixed • Production Ready
# Save as: app.py
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import os
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="JEE Elite Advanced",
    page_icon="🌑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- PURE BLACK DARK MONK UI ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #000000 !important;
    color: #e5e5e5;
    font-family: Inter, sans-serif;
}
h1, h2, h3 { color: #ffffff; }
.stButton>button {
    background-color: #111;
    color: #fff;
    border-radius: 10px;
    border: 1px solid #333;
}
.stAlert { background-color: #111 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- FORCE RESET ----------------
if st.button("🔁 Force Full Reset"):
    st.session_state.clear()
    st.experimental_rerun()

# ---------------- SESSION INIT ----------------
if "last_reset" not in st.session_state:
    st.session_state.last_reset = date.today()
if "todos" not in st.session_state:
    st.session_state.todos = ["", "", ""]
if "todo_done" not in st.session_state:
    st.session_state.todo_done = [False, False, False]
if "day_ended" not in st.session_state:
    st.session_state.day_ended = False

# ---------------- AUTO DAILY RESET ----------------
today_date = date.today()
if st.session_state.last_reset != today_date:
    st.session_state.todos = ["", "", ""]
    st.session_state.todo_done = [False, False, False]
    st.session_state.day_ended = False
    st.session_state.last_reset = today_date

# ---------------- HEADER ----------------
st.title("🌑 JEE Elite Advanced System")
st.caption("Discipline > Motivation | Monk Mode")

# ---------------- DAILY QUOTE ----------------
quotes = [
    "No zero days.",
    "Average is the enemy.",
    "Silence builds champions.",
    "IIT is earned daily.",
    "Focus decides fate."
]

daily_quote = quotes[today_date.toordinal() % len(quotes)]
st.info(f"🧠 Quote: **{daily_quote}**")
# ---------------- CALENDAR ----------------
st.subheader("📅 Today")
st.write(today_date.strftime("%A, %d %B %Y"))

# ---------------- 30 MIN ONLY ME ----------------
st.subheader("🧘 30 Minutes — Only Me")
self_focus = st.checkbox("30 min no phone • no distraction")
if not self_focus:
    st.warning("⚠️ Mandatory mental discipline block")

# ---------------- TODO ----------------
st.header("✅ Mandatory Daily Tasks (3)")
for i in range(3):
    st.session_state.todos[i] = st.text_input(
        f"Task {i+1}", st.session_state.todos[i]
    )
    st.session_state.todo_done[i] = st.checkbox(
        "Completed", st.session_state.todo_done[i], key=f"todo_{i}"
    )

if all(st.session_state.todo_done):
    st.success("🔥 All tasks completed")
else:
    st.warning("⚠️ Incomplete tasks will carry forward")

# ---------------- MODE ----------------
mode = st.radio(
    "🎯 Preparation Mode",
    ["JEE Main", "JEE Advanced"],
    horizontal=True
)

# ---------------- COUNTDOWN ----------------
st.header("⏳ JEE Countdown")
now = datetime.now()
jee_main = datetime(2027, 1, 25)
jee_adv = datetime(2027, 5, 30)

c1, c2 = st.columns(2)
with c1:
    st.metric("📘 JEE Main", (jee_main - now).days)
with c2:
    st.metric("📕 JEE Advanced", (jee_adv - now).days)

# ---------------- STUDY INPUT ----------------
st.header("🧮 Study Log")

study_hours = st.slider("Study Hours", 0.0, 16.0, 0.0, 0.5)
math_q = st.number_input("Math Questions", 0, 300, 0)
phy_q = st.number_input("Physics Questions", 0, 300, 0)
chem_q = st.number_input("Chemistry Questions", 0, 300, 0)

# -------- Accuracy OPTIONAL --------
use_accuracy = st.checkbox("Include Accuracy (%)")
if use_accuracy:
    accuracy = st.slider("Accuracy %", 0, 100, 0)
else:
    accuracy = 0

revision = st.slider("Revision Quality (0–10)", 0, 10, 0)

# ---------------- SCORING ----------------
weight = 1.4 if mode == "JEE Advanced" else 1.2

score = min(
    100,
    round(
        (study_hours * 3
         + (math_q + phy_q + chem_q) * weight * 0.5
         + accuracy * 0.2
         + revision * 10) / 10,
        2
    )
)

st.metric("🔥 Daily Score", f"{score} / 100")

# ---------------- AUTO SAVE (SAFE DF INIT) ----------------
file_path = "jee_elite_history.csv"

row = {
    "Date": today_date.strftime("%Y-%m-%d"),
    "Score": score,
    "TasksCompleted": sum(st.session_state.todo_done),
    "Focus30Min": self_focus
}

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=row.keys())

if row["Date"] not in df["Date"].values:
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

df.to_csv(file_path, index=False)

# ---------------- END OF DAY GRAPH ----------------
st.header("📊 Consistency")
if st.session_state.day_ended:
    df["Date"] = pd.to_datetime(df["Date"])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Date"], df["Score"], marker="o", linewidth=2)
    ax.axhline(70, linestyle="--")
    ax.set_ylabel("Score")
    ax.set_title("Daily Performance")
    st.pyplot(fig)
else:
    st.info("Graph will appear at end of day")

# ---------------- MONTHLY REVIEW (FIXED) ----------------
def generate_monthly_review(df):
    today = date.today()
    last_day = pd.Period(today, freq="M").days_in_month
    if today.day != last_day:
        return

    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])

    month_df = df_copy[
        (df_copy["Date"].dt.month == today.month) &
        (df_copy["Date"].dt.year == today.year)
    ]

    if month_df.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(month_df["Date"], month_df["Score"], marker="o", linewidth=2)
    ax.set_title(f"{today.strftime('%B')} Performance")
    plt.savefig("monthly_review.png")
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"{today.strftime('%B')} JEE Monthly Review", ln=True, align="C")
    pdf.image("monthly_review.png", x=10, y=30, w=190)
    pdf.output(f"monthly_review_{today.strftime('%Y_%m')}.pdf")

generate_monthly_review(df)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style="display:flex; justify-content:space-between; font-size:13px; color:#888;">
    <div>Something big to be achieved</div>
    <div>Powered by ChatGPT & Pirate</div>
</div>
""", unsafe_allow_html=True)
