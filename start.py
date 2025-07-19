import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "✅ Бот работает! Введите название товара:")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    bot.reply_to(message, f"🔍 Ищу товар: {message.text}... (функция пока заглушка)")

bot.polling(none_stop=True)
