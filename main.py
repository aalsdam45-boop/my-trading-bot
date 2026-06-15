from telegram.ext import Application, CommandHandler
TOKEN = "8833295411:AAGzMSwJr70Gy6wwZflOHWUi50wTmmg4EXI"
async def start(update, context):
    await update.message.reply_text("البوت يعمل بنجاح!")
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("البوت بدأ العمل...")
    app.run_polling()
if __name__ == '__main__':
    main()
