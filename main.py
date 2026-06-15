import os
import sys
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Request

def main():
    TOKEN = os.environ.get("TOKEN")
    
    if not TOKEN:
        sys.exit("TOKEN مفقود!")

    # إضافة إعدادات الطلب لزيادة وقت الاستجابة وتجنب أخطاء الاتصال
    request = Request(connect_timeout=15.0, read_timeout=15.0)
    
    app = ApplicationBuilder().token(TOKEN).request(request).build()
    
    print("البوت بدأ العمل مع إعدادات اتصال محسنة...")
    app.run_polling()

if __name__ == '__main__':
    main()
