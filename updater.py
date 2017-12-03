from os import environ
from telegram.ext import Updater


port = environ.get('PORT', 443)
token = environ.get('BOT_TOKEN')
url = environ.get('BOT_URL', '/')

bot_updater = Updater(token)


def start_listen():
    """Begin listening"""
    bot_updater.start_webhook(listen='0.0.0.0',
                              url_path=url,
                              port=port)
    bot_updater.bot.set_webhook("https://xktkbot.herokuapp.com/")

