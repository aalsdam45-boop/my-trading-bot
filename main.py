import os
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد السجلات (لتحليل أي خطأ يظهر في الـ Logs)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# دالة لإرسال الرسائل لأي مكان (استخدمها في مشروعك)
async def send_message_to_channel(bot: Bot, message: str):
    CHAT_ID = os.environ.get("CHAT_ID")
    if not CHAT_ID:
        print("خطأ: CHAT_ID غير موجود في المتغيرات!")
        return
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("تم الإرسال بنجاح!")
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")

# أمر /start للتأكد من الاتصال
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل! سأقوم بإرسال تجربة للقناة الآن.")
    await send_message_to_channel(context.bot, "رسالة تجريبية من البوت إلى القناة!")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("خطأ فادح: TOKEN مفقود!")
        return

    # بناء التطبيق
    app = Application.builder().token(TOKEN).build()
    
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    
    print("البوت بدأ العمل...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
