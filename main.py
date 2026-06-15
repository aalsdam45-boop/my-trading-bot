import ccxt
import pandas as pd
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# إعداد المتغيرات
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'GBP/CHF', 'EUR/AUD', 'EUR/JPY', 'USD/CAD', 'GBP/JPY', 'USD/CHF', 'USD/JPY']

def calculate_indicators(df):
    delta = df['c'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['EMA9'] = df['c'].ewm(span=9, adjust=False).mean()
    df['EMA21'] = df['c'].ewm(span=21, adjust=False).mean()
    return df

async def send_status(context):
    """إرسال رسالة الحالة التي طلبتها"""
    pairs_text = "\n".join([f"  • {pair}" for pair in TRADING_PAIRS])
    msg = f"📊 حالة البوت — الصلاحي\n━━━━━━━━━━━━━━━━━\nالنظام  : ✅ مفعّل\nالسوق   : مفتوح 🟢\nالأزواج النشطة:\n{pairs_text}\n━━━━━━━━━━━━━━━━━\n📈 إجمالي الإشارات : تحت المراقبة"
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

async def analyze_and_notify(context):
    exchange = ccxt.binance()
    for symbol in TRADING_PAIRS:
        try:
            # تم التغيير لـ 15 دقيقة لزيادة الإشارات
            bars = exchange.fetch_ohlcv(symbol.replace('/', ''), timeframe='15m', limit=50)
            df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
            df = calculate_indicators(df)
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            if prev['EMA9'] < prev['EMA21'] and last['EMA9'] > last['EMA21'] and last['RSI'] < 45:
                await context.bot.send_message(chat_id=CHAT_ID, text=f"📈 إشارة شراء قوية: {symbol}\nالسعر: {last['c']}")
            elif prev['EMA9'] > prev['EMA21'] and last['EMA9'] < last['EMA21'] and last['RSI'] > 55:
                await context.bot.send_message(chat_id=CHAT_ID, text=f"📉 إشارة بيع قوية: {symbol}\nالسعر: {last['c']}")
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", send_status))
    
    # جدولة التحليل كل 15 دقيقة
    job_queue = app.job_queue
    job_queue.run_repeating(analyze_and_notify, interval=900, first=5)
    
    app.run_polling()
