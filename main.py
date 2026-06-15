import ccxt
import pandas as pd
import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# استخدام os.environ لجلب المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
BOT_RUNNING = True

async def market_loop(app):
    while True:
        if BOT_RUNNING:
            # هنا يمكنك وضع منطق التداول الخاص بك
            # مثال لإرسال رسالة تجريبية للتأكد من العمل
            try:
                await app.bot.send_message(chat_id=CHAT_ID, text="🤖 البوت يعمل الآن بشكل سليم!")
                await asyncio.sleep(600) # يرسل رسالة كل 10 دقائق
            except Exception as e:
                print(f"Error: {e}")
        await asyncio.sleep(60)

async def start_bot(update, context):
    await update.message.reply_text("🚀 البوت مفعل!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_bot))
    
    # الحل الجذري للـ Loop
    loop = asyncio.get_event_loop()
    loop.create_task(market_loop(app))
    
    app.run_polling()
