import os
import ccxt
import pandas as pd
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# إعداد المتغيرات
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'GBP/CHF', 'EUR/AUD', 'EUR/JPY', 'USD/CAD', 'GBP/JPY', 'USD/CHF', 'USD/JPY']

bot_active = True
stats = {"win": 0, "loss": 0, "history": []}
exchange = ccxt.binance()

async def analyze_market(bot):
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
                        await asyncio.sleep(60)
                except Exception: continue
        await asyncio.sleep(60)

async def get_menu(update, context):
    await update.message.reply_text("📋 البوت يعمل. استخدم الأزرار للتحكم.")

async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    global bot_active
    if query.data == 'start': bot_active = True
    elif query.data == 'stop': bot_active = False

if __name__ == '__main__':
    # بناء البوت بشكل مبسط جداً لتفادي أي خطأ في الـ build
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("menu", get_menu))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # تشغيل المهمة
    asyncio.create_task(analyze_market(app.bot))
    
    app.run_polling()
