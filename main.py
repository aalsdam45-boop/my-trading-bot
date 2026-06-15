import os
import ccxt
import asyncio
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await update.message.reply_text("البوت يعمل الآن.")

def main():
    # بناء البوت بطريقة بدائية جداً لضمان عدم وجود أخطاء في الـ Builder
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("البوت بدأ في العمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
