import ccxt
import pandas as pd
import pandas_ta as ta
import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# الإعدادات
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
BOT_RUNNING = True
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/JPY', 'GBP/JPY', 'USD/CHF']

# دالة تحليل سريعة جداً
def analyze_market(symbol):
    try:
        # استخدام Binance (محدث دائماً)
        exchange = ccxt.binance()
        bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=30) # تقليل عدد الشموع لسرعة معالجة فائقة
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        # مؤشرات دقيقة للسكالبينج (Scalping)
        df['RSI'] = ta.rsi(df['c'], length=14)
        df['EMA9'] = ta.ema(df['c'], length=9)
        df['EMA21'] = ta.ema(df['c'], length=21)
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # استراتيجية التقاطع السريع
        if prev['EMA9'] < prev['EMA21'] and last['EMA9'] > last['EMA21'] and last['RSI'] < 45:
            return "📈 إشارة شراء لحظية"
        if prev['EMA9'] > prev['EMA21'] and last['EMA9'] < last['EMA21'] and last['RSI'] > 55:
            return "📉 إشارة بيع لحظية"
        return None
    except: return None

# معالجة متوازية لجميع الأزواج
async def check_all_pairs(app):
    tasks = [asyncio.to_thread(analyze_market, pair) for pair in TRADING_PAIRS]
    results = await asyncio.gather(*tasks)
    for i, signal in enumerate(results):
        if signal:
            await app.bot.send_message(chat_id=CHAT_ID, text=f"⚡ {TRADING_PAIRS[i]}: {signal}")

async def market_loop(app):
    while True:
        if BOT_RUNNING:
            await check_all_pairs(app)
        await asyncio.sleep(20) # فحص متكرر وسريع كل 20 ثانية

async def start_bot(update, context):
    global BOT_RUNNING
    BOT_RUNNING = True
    await update.message.reply_text("🚀 نظام التحليل الفائق يعمل.")

async def stop_bot(update, context):
    global BOT_RUNNING
    BOT_RUNNING = False
    await update.message.reply_text("🛑 تم إيقاف النظام.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_bot))
    app.add_handler(CommandHandler("stop", stop_bot))
    asyncio.create_task(market_loop(app))
    app.run_polling()
