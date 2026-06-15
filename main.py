import os
import logging
import sys
from telegram.ext import Application, CommandHandler
from telegram.error import TelegramError

# كاشف الأخطاء مفصل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def start(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    logger.info(f"أمر /start وصل من user_id={user_id}, chat_id={chat_id}")
    
    env_token = os.environ.get("TOKEN")
    env_chat_id = os.environ.get("CHAT_ID")
    
    # رسالة تشخيص
    msg = f"🔍 تقرير التشخيص:\n\n"
    msg += f"TOKEN موجود: {'✅ نعم' if env_token else '❌ لا'}\n"
    msg += f"CHAT_ID المقروء: {env_chat_id}\n"
    msg += f"Chat ID الحالي: {chat_id}\n\n"
    
    await update.message.reply_text(msg)
    
    # تجربة الإرسال
    if env_chat_id:
        try:
            logger.info(f"جاري الإرسال إلى CHAT_ID={env_chat_id}")
            await context.bot.send_message(
                chat_id=env_chat_id, 
                text="✅ البوت يعمل ويرسل رسائل للق
