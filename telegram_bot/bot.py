import logging
import threading

import telebot
import termcolor

from . import env
from . import logger

def init_bot():
    telebot.logger.setLevel(logging.DEBUG)

    token = env.get_env('TOKEN')
    bot = telebot.TeleBot(token)
    @bot.callback_query_handler(func=lambda call: call.data in [
        'accept',
        'reject',
    ])
    def buttons_callback(call):
        logger.get_logger().debug(call)

    thread = threading.Thread(target=lambda: bot.polling(none_stop=True))
    thread.start()

    logger.get_logger().info(
        'initialize the %s bot',
        termcolor.colored('Telegram', 'magenta'),
    )

    bot_user = bot.get_me()
    logger.get_logger().debug(
        'bot user: %s',
        termcolor.colored(bot_user, 'cyan'),
    )

    return bot, thread

def send_message(bot, text):
    channel = env.get_env('CHANNEL')
    reply_markup = _make_reply_markup()
    bot.send_message(channel, text, reply_markup=reply_markup)

def send_photo(bot, filename):
    channel = env.get_env('CHANNEL')
    reply_markup = _make_reply_markup()
    with open(filename, 'rb') as photo:
        bot.send_photo(channel, photo, reply_markup=reply_markup)

def _make_reply_markup():
    accept_text = env.get_env('ACCEPT_TEXT', 'Accept')
    reject_text = env.get_env('REJECT_TEXT', 'Reject')
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(accept_text, callback_data='accept'),
        telebot.types.InlineKeyboardButton(reject_text, callback_data='reject'),
    )

    return markup

def _format_button_text(text, data):
    return '{} ({})'.format(text, data) if data is not None else text
