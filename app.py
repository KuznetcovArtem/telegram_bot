import telebot

from config import *
from extensions import Converter, ApiException
from telebot import types

def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))

    markup.add(*buttons)
    return markup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n <Имя валюты> <В какую валюту перевести> \
    <Количество переводимой валюты>\nУвидеть список доступных валют: /values\nПриступить к конвертации: /convert"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту которую необходимо конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту в которую необходимо конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Введите сумму для валюты которую необходимо конвертировать: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        total_base = Converter.get_price(quote, base, amount)
    except ApiException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n {e}')
    else:
        bot.send_message(message.chat.id, total_base)

bot.polling(none_stop=True)