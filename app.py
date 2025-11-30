import streamlit as st
from transformers import pipeline
import numpy as np
import random
from chatbot import chat_with_bot, generate_affirmation


# ---------------------------
# STREAMLIT CONFIG
# ---------------------------
st.set_page_config(
    page_title="MoodMate AI",
    page_icon="🧠",
    layout="centered",
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown(
    """
    <style>
    .title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-top: -20px;
        background: linear-gradient(90deg, #8e44ad, #3498db);
        -webkit-background-clip: text;
        color: transparent;
    }

    .subtext {
        text-align: center;
        color: #bbb;
        font-size: 17px;
        margin-top: -10px;
    }

    .bubble {
        padding: 18px;
        border-radius: 12px;
        background-color: #1e1e1e20;
        margin-bottom: 15px;
    }

    .mood-circle {
        font-size: 62px;
        text-align: center;
        margin-bottom: 6px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# LOAD TRANSFORMER MODEL
# ---------------------------
@st.cache_resource(show_spinner=True)
def load_model():
    return pipeline("sentiment-analysis")

classifier = load_model()

# ---------------------------
# EMOJI MAPPING
# ---------------------------
def mood_to_emoji(mood):
    mapping = {
        "POSITIVE": "😄",
        "NEGATIVE": "😔",
        "NEUTRAL": "😐"
    }
    return mapping.get(mood, "🙂")

# ---------------------------
# STATIC AFFIRMATIONS & TIPS
# ---------------------------
AFFIRMATIONS = {
    "POSITIVE": [
        "You're glowing today — keep shining!",
        "Your energy is magnetic. Own it!",
        "You're on the right path. Trust yourself."
    ],
    "NEGATIVE": [
        "It's okay to feel down — you’re stronger than you think.",
        "Even the moon has phases. This too will pass.",
        "You deserve rest, patience, and kindness — especially from yourself."
    ],
    "NEUTRAL": [
        "Breathe. Center yourself. You’re doing great.",
        "Balance is a superpower — and you have it.",
        "Stillness can be clarity in disguise."
    ]
}

TIPS = {
    "POSITIVE": [
        "Capitalize on your energy: Break big tasks today!",
        "Perfect moment to start something new.",
        "Focus on your top 3 priorities — you're primed for impact!"
    ],
    "NEGATIVE": [
        "Start with a 5-minute task to reset momentum.",
        "Clean your workspace for an instant mental refresh.",
        "Do one small win — build from there."
    ],
    "NEUTRAL": [
        "Sort your tasks by importance — clarity first.",
        "Take a short walk and organize your thoughts.",
        "Set a simple goal for the next hour."
    ]
}

# ---------------------------
# HEADER
# ---------------------------
st.markdown("<h1 class='title'>MoodMate AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Mood Analyzer + Emotional Support Chatbot</p>", unsafe_allow_html=True)
st.write("")

# ---------------------------
# TABS — Mood Analyzer & Chatbot
# ---------------------------
tab1, tab2 = st.tabs(["🧠 Mood Analyzer", "💬 AI Chatbot"])

# --------------------------------------------------------------------
# TAB 1 — MOOD ANALYZER
# --------------------------------------------------------------------
with tab1:
    st.subheader("How are you feeling today?")

    text = st.text_area(
        "Describe your mood:",
        height=140,
        placeholder="Write your thoughts, feelings, or your day…"
    )

    if st.button("Analyse My Mood 🔍", use_container_width=True):
        if not text.strip():
            st.warning("Write something first chhotu 😭")
        else:
            with st.spinner("Understanding your mood…"):
                result = classifier(text)[0]
                mood = result["label"]
                score = result["score"]

            emoji = mood_to_emoji(mood)

            st.markdown(f"<div class='mood-circle'>{emoji}</div>", unsafe_allow_html=True)
            st.markdown(f"### Mood: `{mood}`")
            st.progress(score)

            # ------- STATIC AFFIRMATION
            st.markdown("### 💜 Affirmation")
            st.markdown(f"<div class='bubble'>{random.choice(AFFIRMATIONS[mood])}</div>", unsafe_allow_html=True)

            # ------- STATIC PRODUCTIVITY TIP
            st.markdown("### ⚡ Productivity Tip")
            st.markdown(f"<div class='bubble'>{random.choice(TIPS[mood])}</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------
            # 🌟 NEW — AI DAILY AFFIRMATION (Gemini)
            # --------------------------------------------------------------------
            st.markdown("### ✨ AI Daily Affirmation")

            with st.spinner("Crafting your personalized affirmation…"):
                ai_aff = generate_affirmation(mood, text)

            st.markdown(
                f"""
                <div class='bubble' style='background: linear-gradient(90deg,#8e44ad30,#3498db30); 
                border-left: 4px solid #8e44ad;'>
                    {ai_aff}
                </div>
                """,
                unsafe_allow_html=True,
            )


# --------------------------------------------------------------------
# TAB 2 — CHATBOT
# --------------------------------------------------------------------
with tab2:
    st.subheader("Talk to MoodMate's AI Support Bot")

    chat_input = st.text_area(
        "Say something:",
        placeholder="Tell me what’s on your mind…",
        height=120
    )

    if st.button("Send Message 💬", use_container_width=True):
        if not chat_input.strip():
            st.warning("At least say hi chhotu 😭")
        else:
            with st.spinner("Thinking…"):
                reply = chat_with_bot(chat_input)

            st.markdown("### 🤖 AI Response")
            st.markdown(f"<div class='bubble'>{reply}</div>", unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>Made with 💜 by Raghav</p>", unsafe_allow_html=True)
