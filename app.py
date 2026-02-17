import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")
st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# Load HF token safely
try:
    HF_TOKEN = st.secrets["HF_API_TOKEN"]
except:
    st.error("HF_API_TOKEN not found in Streamlit Secrets.")
    st.stop()

# Create client using new router system
client = InferenceClient(
    model="microsoft/DialoGPT-small",
    token=HF_TOKEN,
)

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

    try:
        response = client.chat_completion(
            messages=[
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"Model error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)
