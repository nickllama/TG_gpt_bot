import telebot
import openai
import os
from telebot import types
from dotenv import load_dotenv

load_dotenv()

# Загрузка переменных окружения
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if TELEGRAM_API_KEY:
    print(f"Значение переменной окружения TELEGRAM_API_KEY: {TELEGRAM_API_KEY}")
else:
    print("Переменная окружения TELEGRAM_API_KEY не установлена.")

if OPENAI_API_KEY:
    print(f"Значение переменной окружения OPENAI_API_KEY: {OPENAI_API_KEY}")
else:
    print("Переменная окружения OPENAI_API_KEY не установлена.")

bot = telebot.TeleBot(TELEGRAM_API_KEY)
openai.api_key = OPENAI_API_KEY

name = ''
surname = ''
age = 0

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    try:
        age = int(message.text)
        question = f'Тебе {age} лет, тебя зовут {name} {surname}?\nДа или Нет?'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup.add(item_yes, item_no)
        bot.send_message(message.from_user.id, text=question, reply_markup=markup)
        bot.register_next_step_handler(message, check_confirmation)
    except Exception:
        bot.send_message(message.from_user.id, 'Введите ваш возраст цифрами, пожалуйста')

def check_confirmation(message):
    if message.text.lower() == 'да':
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Меня зовут {name} {surname} и мне {age} лет.",
            max_tokens=3500
        )
        bot.send_message(message.from_user.id, response.choices[0].text)
    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, 'Хорошо, начнем сначала.')
        start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)