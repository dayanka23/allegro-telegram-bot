
import os
import telebot
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    query = message.text.strip()
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ищу товар: " + query)

    try:
        allegro_url = "https://allegro.pl/listing?string=" + query.replace(" ", "+")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(allegro_url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')
        item = soup.select_one('div[data-box-name="items-v3"] article')

        if not item:
            bot.send_message(chat_id, "Ничего не найдено на Allegro.")
            return

        title_tag = item.select_one('h2')
        title = title_tag.text.strip() if title_tag else "Без названия"

        price_tag = item.select_one('div._9c44d_1zemI span')
        price = price_tag.text.strip() if price_tag else "Без цены"

        link_tag = item.select_one('a')
        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else allegro_url

        result = "Allegro результат:\nНазвание: " + title + "\nЦена: " + price + "\nСсылка: " + link
        print("Ответ пользователю:\n" + result)
        bot.send_message(chat_id, result)

    except Exception as e:
        bot.send_message(chat_id, "Ошибка при поиске: " + str(e))

bot.polling()
