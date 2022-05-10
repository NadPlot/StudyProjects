from config import keys, TOKEN
from extensions import MyException, Convert
import telebot

bot = telebot.TeleBot(TOKEN)


# приветствие, ответ на /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добрый день, {message.chat.username}")
    text = '''Чтобы начать работу введите (через пробел):
<название валюты> <в какую валюту перевести> <количество первой валюты>'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message):
    text = '''Доступные команды:
/start - вернет вас к началу,
/values - покажет список валют доступных для конвертации.
Формат ввода команды (через пробел):
<название валюты> <в какую валюту перевести> <количество первой валюты>'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise MyException('Неверный формат ввода команды. /help')

        base, quote, amount = values
        price = Convert().get_price(base, quote, amount)
    except MyException as e:
        bot.reply_to(message, f'Ошибка:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {base} - {price} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)