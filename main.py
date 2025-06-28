import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Obuna tekshirish funksiyasi
def check_subscription(user_id):
    channels = ['@goldirro', '@goldirrokino']
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("1️⃣ @goldirro", url="https://t.me/goldirro"),
        telebot.types.InlineKeyboardButton("2️⃣ @goldirrokino", url="https://t.me/goldirrokino"),
        telebot.types.InlineKeyboardButton("✅ A'zo bo‘ldim", callback_data="check_subs")
    )
    bot.send_message(message.chat.id,
        "Assalom alaykum Goldirrokino ga xush kelibsiz! 🎬\n\n"
        "Botdan foydalanish uchun quyidagi kanallarga a’zo bo‘ling:",
        reply_markup=markup
    )

# Callback tugmasi uchun
@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id,
            "✅ Raxmat! Endi kinoni nomi yoki kodi orqali izlang:\nMasalan: flash yoki #201"
        )
    else:
        bot.send_message(call.message.chat.id,
            "❌ Iltimos, ikkala kanalga ham a’zo bo‘ling:\n@goldirro va @goldirrokino"
        )

# Webhook endpoint
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Flaskni ishga tushiramiz
@app.route('/')
def index():
    return 'Bot ishlayapti!'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + '/' + TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))