import ccxt
import pandas as pd
import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

async def start(update, context):
    await update.message.reply_text("✅ البوت يعمل الآن!")

async def post_init(application):
    """هذه الدالة تعمل مرة واحدة عند تشغيل البوت"""
    await application.bot.send_message(chat_id=CHAT_ID, text="🤖 البوت متصل وجاهز للعمل!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    
    # التشغيل المباشر دون الحاجة لـ loop خارجي (هذا هو الحل للخطأ)
    app.run_polling()
