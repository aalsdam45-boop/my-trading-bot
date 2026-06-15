import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# إعداد السجلات (Logs) لمعرفة ما يحدث داخل البوت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
    await update.message.reply_text("البوت يعمل بشكل ممتاز ومستقر!")

if __name__ == '__main__':
    # جلب التوكن من المتغيرات (Variables) في Railway
    TOKEN = os.environ.get("TOKEN")
    
    # بناء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    
    print("تم تشغيل البوت بنجاح...")
    # التشغيل باستخدام Polling
    app.run_polling()
