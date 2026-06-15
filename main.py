import ccxt
import pandas as pd
import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# إعداد المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

async def market_loop(context):
    """هذه الدالة تعمل في الخلفية"""
    try:
        # مثال لمنطق التداول الخاص بك
        await context.bot.send_message(chat_id=CHAT_ID, text="🤖 البوت يعمل ويراقب السوق...")
    except Exception as e:
        print(f"Error in loop: {e}")

async def start(update, context):
    await update.message.reply_text("✅ تم تشغيل البوت بنجاح!")

if __name__ == '__main__':
    # بناء البوت
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # إضافة المهمة المتكررة للعمل في الخلفية
    job_queue = app.job_queue
    job_queue.run_repeating(market_loop, interval=60, first=10)
    
    # التشغيل
    app.run_polling()
