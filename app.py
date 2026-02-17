import streamlit as st
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# -----------------------------
# CHECK SECRET SAFELY
# -----------------------------
if "HF_API_TOKEN" not in st.secrets:
    st.error("HF_API_TOKEN not found in Streamlit Secrets.")
    st.stop()

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

# NEW ROUTER ENDPOINT
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------
# FUNCTION TO CALL MODEL
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

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

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
