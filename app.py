import streamlit as st
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# -----------------------------
# CHECK SECRET
# -----------------------------
if "HF_API_TOKEN" not in st.secrets:
    st.error("HF_API_TOKEN not found in Streamlit Secrets.")
    st.stop()

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------
# QUERY FUNCTION
# -----------------------------
def query_model(prompt):
    try:
        payload = {
            "inputs": prompt
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return f"Model error: {response.text}"

        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No response.")

        return str(result)

    except Exception as e:
        return f"Unexpected error: {str(e)}"

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    prompt = f"""
    Answer clearly and concisely.
    If the user asks to respond in Tamil, Hindi, Malayalam, or Telugu,
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
