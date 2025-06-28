import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Tokenni ENV (muhit o'zgaruvchisi) dan olamiz
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

# Kanalga obuna bo‘lganini tekshirish
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

    # Tugmalar
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("1️⃣ @goldirro", url="https://t.me/goldirro")
    btn2 = InlineKeyboardButton("2️⃣ @goldirrokino", url="https://t.me/goldirrokino")
    btn3 = InlineKeyboardButton("✅ A'zo bo‘ldim", callback_data="check_subs")
    markup.add(btn1, btn2, btn3)

    text = (
        "Assalom alaykum Goldirrokino ga xush kelibsiz! 🎬\n\n"
        "Botdan foydalanish uchun quyidagi kanallarga a’zo bo‘ling:"
    )
    bot.send_message(chat_id, text, reply_markup=markup)

# "A'zo bo‘ldim" tugmasi
@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subscriptions(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.send_message(call.message.chat.id,
            "✅ Raxmat! Endi kinolarni nomi yoki kodi orqali izlang:\n\n"
            "🎬 Masalan: flash yoki #201"
        )
    else:
        bot.send_message(call.message.chat.id,
            "❌ Iltimos, ikkala kanalga ham a'zo bo‘ling:\n@goldirro va @goldirrokino"
        )

# Botni ishga tushiramiz
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    bot.polling(none_stop=True)