import os
import sys
from telegram.ext import Application

# جلب المتغيرات
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("خطأ: لم يتم العثور على TOKEN")
    sys.exit(1)

def main():
    # استخدام Application.builder مباشرة
    app = Application.builder().token(TOKEN).build()
    
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
