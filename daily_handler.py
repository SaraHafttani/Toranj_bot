from telegram.ext import MessageHandler, filters
from ai.daily import daily_lesson_ai

async def daily_lesson_handler(update, context):
    text = update.message.text.lower().strip()

    # اگر پیام شامل کلمات مربوط به درس روزانه بود
    if any(k in text for k in ["درس", "روزانه", "daily", "lesson"]):
        reply = daily_lesson_ai()
        await update.message.reply_text(reply, parse_mode="Markdown")