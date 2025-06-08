import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key.strip().lower() == "your_gemini_api_key_here":
    raise ValueError("❌ API key missing or invalid. Check your .env or config.")