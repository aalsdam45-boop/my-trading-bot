import os
import logging
from telegram.ext import Application, CommandHandler

# إعدادات بسيطة
logging.basicConfig(level=logging.INFO)

async def start(update, context):
    CHAT_ID = os.environ.get("CHAT_ID")
    if CHAT_ID:
        try:
            await context.bot.send_message(chat_id=CHAT_ID, text="البوت يعمل ويرسل!")
            await update.message.reply_text("تم الإرسال للقناة بنجاح.")
        except Exception as e:
            await update.message.reply_text(f"خطأ: {e}")
    else:
        await update.message.reply_text("يرجى إعداد CHAT_ID في المتغيرات.")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        return

    # الطريقة المباشرة للبناء (تتجنب أخطاء _applicationbuilder.py)
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
