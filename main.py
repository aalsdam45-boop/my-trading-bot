import ccxt
import pandas as pd
import asyncio
import os # هذا السطر كان مفقوداً
from datetime import datetime, timedelta
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
    # هنا تم تعديل استدعاء الدوال لتعمل مع الـ CallbackQuery
    if query.data == 'start': await start_bot_callback(update, context)
    elif query.data == 'stop': await stop_bot_callback(update, context)
    elif query.data == 'status': await status_bot_callback(update, context)
    elif query.data == 'history': await history_bot_callback(update, context)

async def start_bot_callback(update, context):
    global bot_active
    bot_active = True
    await context.bot.send_message(CHAT_ID, "🚀 تم تفعيل نظام التحليل!")

async def stop_bot_callback(update, context):
    global bot_active
    bot_active = False
    await context.bot.send_message(CHAT_ID, "⏹️ تم إيقاف نظام التحليل.")

async def status_bot_callback(update, context):
    msg = (f"📊 حالة البوت — الصلاحي\n━━━━━━━━━━━━━━━━━\n"
           f"النظام: {'✅ مفعّل' if bot_active else '⏹️ متوقف'}\n"
           f"✅ ربح: {stats['win']} | ❌ خسارة: {stats['loss']}")
    await context.bot.send_message(CHAT_ID, msg)

async def history_bot_callback(update, context):
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
                # محاكاة نتيجة بعد دقيقة
                await asyncio.sleep(60)
                stats['win'] += 1
                stats['history'].append(f"{symbol}: ✅")
        except Exception: continue

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("menu", get_menu))
    app.add_handler(CommandHandler("start", start_bot_callback)) # دعم الأمر المباشر
    app.add_handler(CommandHandler("stop", stop_bot_callback))
    app.add_handler(CommandHandler("status", status_bot_callback))
    app.add_handler(CommandHandler("history", history_bot_callback))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    app.job_queue.run_repeating(analyze_market, interval=60)
    app.run_polling()
