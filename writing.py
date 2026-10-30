# ai/writing.py
from ai.chat import call_ai

def evaluate_writing(text):
    prompt = f"""
You are a CEFR English examiner.

Evaluate the student's writing.

Writing:

{text}

Score the writing in:

1. Grammar (0-5)
2. Vocabulary (0-5)
3. Sentence Structure (0-5)
4. Fluency (0-5)

Return ONLY this format:

Grammar: X
Vocabulary: X
Structure: X
Fluency: X
Total: X

Estimated Level: A1/A2/B1/B2
"""

    return call_ai(prompt)