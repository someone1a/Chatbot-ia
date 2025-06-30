import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": message}
        ]
    }
    res = requests.post(GROQ_URL, headers=headers, json=body)
    return res.json()["choices"][0]["message"]["content"]
