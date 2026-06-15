import os
import sys
from telegram.ext import ApplicationBuilder, CommandHandler

# جلب المتغيرات مع التحقق
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# التحقق من وجود المتغيرات
if not TOKEN:
    print("خطأ: المتغير TOKEN غير موجود في Railway Variables!")
    sys.exit(1)

async def start(update, context):
    await update.message.reply_text("البوت يعمل!")

def main():
    # بناء البوت
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        print("البوت يعمل الآن بنجاح...")
        app.run_polling()
    except Exception as e:
        print(f"حدث خطأ أثناء التشغيل: {e}")

if __name__ == '__main__':
    main()
