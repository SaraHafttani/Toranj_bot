import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found")
