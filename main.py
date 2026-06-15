import os
import sys
from telegram.ext import Application

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("خطأ: TOKEN غير موجود")
    sys.exit(1)

def main():
    # البناء بأبسط صورة ممكنة
    app = Application.builder().token(TOKEN).build()
    
    print("البوت بدأ العمل بنجاح...")
    # التشغيل المباشر
    app.run_polling()

if __name__ == '__main__':
    main()
