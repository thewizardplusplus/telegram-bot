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
    bot.send_message(channel, text)

def send_photo(bot, filename):
    channel = env.get_env('CHANNEL')
    with open(filename, 'rb') as photo:
        bot.send_photo(channel, photo)
