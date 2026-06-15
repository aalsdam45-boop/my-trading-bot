from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أنا أعمل!")

if __name__ == '__main__':
    # تأكد أنك وضعت TOKEN في المتغيرات
    TOKEN = os.environ.get("TOKEN")
    
    # بناء التطبيق بأبسط طريقة ممكنة
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("البوت جاهز...")
    app.run_polling()
