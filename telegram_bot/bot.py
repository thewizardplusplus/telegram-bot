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
    bot.send_message(
        env.get_env('CHANNEL'),
        text,
        reply_markup=_make_buttons_markup(),
    )

def send_photo(bot, filename):
    with open(filename, 'rb') as photo:
        bot.send_photo(
            env.get_env('CHANNEL'),
            photo,
            reply_markup=_make_buttons_markup(),
        )

def update_buttons(bot, db_connection, channel_id, message_id):
    bot.edit_message_reply_markup(
        channel_id,
        message_id,
        reply_markup=_make_buttons_markup(
            db.count_votes(db_connection, channel_id, message_id, 'accept'),
            db.count_votes(db_connection, channel_id, message_id, 'reject'),
        ),
    )

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
    text = _format_button_text(action, counter, counter)
    return telebot.types.InlineKeyboardButton(text, callback_data=action)

def _make_buttons_markup(accept_number=0, reject_number=0):
    total_number = accept_number + reject_number
    buttons_markup = telebot.types.InlineKeyboardMarkup()
    buttons_markup.row(
        telebot.types.InlineKeyboardButton(
            _format_button_text('accept', accept_number, total_number),
            callback_data='accept',
        ),
        telebot.types.InlineKeyboardButton(
            _format_button_text('reject', reject_number, total_number),
            callback_data='reject',
        ),
    )

    return buttons_markup

def _format_button_text(action, number, total_number):
    template = env.get_env(
        action.upper() + '_TEXT',
        action.capitalize() + ' ${number} (${percents}%)',
    )
    percents = number / total_number * 100 if number != 0 else 0
    return template \
        .replace('${number}', str(number)) \
        .replace('${percents}', '{:.2f}'.format(percents))
