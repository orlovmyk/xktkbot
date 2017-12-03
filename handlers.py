"""
Handlers for all commands
"""
import random
from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup
import classes


SKETCHES = classes.Sketches()
SKETCHES.load()
USERS = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Запись на сеанс', 'Эскизы'], ['Оценить']],
                                       resize_keyboard=True)
TIME, INFO, CONTACT = range(3)


#SKETCHES PART
def sketches_show(bot, update):
    photo = SKETCHES.get_random()
    update.message.reply_photo(photo=photo[1])
    update.message.reply_text('Эскиз под номером ' + photo[0])


def sketches_add(bot, update):
    photo_id = update.message.photo[-1].file_id
    SKETCHES.write(photo_id)
    update.message.reply_text('Добавил фото в эскизы', quote=True)


def session(bot, update):
    user = update.message.from_user
    new_user = classes.User(username=user.username, first_name=user.first_name, last_name=user.last_name)
    chat_id = update.message.chat_id
    USERS.update({chat_id: new_user})
    update.message.reply_text('Давайте запишем вас на сеанс!\n'
                              'Просто ответьте на пару вопросов)\n'
                              '/cancel - отмена записи\n\n'
                              'И первый вопрос\nКакое время для сеанса вас устраивает?',
                              quote=True)
    return TIME


def time(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    user = USERS.get(chat_id)
    user.add_time(text)
    update.message.reply_text('Время записал\n\n'
                              'Есть какие-то пожелания?\n', quote=True)
    return INFO


def info(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    user = USERS.get(chat_id)
    user.add_info(text)
    update.message.reply_text('Пожелания записал\n\n'
                              'Можем ли мы с вами связаться еще как-то кроме телеграма?\n'
                              'Мобильный телефон?  Viber?  WhatsApp?', quote=True)
    return CONTACT


def contact(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    user = USERS.get(chat_id)
    user.add_phone(text)
    update.message.reply_text(user.get())
    update.message.reply_text('Я отправил заполненую форму нашему работнику\n'
                              'Спасибо за ваше терпение\n'
                              'С вами свяжутся в ближайшее время',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END


def cancel(bot, update):
    chat_id = update.message.chat_id
    USERS.pop(chat_id, None)
    update.message.reply_text('Отменил запись, но мы всегда готовы вас обслужить!',
                              quote=True,
                              reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END


def start(bot, update):
    user = update.message.from_user

    update.message.reply_text('Приветики',
                              reply_markup=MAIN_MENU_MARKUP)


conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Запись на сеанс', session)],

        states={
            TIME: [MessageHandler(Filters.text, time)],

            INFO: [MessageHandler(Filters.text, info)],

            CONTACT: [MessageHandler(Filters.text, contact)]

        },

        fallbacks=[CommandHandler('cancel', cancel)])

bot_handlers = [CommandHandler('start', start),
                RegexHandler('Эскизы', sketches_show),
                MessageHandler(Filters.photo, sketches_add),
                conv_handler]