import telebot
import requests
import random
from bs4 import BeautifulSoup

TOKEN = '5966751899:AAEl9kN2oCOs7ma1Hq4QRKTeCiWZWLAnKfA'
bot = telebot.TeleBot(TOKEN)

# BUTTONS
markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
item1 = telebot.types.KeyboardButton('🗞️ Новости')
item2 = telebot.types.KeyboardButton('Мой ID')
item3 = telebot.types.KeyboardButton('📍 Получить свои координаты', request_location=True)
item4 = telebot.types.KeyboardButton('Мой IP')
item5 = telebot.types.KeyboardButton('🎲 Бросок кубика')
item6 = telebot.types.KeyboardButton('🔢 Случайное число')
markup.add(item1, item2, item3, item4, item5, item6)

# START
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgEAAxkBAAEHAmpjqYoKp4ooL-3dVFpXTCS58qAKJAACDwEAAjgOghG1zE1_4hSRgiwE')
    mess = f'Приветствую, <b>{message.from_user.first_name}</b>! Вот, что я умею:'
    bot.reply_to(message, mess, parse_mode='html', reply_markup=markup)

# PARSER, ID, IP, LOCATION, RANDOM
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == 'Мой ID':
        bot.send_message(message.chat.id, f"Ваш 🆔: {message.from_user.id}", reply_markup=markup)
    elif message.text == '🗞️ Новости':
        soup = BeautifulSoup(requests.get('https://rbc.ru/').text, 'html.parser')
        news = soup.find_all('span', {'class': 'news-feed__item__title'})
        news_list = []
        for n in news:
            news_list.append(n.text.strip())
        if news_list:
            bot.send_message(message.chat.id, '\n'.join('\n\r'+line.strip() for line in news_list), reply_markup=markup)
    elif message.text == '📍 Получить свои координаты':
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Получить свои координаты", request_location=True)
        keyboard.add(button)
        bot.send_message(message.chat.id, "Нажмите на кнопку '📍 Получить свои координаты' и поделитесь своей локацией", reply_markup=keyboard)
    elif message.text == 'Мой IP':
        response = requests.get('https://api.ipify.org')
        ip = response.text
        bot.send_message(message.chat.id, f"Ваш IP-адрес: {ip}", reply_markup=markup)
    elif message.text == '🎲 Бросок кубика':
        number = random.randint(1, 6)
        bot.reply_to(message, f"Результат броска кубика: {number}", reply_markup=markup)
    elif message.text == '🔢 Случайное число':
        number = random.randint(1, 100)
        bot.reply_to(message, f"Случайное число: {number}", reply_markup=markup)


# LOCATION FUNC
@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    bot.send_message(message.chat.id, f"Ваши координаты: ({latitude}, {longitude})", reply_markup=markup)

bot.polling()
