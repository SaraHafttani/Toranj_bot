from telegram.ext import MessageHandler, filters
from ai.vocab import vocab_ai

async def vocab_handler(update, context):
    text = update.message.text.strip()

    # اگر کاربر نوشت "لغت: ..."
    if text.startswith("لغت:"):
        word = text.replace("لغت:", "").strip()
    else:
        # اگر فقط یک کلمه بود (بدون فاصله)
        if " " not in text:
            word = text
        else:
            return  # جمله بود → میره برای مکالمه

    reply = vocab_ai(word)
    await update.message.reply_text(reply, parse_mode="Markdown")