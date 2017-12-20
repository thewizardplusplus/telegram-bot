import logging

import telebot
import termcolor

from . import env
from . import logger

def init_bot():
    telebot.logger.setLevel(logging.DEBUG)

    token = env.get_env('TOKEN')
    bot = telebot.TeleBot(token)
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

def update_buttons(bot, channel_id, message_id, **kwargs):
    reply_markup = _make_reply_markup(**kwargs)
    bot.edit_message_reply_markup(
        channel_id,
        message_id,
        reply_markup=reply_markup,
    )

def _make_reply_markup(**kwargs):
    accept_text = _format_button_text(
        env.get_env('ACCEPT_TEXT', 'Accept'),
        kwargs.get('accept', None),
    )
    reject_text = _format_button_text(
        env.get_env('REJECT_TEXT', 'Reject'),
        kwargs.get('reject', None),
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(accept_text, callback_data='accept'),
        telebot.types.InlineKeyboardButton(reject_text, callback_data='reject'),
    )

    return markup

def _format_button_text(text, data):
    return '{} ({})'.format(text, data) if data is not None else text
