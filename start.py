import os
import telebot
import requests
from bs4 import BeautifulSoup


BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "✅ Бот работает! Введите название товара:")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    query = message.text.strip()
    if not query:
        bot.reply_to(message, "❌ Невалидный запрос.")
        return

    result = search_allegro(query)
    if result:
        text = f"🔍 *{result['title']}*\n💰 Цена: {result['price']}\n🔗 [Смотреть на Allegro]({result['link']})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Ничего не найдено.")

    
bot.polling(none_stop=True)
def search_allegro(query):
    url = f"https://allegro.pl/listing?string={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    item = soup.select_one('div[data-box-name="Items"] article')
    if not item:
        return None

    title = item.select_one('h2') or item.select_one('h3')
    price = item.select_one('span[data-testid="price"]')
    link = item.find('a', href=True)

    return {
        "title": title.text.strip() if title else "Без названия",
        "price": price.text.strip() if price else "Нет цены",
        "link": f"https://allegro.pl{link['href']}" if link else "Нет ссылки"
    }


