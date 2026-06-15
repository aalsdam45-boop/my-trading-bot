async def start(update, context):
    CHAT_ID = os.environ.get("CHAT_ID")
    try:
        await context.bot.send_message(chat_id=CHAT_ID, text="اختبار إرسال...")
        await update.message.reply_text("تمت محاولة الإرسال!")
    except Exception as e:
        # هذا السطر سيطبع سبب الخطأ في الـ Logs (مثلاً: Bot not in channel)
        print(f"حدث خطأ أثناء الإرسال: {e}")
        await update.message.reply_text(f"فشل الإرسال: {e}")
