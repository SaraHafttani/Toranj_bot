from database import init_db
from telegram import BotCommand  # <--- ۱. این کتابخانه جدید اضافه شد
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters
)

from config import TELEGRAM_TOKEN

from handlers.router import message_router
from handlers.start import start_handler
from handlers.help import help_handler


# ۲. این تابع جدید وظیفه داره منوی دستورات رو به تلگرام معرفی کنه
async def post_init(application: Application):
    commands = [
        BotCommand("start", "شروع به کار با ترنج 🌸"),
        BotCommand("help", "راهنمای استفاده از ربات 📖")
    ]
    await application.bot.set_my_commands(commands)


def main():
    init_db()
    
    # ۳. اینجا post_init رو به ساختار ربات اضافه کردیم
    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).post_init(post_init).build()

    # دستور استارت
    app.add_handler(
        CommandHandler(
            "start",
            start_handler
        )
    )

    # دستور راهنما
    app.add_handler(
        CommandHandler(
            "help",
            help_handler
        )
    )

    # تمام پیام‌های متنی
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_router
        )
    )

    print("✅ Bot is running and Menu commands are set...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()