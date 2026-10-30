import requests
from config import GROQ_API_KEY

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
)

print(response.status_code)
print(response.json())