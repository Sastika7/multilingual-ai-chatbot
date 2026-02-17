import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Multilingual AI Chatbot", layout="centered")

st.title("🤖 Multilingual AI Chatbot (Cloud Version)")

# Get HuggingFace token from Streamlit secrets
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

# -----------------------------
# MODEL QUERY FUNCTION
# -----------------------------
def query_model(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()
