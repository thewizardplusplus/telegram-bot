import contextlib

import telebot
import termcolor
import emoji

from . import env
from . import logger
from . import db

_DEFAULT_BUTTON_TEXT_SUFFIX = ' #{number}/#{total_number} (#{percents}%)'
_BUTTONS_TEXTS = {
    action: text + _DEFAULT_BUTTON_TEXT_SUFFIX
    for action, text in {
        'accept': ':thumbsup:',
        'reject': ':thumbsdown:',
    }.items()
}

def init_bot(options):
    logger.init_logger(telebot.logger, options)

    token = env.get_env('TOKEN')
    bot = telebot.TeleBot(token, threaded=False)
    logger.get_logger().info(
        'initialize the %s bot',
        termcolor.colored('Telegram', 'magenta'),
    )

    bot_user = bot.get_me()
    logger.get_logger().debug('bot user: ' + str(bot_user))

    return bot

def send_message(bot, text, format=None):
    bot.send_message(
        env.get_env('CHANNEL'),
        emoji.emojize(text, use_aliases=True),
        parse_mode=format,
        reply_markup=_make_buttons_markup(),
    )

def send_photo(bot, filename, text=None, format=None):
    with open(filename, 'rb') as photo:
        bot.send_photo(
            env.get_env('CHANNEL'),
            photo,
            caption=emoji.emojize(text, use_aliases=True) \
                if text is not None else None,
            parse_mode=format,
            reply_markup=_make_buttons_markup(),
        )

def send_photos(bot, filenames):
    with contextlib.ExitStack() as stack:
        bot.send_media_group(env.get_env('CHANNEL'), (
            telebot.types.InputMediaPhoto(photo)
            for filename in filenames
            for photo in (stack.enter_context(open(filename, 'rb')),)
        ))

def update_buttons(bot, db_connection, channel_id, message_id):
    bot.edit_message_reply_markup(
        channel_id,
        message_id,
        reply_markup=_make_buttons_markup(
            db.count_votes(db_connection, channel_id, message_id, 'accept'),
            db.count_votes(db_connection, channel_id, message_id, 'reject'),
        ),
    )

def _make_buttons_markup(accept_number=0, reject_number=0):
    if env.get_env('VOTING', 'TRUE') != 'TRUE':
        return None

    total_number = accept_number + reject_number
    buttons = [
        telebot.types.InlineKeyboardButton(
            _format_button_text('accept', accept_number, total_number),
            callback_data='accept',
        ),
        telebot.types.InlineKeyboardButton(
            _format_button_text('reject', reject_number, total_number),
            callback_data='reject',
        ),
    ]
    if env.get_env('SWAP_BUTTONS', 'TRUE') == 'TRUE':
        buttons = list(reversed(buttons))

    buttons_markup = telebot.types.InlineKeyboardMarkup()
    buttons_markup.row(*buttons)

    return buttons_markup

def _format_button_text(action, number, total_number):
    template = emoji.emojize(env.get_env(
        action.upper() + '_TEXT',
        _BUTTONS_TEXTS.get(
            action,
            action.capitalize() + _DEFAULT_BUTTON_TEXT_SUFFIX,
        ),
    ), use_aliases=True)
    percents = number / total_number * 100 if number != 0 else 0
    return template \
        .replace('#{number}', str(number)) \
        .replace('#{total_number}', str(total_number)) \
        .replace('#{percents}', '{:.2f}'.format(percents))
