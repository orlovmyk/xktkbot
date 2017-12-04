from os import environ
from telegram.ext import Updater


port = environ.get('PORT', 5000)
token = environ.get('BOT_TOKEN')
url = environ.get('BOT_URL', '')

bot_updater = Updater(token)


def start_listen():
    """Begin listening"""
    #bot_updater.bot.set_webhook("https://xktkbot.herokuapp.com/")
    bot_updater.start_webhook(url_path=url,
                              port=port,
                              listen='0.0.0.0')
    bot_updater.bot.set_webhook("https://xktkbot.herokuapp.com/")
    bot_updater.idle()


