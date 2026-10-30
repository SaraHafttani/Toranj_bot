from telegram.ext import MessageHandler, filters
from ai.chat import ai_conversation

async def conversation_handler(update, context):
    user_text = update.message.text.strip()

    # اگر پیام کاربر یک کلمه بود → میره برای لغت‌یار
    if " " not in user_text and not user_text.startswith("لغت:"):
        return

    # اگر پیام کاربر سوال گرامری بود → میره برای گرامر‌یار
    if any(k in user_text.lower() for k in ["فرق", "grammar", "گرامر", "چیه"]):
        return

    # در غیر این صورت → مکالمه انگلیسی
    reply = ai_conversation(user_text)
    await update.message.reply_text(reply, parse_mode="Markdown")