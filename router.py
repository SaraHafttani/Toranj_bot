from database import (
    get_user,
    update_level,
    start_test,
    get_test_info,
    set_question,
    add_score,
    finish_test,
    reset_test
)

from ai.placement_test import QUESTIONS
from ai.vocab import vocab_ai
from ai.grammar import grammar_ai
from ai.daily import daily_lesson_ai
from ai.chat import ai_conversation
from ai.writing import evaluate_writing  # اضافه کردن هوش مصنوعی ارزیابی رایتینگ

# یک دیکشنری موقت در حافظه برای اینکه بفهمیم کدام کاربران منتظر ارسال رایتینگ برای تعیین سطح هستند
waiting_for_writing = set()

async def message_router(update, context):

    if not update.message or not update.message.text:
        return

    text_raw = update.message.text
    text = text_raw.strip().lower()

    user_id = update.effective_user.id

    try:

        # =====================
        # WRITING EVALUATION STATE (مرحله رایتینگ انتهای تعیین سطح)
        # =====================
        if user_id in waiting_for_writing:
            # کاربر الان باید متن رایتینگ خودش رو فرستاده باشه
            await update.message.reply_text("⏳ ترنج در حال تحلیل و ارزیابی رایتینگ شماست، لطفاً کمی صبر کنید...")
            
            # صدا زدن هوش مصنوعی برای ارزیابی رایتینگ
            evaluation_result = evaluate_writing(text_raw)
            
            await update.message.reply_text(
                f"📝 **نتیجه ارزیابی رایتینگ و تعیین سطح نهایی:**\n\n{evaluation_result}\n\n🌸 پرونده تعیین سطح شما با موفقیت بسته شد!",
                parse_mode="Markdown"
            )
            
            # پاک کردن کاربر از لیست انتظار رایتینگ
            waiting_for_writing.remove(user_id)
            return

        # =====================
        # CEFR TEST
        # =====================

        if text == "🎯 تعیین سطح":

            start_test(user_id)
            
            # اگر کاربر قبلاً توی لیست رایتینگ بود پاکش می‌کنیم
            if user_id in waiting_for_writing:
                waiting_for_writing.remove(user_id)

            await update.message.reply_text(
                "🎯 آزمون تعیین سطح آغاز شد.\n\nلطفاً فقط با a , b , c , d پاسخ بده."
            )

            await update.message.reply_text(
                QUESTIONS[0]["question"]
            )

            return

        test_info = get_test_info(user_id)

        if test_info:

            current_question, score, is_active = test_info

            if is_active == 1:

                if text in ["a", "b", "c", "d"]:

                    correct_answer = QUESTIONS[current_question]["answer"]

                    if text == correct_answer:
                        add_score(user_id)

                    current_question += 1

                    if current_question >= len(QUESTIONS):

                        finish_test(user_id)

                        final_score = score

                        if text == correct_answer:
                            final_score += 1

                        if final_score <= 5:
                            level = "A1"

                        elif final_score <= 10:
                            level = "A2"

                        elif final_score <= 15:
                            level = "B1"

                        else:
                            level = "B2"

                        update_level(
                            user_id,
                            level
                        )

                        reset_test(user_id)
                        
                        # --- بخش جدید: انتقال کاربر به مرحله رایتینگ ---
                        waiting_for_writing.add(user_id)

                        await update.message.reply_text(
                            f"""
✅ بخش اول (تستی) آزمون پایان یافت!

📊 امتیاز تستی شما:
{final_score} از {len(QUESTIONS)}

📚 سطح موقت شما: {level}

🔥 **مرحله پایانی تعیین سطح (رایتینگ):**
لطفاً یک پاراگراف کوتاه (۳ الی ۵ جمله) به **انگلیسی** درباره خودت، شغل، علایق یا برنامه‌هات بنویس و ارسال کن تا ترنج رایتینگ تو رو تحلیل کنه و سطح نهاییت رو اعلام کنه! 🌸
"""
                        )

                        return

                    set_question(
                        user_id,
                        current_question
                    )

                    await update.message.reply_text(
                        QUESTIONS[current_question]["question"]
                    )

                    return

                else:

                    await update.message.reply_text(
                        "فقط یکی از گزینه‌های a / b / c / d را وارد کن."
                    )

                    return

        # =====================
        # PROFILE
        # =====================

        if text == "👤 پروفایل من":

            user = get_user(user_id)

            if user:

                telegram_id = user[0]
                username = user[1]
                level = user[2]
                created_at = user[3]

                await update.message.reply_text(
                    f"""
👤 پروفایل شما

🌸 نام:
{username}

📚 سطح زبان:
{level}

🆔 شناسه:
{telegram_id}

📅 تاریخ عضویت:
{created_at}
"""
                )

            else:

                await update.message.reply_text(
                    "پروفایل پیدا نشد."
                )

            return

        if text == "🔙 بازگشت":
            if user_id in waiting_for_writing:
                waiting_for_writing.remove(user_id)

            await update.message.reply_text(
                "🌸 به منوی اصلی ترنج بازگشتی."
            )
            return

        if text == "📚 لغت‌یار":

            await update.message.reply_text(
                "📚 کلمه مورد نظر را ارسال کن.\n\nمثال:\nbeautiful"
            )
            return

        if text == "✏️ گرامر‌یار":

            await update.message.reply_text(
                "✏️ سوال گرامری خود را بپرس."
            )
            return

        if text == "📖 درس روزانه":

            reply = daily_lesson_ai()

            await update.message.reply_text(reply)

            return

        if text == "🗣️ مکالمه":

            await update.message.reply_text(
                "🗣️ وارد بخش مکالمه شدی. حالا می‌تونی آزادانه انگلیسی چت کنی!"
            )
            return

        if text == "ℹ️ راهنما":

            await update.message.reply_text(
                """
📚 لغت:
beautiful

✏️ گرامر:
گرامر: present perfect

📖 درس روزانه

🎯 تعیین سطح
"""
            )
            return

        if text.startswith("لغت:"):

            word = text.replace("لغت:", "").strip()

            reply = vocab_ai(word)

            await update.message.reply_text(reply)

            return

        if text.startswith("گرامر:"):

            question = text.replace(
                "گرامر:",
                ""
            ).strip()

            reply = grammar_ai(question)

            await update.message.reply_text(reply)

            return

        if " " not in text:

            reply = vocab_ai(text)

            await update.message.reply_text(reply)

            return

        reply = ai_conversation(text)

        await update.message.reply_text(reply)

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        await update.message.reply_text(
            f"❌ خطا:\n{str(e)}"
        )