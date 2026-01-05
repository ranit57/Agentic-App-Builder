# llm/gemini_client.py

import os
import google.generativeai as genai

def get_gemini_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model
