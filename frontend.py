import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(page_title="Hybrid AI Chatbot", layout="centered")
st.title("🤖 Hybrid AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input},
            timeout=120
        )

        response.raise_for_status()

        bot_reply = response.json().get("reply", "")

    except requests.exceptions.Timeout:
        bot_reply = "Server timeout. Try shorter question."

    except Exception as e:
        bot_reply = f"Connection error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.write(bot_reply)
