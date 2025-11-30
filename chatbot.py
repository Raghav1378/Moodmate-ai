import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="AIzaSyBRek40ZNmMvS3Y9unM0x5FiwYJ4TqUzFg")

# Load Model
model = genai.GenerativeModel("gemini-2.5-flash")

def chat_with_bot(message):
    prompt = f"""
    You are MoodMate AI's Emotional Support Assistant.

    You must:
    - Respond like a warm, friendly therapist + productivity coach.
    - Be empathetic.
    - Keep messages short, comforting, and actionable.

    User said: {message}
    """

    response = model.generate_content(prompt)
    return response.text


# 🌟 NEW — Generate AI Daily Affirmation
def generate_affirmation(mood, text):
    prompt = f"""
    Create a short, positive, uplifting affirmation for someone who is feeling {mood}.
    
    Their message was: "{text}"

    Rules:
    - 1–2 sentences max
    - very warm, gentle, comforting tone
    - NOT generic
    - emotionally supportive
    """

    response = model.generate_content(prompt)
    return response.text.strip()
