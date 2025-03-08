
import telebot
import requests
from config import TOKEN
from crypto_parser import get_crypto_data

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения новостей
def get_crypto_news():
    try:
        url = "https://newsapi.org/v2/everything?q=crypto&apiKey=d9ce5375-bc45-4c3b-a5fa-5ecf5dd7a5f6"
        response = requests.get(url)
        data = response.json()

        if "articles" in data:
            articles = data["articles"][:5]  # Берем 5 новостей
            news_text = ""
            for article in articles:
                news_text += f"🔹 {article['title']}\n{article['url']}\n\n"
            return news_text
        return "Не удалось получить новости."
    except Exception as e:
        return "Произошла ошибка при получении новостей."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я бот, который присылает новости и информацию о криптовалюте. \n\n"
                         "Используй эти команды:\n"
                         "/news - получить свежие новости\n"
                         "/crypto - получить информацию о криптовалютах")

# Обработчик команды /news
@bot.message_handler(commands=['news'])
def send_news(message):
    bot.reply_to(message, "Собираю новости...")
    news = get_crypto_news()
    bot.send_message(message.chat.id, news)

# Обработчик команды /crypto
@bot.message_handler(commands=['crypto'])
def send_crypto_data(message):
    bot.reply_to(message, "Собираю данные о криптовалютах...")
    # try:
    crypto_data = get_crypto_data()
    if crypto_data:
        # Отправка данных частями, чтобы не превышать лимит сообщения
        chunks = [crypto_data[i:i+4000] for i in range(0, len(crypto_data), 4000)]
        for chunk in chunks:
            bot.send_message(message.chat.id, chunk)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о криптовалютах.")
    # except Exception as e:
    #     bot.send_message(message.chat.id, "Произошла ошибка при получении данных о криптовалютах.")

# Запуск бота
bot.infinity_polling()
