from telegram.ext import Application, CommandHandler
import os

# التوكن يتم جلبه من Railway Variables
TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await update.message.reply_text("البوت يعمل بنجاح!")

def main():
    # التأكد من استخدام حرف 'a' صغير
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("البوت الآن في حالة استماع...")
    app.run_polling()

if __name__ == '__main__':
    main()
