import os
import ccxt
import pandas as pd
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# إعداد المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'GBP/CHF', 'EUR/AUD', 'EUR/JPY', 'USD/CAD', 'GBP/JPY', 'USD/CHF', 'USD/JPY']

# ذاكرة الحالة
bot_active = True
stats = {"win": 0, "loss": 0, "history": []}
exchange = ccxt.binance()

async def analyze_market(bot):
    """دالة المراقبة المستمرة للسوق"""
    while True:
        if bot_active:
            for symbol in TRADING_PAIRS:
                try:
                    bars = exchange.fetch_ohlcv(symbol.replace('/', ''), timeframe='1m', limit=50)
                    df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
                    df['EMA9'] = df['c'].ewm(span=9, adjust=False).mean()
                    df['EMA21'] = df['c'].ewm(span=21, adjust=False).mean()
                    
                    if df['EMA9'].iloc[-2] < df['EMA21'].iloc[-2] and df['EMA9'].iloc[-1] > df['EMA21'].iloc[-1]:
                        await bot.send_message(CHAT_ID, f"🎯 إشارة دخول — {symbol}\nشـراء   📈")
                        stats['win'] += 1
                        stats['history'].append(f"{symbol}: ✅")
                        await asyncio.sleep(10)
                except Exception: 
                    continue
        await asyncio.sleep(60)

async def get_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("▶️ تفعيل", callback_data='start'), InlineKeyboardButton("⏹️ إيقاف", callback_data='stop')],
        [InlineKeyboardButton("📊 الحالة", callback_data='status'), InlineKeyboardButton("📜 السجل", callback_data='history')]
    ]
    await update.message.reply_text("📋 القائمة الرئيسية:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    global bot_active
    if query.data == 'start': 
        bot_active = True
        await context.bot.send_message(CHAT_ID, "🚀 تم تفعيل النظام!")
    elif query.data == 'stop': 
        bot_active = False
        await context.bot.send_message(CHAT_ID, "⏹️ تم إيقاف النظام.")
    elif query.data == 'status': 
        await context.bot.send_message(CHAT_ID, f"📊 الحالة: {'✅ يعمل' if bot_active else '⏹️ متوقف'}\n✅ ربح: {stats['win']}")
    elif query.data == 'history': 
        await context.bot.send_message(CHAT_ID, "📜 آخر 10 صفقات:\n" + "\n".join(stats['history'][-10:]))

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("menu", get_menu))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # تشغيل حلقة التحليل في الخلفية
    asyncio.create_task(analyze_market(app.bot))
    
    # التشغيل المباشر
    print("البوت يعمل الآن...")
    await app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.run(run_bot())
