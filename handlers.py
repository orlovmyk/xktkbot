"""
Handlers for all commands
"""
import os
import math
import random
from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, KeyboardButton
import classes
import constants
import pyowm

USERS = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Текст доклада 📓', 'Геопозиция 🌎'],
                                        ['Оставить коментарий 😡', 'Погода️ 🌤️'],
                                        ['Исходники ℹ️', 'Случайный факт про доклад 🤔']],
                                       resize_keyboard=True)
MARK, CONTACT = range(2)


# TEXT PART
def report_text(bot, update):
    markup = ReplyKeyboardMarkup([['Слайд 1', 'Слайд 2'],
                                  ['Слайд 3', 'Слайд 4'],
                                  ['Слайд 5', 'Слайд 6'],
                                  ['Слайд 7', 'Слайд 8'],
                                  ['Главное меню']])

    update.message.reply_text('Докладчик читает с листочка)))\n'
                              'Теперь вы можете тоже 🙃',
                              reply_markup=markup)


def report(bot, update):
    text = update.message.text
    try:
        num = int(text[-1:])
    except ValueError:
        update.message.reply_text('Что-то пошло не так..')
        return
    update.message.reply_text(constants.slides[num])


# MAIN MENU
def start(bot, update):
    update.message.reply_text('Привет!\n'
                              'Я чат-бот, созданый для научной конференции\n\n'
                              'Скорее всего вы уже находитесь на ней. '
                              'Можете полазить по пунктам меню, тут много интересного. 👌',
                              reply_markup=MAIN_MENU_MARKUP)


def main_menu(bot, update):
    update.message.reply_text('Главное меню...',
                              reply_markup=MAIN_MENU_MARKUP)


# WEATHER
def weather(bot, update):
    """
    key = os.environ.get('OWM')
    owm = pyowm.OWM(key)

    observation = owm.weather_at_place('Kharkiv, ua')
    w = observation.get_weather()

    temp = w.get_temperature('celsius')
    w.get_wind()['speed']
    w.get_humidity()),
    """

    temp = {"temp_max":1.0,
            "temp_min":1.0,
            "temp":1.0,
            "humidity":80,
            "speed":4}

    update.message.reply_text("""
<b>ПОГОДА В ХАРЬКОВЕ</b>
Температура:
минимальная - {0}
средняя - {1}
максимальная - {2}

Скорость ветра: {3} м/с
Облачность: {4} %
""".format(temp['temp_min'], temp['temp'], temp['temp_max'], temp['speed'], temp['humidity']),
                              parse_mode='HTML')


# LOCATION
def location(bot, update):
    markup = ReplyKeyboardMarkup([[KeyboardButton('Мое местоположение',request_location=True)],['Главное меню']],
                                 resize_keyboard=True)
    update.message.reply_text('Координаты или жизнь!', reply_markup=markup)


def location_calculate(lt1, lng1, lt2, lng2):
    EARTH_RADIUS = 6372795

    lat1 = lt1 * math.pi / 180
    long1 = lng1 * math.pi / 180
    lat2 = lt2 * math.pi / 180
    long2 = lng2 * math.pi / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)

    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt((cl2 * sdelta)**2 + (cl1 * sl2 - sl1 * cl2 * cdelta)**2)
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * EARTH_RADIUS

    #в метрах
    return dist


def location_handler(bot, update):
    long = update.message.location.longitude
    lati = update.message.location.latitude

    lat_k = 49.9992089
    long_k = 36.2429473

    res = location_calculate(lati, long, lat_k, long_k)

    update.message.reply_text('До <b>ХКТК</b> {} км'.format(round(res / 1000, 2)), parse_mode='HTML')


# SOURCE
def source(bot, update):
    update.message.reply_text('ОТКРЫТРЫЙ ИСХОДНЫЙ КОД!!!11!\n'
                              'ЭТО ЖЕ ПРЯМ <b>GNU</b> !!11!\n'
                              'https://github.com/orlovw/xktkbot',
                              reply_markup=MAIN_MENU_MARKUP,
                              parse_mode='HTML')


# PHOTO PART
def photo(bot, update):
    photo_id = update.message.photo[-1].file_id
    update.message.reply_text(photo_id, quote=True)


def photo_send(bot, update):
    update.message.reply_photo(photo=random.choice(constants.photos))



# RANDOM_FACT
def random_fact(bot, update):
    answer = random.choice(constants.facts)
    update.message.reply_text(answer)


# COMMENTS PART
def comment(bot, update):
    user = update.message.from_user
    new_user = classes.User(username=user.username, first_name=user.first_name, last_name=user.last_name)
    chat_id = update.message.chat_id
    USERS.update({chat_id: new_user})

    markup=ReplyKeyboardMarkup([['/cancel']], resize_keyboard=True)
    update.message.reply_text('Вижу вы решили оставить <b>ГНЕВНЫЙ</b> комментарий?\n'
                              'Окей, я только за!\n\nМожете писать, все что хотите!\n'
                              'Доставку беру на себя)\n'
                              'Используйте /cancel для отмены',
                              quote=True, parse_mode='HTML', reply_markup=markup)
    return MARK


def mark(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    user = USERS.get(chat_id)
    user.add_comment(text)
    update.message.reply_text('Наверное там что-то интересное, жаль я не умею читать 😢\n\n'
                              'Сколько б вы поставили докладу по 12-бальной системе?\n',
                              quote=True)
    return CONTACT


def contact(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        text = int(text)
    except ValueError:
        update.message.reply_text('Оценка должна быть числом (ну к примеру 1)\n'
                                  'Арабскими цифрами слево направо (дискретная система исчелсления,'
                                  ' можно дробное число(это не баг а фича!))')
        return CONTACT

    if text > 12:
        update.message.reply_text('А у вас число больше 12, в курсе?)')
        return CONTACT

    if text < 0:
        update.message.reply_text('А у вас число отрицательное, в курсе?)')
        return CONTACT

    user = USERS.get(chat_id)
    user.add_mark(text)
    #239062390 - @orlow
    bot.sendMessage(chat_id='239062390', text=user.show())
    update.message.reply_text('Я отправил коментарий и оценку докладчику\n'
                              'Спасибо за заполнение <i>долгой и нудной</i> формы\n',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP,
                              parse_mode='HTML')
    return ConversationHandler.END


def cancel(bot, update):
    chat_id = update.message.chat_id
    USERS.pop(chat_id, None)
    update.message.reply_text('Окей, отменяю',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END




conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Оставить коментарий 😡', comment)],

        fallbacks=[CommandHandler('cancel', cancel)],

        states={
            MARK: [MessageHandler(Filters.text, mark)],

            CONTACT: [MessageHandler(Filters.text, contact)]

        })

bot_handlers = [CommandHandler('start', start),
                RegexHandler('Исходники ℹ️', source),
                RegexHandler('Текст доклада 📓', report_text),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Случайный факт про доклад 🤔', random_fact),
                RegexHandler('Геопозиция 🌎', location),
                RegexHandler('Погода️ 🌤️', weather),
                RegexHandler('Слайд [1-8]', report),
                RegexHandler('Случайная картинка', photo_send),

                MessageHandler(Filters.location, location_handler),
                MessageHandler(Filters.photo, photo),
                conv_handler]