import requests
from deep_translator import GoogleTranslator

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

def detect_target_language(text):
    text_lower = text.lower()

    if "tamil" in text_lower:
        return "ta"
    elif "hindi" in text_lower:
        return "hi"
    elif "malayalam" in text_lower:
        return "ml"
    elif "telugu" in text_lower:
        return "te"
    else:
        return None

def chat_reply(user_message):
    try:
        target_lang = detect_target_language(user_message)

        # Always generate English reasoning first
        english_prompt = (
            user_message +
            "\n\nRespond clearly in English in 3-4 short sentences."
        )

        payload = {
            "model": MODEL_NAME,
            "prompt": english_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 120
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        english_reply = response.json().get("response", "").strip()

        # Translate if needed
        if target_lang:
            translated = GoogleTranslator(
                source="auto",
                target=target_lang
            ).translate(english_reply)

            return translated

        return english_reply

    except Exception as e:
        return f"Hybrid system error: {str(e)}"
