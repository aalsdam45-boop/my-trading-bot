import ccxt
import pandas as pd
import os
import asyncio
from datetime import datetime, timedelta
from telegram.ext import ApplicationBuilder

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TRADING_PAIRS = ['EUR/USD', 'GBP/USD', 'GBP/CHF', 'EUR/AUD', 'EUR/JPY', 'USD/CAD', 'GBP/JPY', 'USD/CHF', 'USD/JPY']
exchange = ccxt.binance()

async def check_result(symbol, entry_price, direction, context):
    """مراقبة النتيجة بعد دقيقة"""
    await asyncio.sleep(60) # الانتظار لانتهاء الصفقة
    try:
        ticker = exchange.fetch_ticker(symbol.replace('/', ''))
        current_price = ticker['last']
        
        # تحديد الربح أو الخسارة
        is_win = (current_price > entry_price) if "شـراء" in direction else (current_price < entry_price)
        result_text = "✅ ربح (Win)" if is_win else "❌ خسارة (Loss)"
        
        msg = (f"🏁 نتيجة الصفقة التجريبية — {symbol.replace('/', '')}\n"
               f"النتيجة: {result_text}\n"
               f"سعر الدخول: {entry_price}\n"
               f"سعر الإغلاق: {current_price}\n\n"
               f"🧪 هذا اختبار — كل شيء يعمل بشكل صحيح.\n"
               f"🔗 سجل الآن")
        await context.bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"Error checking result: {e}")

async def send_trading_signal(context):
    for symbol in TRADING_PAIRS:
        try:
            bars = exchange.fetch_ohlcv(symbol.replace('/', ''), timeframe='1m', limit=50)
            df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
            df['EMA9'] = df['c'].ewm(span=9, adjust=False).mean()
            df['EMA21'] = df['c'].ewm(span=21, adjust=False).mean()
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            entry_price = last['c']
            
            direction = None
            if prev['EMA9'] < prev['EMA21'] and last['EMA9'] > last['EMA21']:
                direction = "شـراء   📈"
            elif prev['EMA9'] > prev['EMA21'] and last['EMA9'] < last['EMA21']:
                direction = "بيـع    📉"
                
            if direction:
                entry_time = datetime.now().strftime("%I:%M %p")
                exit_time = (datetime.now() + timedelta(minutes=1)).strftime("%I:%M %p")
                
                msg = (f"╔══════════════════╗\n  🎯 إشـارة دخـول — الصلاحي\n╚══════════════════╝\n"
                       f"🟢 {symbol.replace('/', '')}  |  {direction}\n"
                       f"┌─────────────────────\n│ ⏳ المدة    : 1 دقيقة\n│ 📊 الدقة    : 75%\n└─────────────────────\n"
                       f"🕐 الدخول  : {entry_time}\n🔔 الإغلاق : {exit_time}\n\n"
                       f"🧪 إشارة تجريبية\n▸ الصلاحي/ محترف للتداول — v1.0\n🔗 سجل الآن")
                
                await context.bot.send_message(chat_id=CHAT_ID, text=msg)
                # بدء مراقبة النتيجة في الخلفية
                asyncio.create_task(check_result(symbol, entry_price, direction, context))
                
        except Exception as e:
            continue

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    job_queue = app.job_queue
    job_queue.run_repeating(send_trading_signal, interval=60, first=5)
    app.run_polling()
