# app.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Configure API key (you can also use environment variables)
load_dotenv()
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY"))

# Create the model with system instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
You are a friendly, professional assistant for Paves Technologies.

Your job is to help users learn more about the company, its services, culture, clients, products, and values.

You should speak clearly, warmly, and respectfully — like a helpful team member from Paves.

If the user asks about anything unrelated to Paves Technologies (e.g. general knowledge, news, jokes, AI, weather, politics, etc.), respond **only** with:

"Sorry, I can only assist with queries related to Paves Technologies."

Never break this rule.
"""
)

# App UI configuration
st.set_page_config(page_title="Paves Assistant", page_icon="💼", layout="centered")

st.title("💼 Paves Technologies Assistant")
st.markdown("Welcome! Ask me anything about **Paves Technologies**. _(Type only company-related questions.)_")

# Chat history using session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input box
user_input = st.chat_input("Ask about Paves Technologies...")

if user_input:
    # Add user input to chat history
    st.session_state.chat_history.append(("user", user_input))

    # Generate response using Gemini
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.chat_history.append(("bot", bot_reply))

# Display full conversation
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").markdown(f"**You:** {message}")
    else:
        st.chat_message("assistant").markdown(message)
