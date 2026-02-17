import streamlit as st
import requests

st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# Load API key from Streamlit Secrets
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("OPENROUTER_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "Multilingual AI Chatbot"
    }

    data = {
        "model": "openchat/openchat-3.5",
        "messages
