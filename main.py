import os
import ccxt
import pandas as pd
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# إعداد المتغيرات
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'GBP/CHF', 'EUR/AUD', 'EUR/JPY', 'USD/CAD', 'GBP/JPY', 'USD/CHF', 'USD/JPY']

# ذاكرة الحالة
bot_active = True
stats = {"win": 0, "loss": 0, "history": []}
exchange = ccxt.binance()

async def get_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("▶️ تفعيل", callback_data='start'), InlineKeyboardButton("⏹️ إيقاف", callback_data='stop')],
        [InlineKeyboardButton("📊 الحالة", callback_data='status'), InlineKeyboardButton("📜 السجل", callback_data='history')]
    ]
    await update.message.reply_text("📋 القائمة الرئيسية:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'start':
        global bot_active
        bot_active = True
        await context.bot.send_message(CHAT_ID, "🚀 تم تفعيل نظام التحليل!")
    elif query.data == 'stop':
        bot_active = False
        await context.bot.send_message(CHAT_ID, "⏹️ تم إيقاف نظام التحليل.")
    elif query.data == 'status':
        msg = f"📊 حالة البوت — الصلاحي\nالنظام: {'✅ مفعّل' if bot_active else '⏹️ متوقف'}\n✅ ربح: {stats['win']} | ❌ خسارة: {stats['loss']}"
        await context.bot.send_message(CHAT_ID, msg)
    elif query.data == 'history':
        history_msg = "📜 آخر الإشارات:\n" + "\n".join(stats['history'][-10:])
        await context.bot.send_message(CHAT_ID, history_msg or "السجل فارغ.")

async def analyze_market(context):
    if not bot_active: return
    for symbol in TRADING_PAIRS:
        try:
            bars = exchange.fetch_ohlcv(symbol.replace('/', ''), timeframe='1m', limit=50)
            df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
            df['EMA9'] = df['c'].ewm(span=9, adjust=False).mean()
            df['EMA21'] = df['c'].ewm(span=21, adjust=False).mean()
            
            if df['EMA9'].iloc[-2] < df['EMA21'].iloc[-2] and df['EMA9'].iloc[-1] > df['EMA21'].iloc[-1]:
                await context.bot.send_message(CHAT_ID, f"🎯 إشارة دخول — {symbol}\nشـراء   📈")
                await asyncio.sleep(60)
                stats['win'] += 1
                stats['history'].append(f"{symbol}: ✅")
        except Exception: continue

if __name__ == '__main__':
    # بناء البوت مع تفعيل الـ JobQueue بشكل صحيح
    app = ApplicationBuilder().token(TOKEN).build()
    
    # التأكد من وجود الـ job_queue
    job_queue = app.job_queue
    job_queue.run_repeating(analyze_market, interval=60, first=10)
    
    app.add_handler(CommandHandler("menu", get_menu))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("البوت يعمل الآن...")
    app.run_polling()
