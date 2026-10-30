from ai.chat import call_ai

def build_grammar_prompt(question):
    return f"""
Explain this grammar question clearly:
"{question}"

Structure:

1) Simple Explanation
2) 3 Examples
3) Comparison (if needed)
4) Common Mistakes
5) Mini Exercise (3 questions)
6) Toranj-style poetic sentence
"""

def grammar_ai(question):
    prompt = build_grammar_prompt(question)
    return call_ai(prompt)