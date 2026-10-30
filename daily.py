from ai.chat import call_ai

def build_daily_lesson_prompt():
    return """
Create a daily English lesson:

1) Vocabulary + IPA + Persian meaning + example
2) Grammar Tip
3) Mini Dialogue
4) Toranj-style poetic sentence
"""

def daily_lesson_ai():
    prompt = build_daily_lesson_prompt()
    return call_ai(prompt)