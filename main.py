import os
import asyncio
from telethon import TelegramClient, events, Button
from datetime import datetime, timedelta

# Load config from environment variables
API_ID=28013497
API_HASH=3bd0587beedb80c8336bdea42fc67e27
BOT_TOKEN=7619774036:AAH9PLMNaw5Vjc7ujp8EPKq9P47KXl2gXNY

# Configuration
target_group = os.getenv("TARGET_GROUP", "auto_reply_Gr")
facebook_page = os.getenv("FACEBOOK_PAGE", "https://www.facebook.com/share/1FaBZ3ZCWW/?mibextid=wwXIfr")
telegram_channel = os.getenv("TELEGRAM_CHANNEL", "https://t.me/vanna_sovanna")

admins_env = os.getenv("ADMINS", "vanna_sovanna,rachana0308,admin3")
admins = [a.strip().lower() for a in admins_env.split(",")]

bot = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

chat_language = {}
user_last_reply = {}

menu_text = {
    'km': "សួស្តីបងៗ! ​យើងខ្ញុំនិងតបសារឆាប់ៗនេះ សូមអធ្យាស្រ័យចំពោះការឆ្លើយតបយឺតយ៉ាវ។ សូមអរគុណ 💙🙏៖",
    'en': "Hello everyone! I will reply shortly. Sorry for the delayed response. Thank you 💙🙏",
    'zh': "大家好！我会很快回复。抱歉回复得晚了。谢谢💙🙏"
}

def get_group_buttons():
    return [[
        Button.url("📘 Facebook Page", facebook_page),
        Button.url("📢 Telegram Admin", telegram_channel)
    ]]

def detect_language_by_text(text: str) -> str:
    for ch in text:
        if '\u1780' <= ch <= '\u17FF':
            return 'km'
        elif '\u4E00' <= ch <= '\u9FFF':
            return 'zh'
        elif ('a' <= ch.lower() <= 'z'):
            return 'en'
    return 'km'

@bot.on(events.NewMessage)
async def handle_group_message(event):
    chat = await event.get_chat()
    if not event.is_group or getattr(chat, 'username', '') != target_group:
        return

    sender = await event.get_sender()
    if sender is None:
        return  # 🛑 Anonymous admin or unknown sender

    user_id = sender.id
    username = (sender.username or "").lower()

    if username in admins:
        return  # don't reply to admins

    now = datetime.utcnow()
    key = (event.chat_id, user_id)

    last_reply_time = user_last_reply.get(key)
    if last_reply_time and now - last_reply_time < timedelta(hours=24):
        return  # already replied within 24h

    message_text = event.raw_text or ""
    lang = detect_language_by_text(message_text)
    chat_language[event.chat_id] = lang

    await event.reply(menu_text.get(lang, menu_text['en']),
                      buttons=get_group_buttons(),
                      parse_mode='md')

    user_last_reply[key] = now

print("🤖 Bot is running...")
bot.run_until_disconnected()
