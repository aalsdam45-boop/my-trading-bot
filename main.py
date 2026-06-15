import os
import logging
from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO)

async def start(update, context):
    chat_id = os.environ.get("CHAT_ID")
    await update.message.reply_text(f"CHAT_ID اللي قارئه البوت: {chat_id}")
    
    if chat_id:
        try:
            await context.bot.send_message(chat_id=chat_id, text="تجربة إرسال للقناة")
            await update.message.reply_text("تم الإرسال بنجاح")
        except Exception as e:
            await update.message.reply_text(f"خطأ التفاصيل: {e}")

def main():
    TOKEN = os.environ.get("TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
