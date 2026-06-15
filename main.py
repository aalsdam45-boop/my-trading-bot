import ccxt
import pandas as pd
import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# الإعدادات (تأخذ القيم من Render Environment Variables)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
BOT_RUNNING = True
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/JPY', 'GBP/JPY', 'USD/CHF']

# الدالة المحدثة التي تحسب المؤشرات يدوياً (لضمان عمل البوت بدون أخطاء)
def analyze_market(symbol):
    try:
        exchange = ccxt.binance()
        bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=50)
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        # حساب RSI يدوياً
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # حساب EMA يدوياً
        df['EMA9'] = df['c'].ewm(span=9, adjust=False).mean()
        df['EMA21'] = df['c'].ewm(span=21, adjust=False).mean()
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # استراتيجية الإشارات
        if prev['EMA9'] < prev['EMA21'] and last['EMA9'] > last['EMA21'] and last['RSI'] < 45:
            return "📈 إشارة شراء قوية"
        if prev['EMA9'] > prev['EMA21'] and last['EMA9'] < last['EMA21'] and last['RSI'] > 55:
            return "📉 إشارة بيع قوية"
        return None
    except: 
        return None

# دالة فحص الأزواج
async def check_all_pairs(app):
    for pair in TRADING_PAIRS:
        signal = analyze_market(pair)
        if signal:
            await app.bot.send_message(chat_id=CHAT_ID, text=f"⚡ {pair}: {signal}")
            await asyncio.sleep(2)

async def market_loop(app):
    while True:
        if BOT_RUNNING:
            await check_all_pairs(app)
        await asyncio.sleep(20)

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
