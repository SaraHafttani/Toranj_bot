from telegram.ext import MessageHandler, filters
from ai.grammar import grammar_ai

async def grammar_handler(update, context):
    text = update.message.text.strip()

    # اگر کاربر نوشت "گرامر: ..."
    if text.startswith("گرامر:"):
        question = text.replace("گرامر:", "").strip()

    else:
        # اگر پیام شامل کلمات گرامری بود
        if any(k in text.lower() for k in ["فرق", "grammar", "گرامر", "چیه"]):
            question = text
        else:
            return  # اگر سوال گرامری نبود → برگرده تا هندلرهای دیگه جواب بدن

    reply = grammar_ai(question)
    await update.message.reply_text(reply, parse_mode="Markdown")