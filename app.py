"""
Launch from here 
No telegram imports, only this bot modules

specify this environs pls
BOT_TOKEN
BOT_PORT (default = 5000)
BOT_URL (default = '')
"""
import updater
import handlers


def main():
    Dispatcher = updater.bot_updater.dispatcher
    Handlers = handlers.bot_handlers

    for handler in Handlers:
        Dispatcher.add_handler(handler)

    updater.start_listen()

if __name__ == '__main__':
    main()
