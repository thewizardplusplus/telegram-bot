import logging

import telebot
import termcolor

from . import env
from . import logger
from . import db

def init_bot():
    telebot.logger.setLevel(logging.DEBUG)

    token = env.get_env('TOKEN')
    bot = telebot.TeleBot(token, threaded=False)
    logger.get_logger().info(
        'initialize the %s bot',
        termcolor.colored('Telegram', 'magenta'),
    )

    bot_user = bot.get_me()
    logger.get_logger().debug(
        'bot user: %s',
        termcolor.colored(bot_user, 'cyan'),
    )

    return bot

def send_message(bot, text):
    channel = env.get_env('CHANNEL')
    reply_markup = _make_reply_markup()
    bot.send_message(channel, text, reply_markup=reply_markup)

def send_photo(bot, filename):
    channel = env.get_env('CHANNEL')
    reply_markup = _make_reply_markup()
    with open(filename, 'rb') as photo:
        bot.send_photo(channel, photo, reply_markup=reply_markup)

def update_buttons(bot, db_connection, channel_id, message_id):
    reply_markup = _make_reply_markup(db_connection, channel_id, message_id)
    bot.edit_message_reply_markup(
        channel_id,
        message_id,
        reply_markup=reply_markup,
    )

def _make_reply_markup(db_connection=None, channel_id=None, message_id=None):
    accept_button = _make_button_markup(
        'accept',
        db_connection,
        channel_id,
        message_id,
    )
    reject_button = _make_button_markup(
        'reject',
        db_connection,
        channel_id,
        message_id,
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(accept_button, reject_button)

    return markup

def _make_button_markup(
    action,
    db_connection=None,
    channel_id=None,
    message_id=None,
):
    counter = db.count_votes(
        db_connection,
        channel_id,
        message_id,
        action,
    ) if all((db_connection, channel_id, message_id)) else 0
    text = _format_button_text(
        env.get_env(action.upper() + '_TEXT', action.capitalize()),
        counter,
    )
    return telebot.types.InlineKeyboardButton(text, callback_data=action)

def _format_button_text(text, data):
    return '{} ({})'.format(text, data) if data is not None else text
