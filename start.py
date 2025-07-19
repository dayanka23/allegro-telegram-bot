import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")

bot = telebot.TeleBot(BOT_TOKEN)

def search_allegro(query):
    url = f"https://allegro.pl/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    payload = {
        "operationName": "searchProducts",
        "variables": {
            "searchPhrase": query,
            "first": 5
        },
        "query": """
        query searchProducts($searchPhrase: String!, $first: Int!) {
            search {
                products(searchPhrase: $searchPhrase, first: $first) {
                    edges {
                        node {
                            name
                            url
                        }
                    }
                }
            }
        }
        """
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    results = []
    for item in data["data"]["search"]["products"]["edges"]:
        name = item["node"]["name"]
        link = item["node"]["url"]
        results.append(f"🔗 <a href='{link}'>{name}</a>")

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
