import streamlit as st
import requests

st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# Load API key
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("OPENROUTER_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
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
        "model": "mistralai/mistral-7b-instruct",
        "messages": st.session_state.messages
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        response_json = response.json()

        if "choices" in response_json:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            reply = f"Error: {response_json}"

    except Exception as e:
        reply = f"Request failed: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)
