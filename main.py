import os
from telegram.ext import Application, CommandHandler

# استخدام التوكن من المتغيرات
TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await update.message.reply_text("البوت يعمل بنجاح!")

if __name__ == '__main__':
    # بناء التطبيق بالطريقة التقليدية
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("البوت في حالة استماع...")
    app.run_polling()
