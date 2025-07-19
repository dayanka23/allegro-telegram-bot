import os
import telebot
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")

bot = telebot.TeleBot(BOT_TOKEN)

def search_allegro(query):
    url = f"https://allegro.pl/listing?string={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for item in soup.select("article[data-analytics-view-custom-index]"):
        title_tag = item.select_one("h2")
        link_tag = item.select_one("a[href]")
        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag['href']
            results.append(f"🔗 <a href='{link}'>{title}</a>")
        if len(results) >= 5:
            break

    return results or ["❌ Ничего не найдено."]

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "✅ Бот работает! Введите название товара:")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    query = message.text
    bot.send_chat_action(message.chat.id, "typing")
    results = search_allegro(query)
    bot.send_message(message.chat.id, "\n\n".join(results), parse_mode="HTML")

bot.polling(none_stop=True)
