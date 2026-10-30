from telegram import Update
from telegram.ext import ContextTypes


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📖 راهنمای ترنج

🔹 لغت:
لغت: beautiful

🔹 گرامر:
گرامر: present perfect

🔹 درس روزانه:
درس روزانه

🔹 مکالمه:
Hello, how are you?

🔹 ترجمه:
I love learning English.
"""

    await update.message.reply_text(text)