import os
from telegram.ext import ApplicationBuilder, CommandHandler

# قراءة المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

async def start(update, context):
    # مثال: إرسال رسالة للقناة باستخدام المعرف
    await context.bot.send_message(chat_id=CHAT_ID, text="البوت متصل بالقناة ويعمل بنجاح!")
    await update.message.reply_text("تم إرسال رسالة تجريبية للقناة.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("البوت يعمل الآن...")
    app.run_polling()
