import requests

from config import GROQ_API_KEY


def ask_groq(user_message):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
            "content": """
            You are Toranj.

            You are a Persian-speaking English tutor and assistant.

            Rules:

            - Always communicate with the user in Persian.
            - Explain grammar in Persian.
            - Explain vocabulary in Persian.
            - When teaching English, provide English examples with Persian translations.
            - If the user speaks Persian, answer in Persian.
            - If the user wants conversation practice, act as an English partner but give guidance in Persian.
            - Be friendly, motivating and supportive.
            - Keep answers clear and educational.

            Your goal is to help Persian speakers learn English.
            """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:

        response = requests.post(
            url=url,
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏳ زمان پاسخگویی تمام شد."

    except requests.exceptions.ConnectionError:
        return "🌐 اتصال به سرور برقرار نشد."

    except requests.exceptions.RequestException as e:
        return f"❌ خطا:\n{str(e)}"

    except Exception as e:
        return f"⚠️ خطای غیرمنتظره:\n{str(e)}"


def call_ai(prompt):
    return ask_groq(prompt)


def ai_conversation(message):
    return ask_groq(message)