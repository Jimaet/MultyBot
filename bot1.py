import time
import feedparser
import telebot
from threading import Timer

# Укажите ваш токен бота
TOKEN = ''
# Укажите ID вашей группы
CHAT_ID = -1002177082543  # Измените на ваш ID группы
# Укажите список URL ваших RSS-лент
RSS_URLS = [
    'https://habr.com/ru/rss/articles/?fl=ru',
    'https://3dnews.ru/news/rss/',
    # Добавьте больше RSS-лент по мере необходимости
]

# Словарь для хранения ссылок на последние отправленные статьи для каждой ленты
last_link = {}

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот запущен!')
    print(f"Chat ID: {message.chat.id}")  # Печатает ID чата в консоль

def check_rss():
    global last_link
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        if feed.entries:
            latest_entry = feed.entries[0]  # Последняя запись
            if url not in last_link or last_link[url] != latest_entry.link:
                try:
                    bot.send_message(CHAT_ID, f"{latest_entry.title}\n{latest_entry.link}")
                    last_link[url] = latest_entry.link
                except telebot.apihelper.ApiTelegramException as e:
                    if e.error_code == 429:
                        retry_after = int(e.result_json['parameters']['retry_after'])
                        print(f"Too many requests, retrying after {retry_after} seconds")
                        time.sleep(retry_after)
                    else:
                        raise e
    Timer(60, check_rss).start()  # Проверять каждые 10 минут

if __name__ == '__main__':
    check_rss()  # Запуск проверки RSS-лент
    bot.polling(none_stop=True, timeout=60)
