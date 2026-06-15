import os
from telegram.ext import Application, CommandHandler

# هذه الدالة هي الوحيدة التي يحتاجها البوت ليعمل
async def start(update, context):
    await update.message.reply_text("البوت يعمل بنجاح!")

def main():
    # جلب التوكن
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("خطأ: TOKEN مفقود")
        return

    # استخدام Application مباشرة بدلاً من ApplicationBuilder
    # هذا المسار هو المسار الثابت الذي لا يتغير في أي إصدار
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("البوت قيد التشغيل...")
    app.run_polling()

if __name__ == '__main__':
    main()
