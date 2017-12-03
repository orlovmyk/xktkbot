from os import environ
from telegram.ext import Updater


port = environ.get('PORT', 443)
token = environ.get('BOT_TOKEN')
url = environ.get('BOT_URL', '/')

bot_updater = Updater(token=token)


def start_listen():
    """Begin listening"""
    bot_updater.start_webhook(url_path=url, port=port)

