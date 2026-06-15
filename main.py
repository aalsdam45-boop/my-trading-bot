import os
import sys
from telegram.ext import ApplicationBuilder
from telegram import Request

def main():
    TOKEN = os.environ.get("TOKEN")
    
    if not TOKEN:
        print("خطأ: التوكن غير موجود في المتغيرات")
        sys.exit(1)

    # إعدادات الاتصال لتجنب أخطاء الشبكة
    req = Request(connect_timeout=15.0, read_timeout=15.0)
    
    # بناء البوت
    app = ApplicationBuilder().token(TOKEN).request(req).build()
    
    print("البوت بدأ العمل بنجاح...")
    
    # تشغيل البوت مع تنظيف أي أوامر عالقة (حل مشكلة 409 Conflict)
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
