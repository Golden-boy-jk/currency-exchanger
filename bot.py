import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Список доступных валют
currencies = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}

# Команда /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        f"Привет, {message.chat.first_name}!\n"
        "Я бот для конвертации валют. Вот что я умею:\n\n"
        "1. Узнать цену валюты: отправьте сообщение в формате:\n"
        "<имя валюты> <имя валюты для перевода> <количество>\n"
        "Например: евро рубль 100\n\n"
        "2. Для списка доступных валют используйте команду /values."
    )
    bot.reply_to(message, text)

# Команда /values
@bot.message_handler(commands=['values'])
def send_values(message):
    text = 'Доступные валюты:\n' + '\n'.join(currencies.keys())
    bot.reply_to(message, text)

# Обработка текста от пользователя
@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        # Разделяем сообщение на составляющие
        values = message.text.lower().split()

        # Проверка на правильность формата
        if len(values) != 3:
            raise APIException("Неправильный формат. Используйте: <валюта> <валюта для перевода> <количество>.")

        base, quote, amount = values

        # Проверка на наличие валют в списке доступных
        if base not in currencies or quote not in currencies:
            raise APIException(
                f"Валюта {base} или {quote} недоступна. Используйте команду /values для просмотра списка валют.")

        # Получение кода валюты
        base_ticker = currencies[base]
        quote_ticker = currencies[quote]

        # Получение результата с помощью класса CurrencyConverter
        total = CurrencyConverter.get_price(quote_ticker, base_ticker, amount)
        # Округление до 4 знаков после запятой
        total = round(total, 4)
        text = f"Цена {amount} {base} в {quote}: {total} {quote}"

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.reply_to(message, text)

# Запуск бота
bot.polling()
