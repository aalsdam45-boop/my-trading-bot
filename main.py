import os
import sys
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
# تم تغيير مكان استيراد Request ليصبح من telegram.request
from telegram.request import HTTPXRequest 
from telegram import Update

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل الآن بكامل كفاءته!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"استلمت رسالتك: {update.message.text}")

def main():
    TOKEN = os.environ.get("TOKEN")
    
    if not TOKEN:
        print("خطأ: TOKEN غير موجود!")
        sys.exit(1)

    # إعداد الطلب باستخدام HTTPXRequest بدلاً من Request العام
    req = HTTPXRequest(connect_timeout=15.0, read_timeout=15.0)
    
    # بناء البوت مع تمرير الـ Request
    app = ApplicationBuilder().token(TOKEN).request(req).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("تم التشغيل بنجاح...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
