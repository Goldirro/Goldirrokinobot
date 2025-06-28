import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")  # TOKEN .env dan olinadi
bot = telebot.TeleBot(TOKEN)

# Obuna tekshiruvi
def check_subscription(user_id):
    channels = ['@goldirro', '@goldirrokino']
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Xatolik: {channel} → {e}")
            return False
    return True

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("1️⃣ @goldirro", url="https://t.me/goldirro"),
        InlineKeyboardButton("2️⃣ @goldirrokino", url="https://t.me/goldirrokino"),
        InlineKeyboardButton("✅ A'zo bo‘ldim", callback_data="check_subs")
    )
    bot.send_message(chat_id,
        "Assalom alaykum Goldirrokino ga xush kelibsiz! 🎬\n\n"
        "Botdan foydalanish uchun quyidagi kanallarga a’zo bo‘ling:",
        reply_markup=markup
    )

# Obuna tekshiruvi
@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs_handler(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id,
            "✅ Raxmat! Endi kinolarni nomi yoki kodi orqali izlang:\n\n"
            "🎬 Masalan: flash yoki #201"
        )
    else:
        bot.send_message(call.message.chat.id,
            "❌ Iltimos, ikkala kanalga ham a'zo bo‘ling:\n@goldirro va @goldirrokino"
        )

# Botni ishga tushirish
print("🤖 Bot ishga tushdi...")
bot.polling(none_stop=True)