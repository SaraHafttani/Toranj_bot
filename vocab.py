from ai.chat import call_ai

def build_vocab_prompt(word):
    return f"""
Explain the word "{word}" with:

1) Meaning (Persian)
2) Pronunciation (IPA)
3) Part of Speech
4) Collocations
5) 3 Example Sentences
6) Synonyms
7) Poetic Toranj-style sentence
"""

def vocab_ai(word):
    prompt = build_vocab_prompt(word)
    return call_ai(prompt)