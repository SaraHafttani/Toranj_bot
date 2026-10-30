from database import add_user
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.first_name
    )

    keyboard = [
        ["📚 لغت‌یار", "✏️ گرامر‌یار"],
        ["🗣️ مکالمه", "📖 درس روزانه"],
        ["🎯 تعیین سطح", "👤 پروفایل من"],
        ["ℹ️ راهنما", "🔙 بازگشت"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = """
🌸 سلام، من ترنج هستم.

دستیار یادگیری زبان انگلیسی

می‌توانم به شما کمک کنم:

📚 لغت‌یار
✏️ گرامر‌یار
🗣️ تمرین مکالمه
📖 درس روزانه
🎯 تعیین سطح زبان

برای شروع یکی از گزینه‌های زیر را انتخاب کن.
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )