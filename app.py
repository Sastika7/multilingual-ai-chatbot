import streamlit as st
import requests

st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

if "HF_API_TOKEN" not in st.secrets:
    st.error("HF_API_TOKEN not found in Streamlit Secrets.")
    st.stop()

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Model error: {response.text}"

    result = response.json()

    if isinstance(result, list):
        return result[0]["generated_text"]

    return str(result)

if "messages" not in st.session_state:
    st.session_state.messages = []

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

    prompt = f"""
    Answer clearly.
    If asked to respond in Tamil, Hindi, Malayalam, or Telugu,
    respond ONLY in that language.

    Question:
    {user_input}
    """

    reply = query_model(prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)
