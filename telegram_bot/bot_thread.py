import threading
import functools
import time

import termcolor

from . import bot
from . import db
from . import logger
from . import utils
from . import env

class BotThread(threading.Thread):
    def __init__(self, bot_client):
        super().__init__()
        self._bot_client = bot_client

    def run(self):
        restart_delay = int(env.get_env('RESTART_DELAY', 1000)) / 1000
        while True:
            _init_bot_polling(self._bot_client)
            time.sleep(restart_delay)

def init_bot_thread(bot_client):
    thread = BotThread(bot_client)
    thread.setDaemon(True)
    thread.start()

@utils.catch_exceptions
def _init_bot_polling(bot_client):
    logger.get_logger().info(
        'run a %s bot polling',
        termcolor.colored('Telegram', 'magenta'),
    )

    db_connection = db.init_db()
    bot_client.callback_query_handler(
        func=lambda call: call.data in ['accept', 'reject'],
    )(functools.partial(_handle_button_click, bot_client, db_connection))

    bot_client.polling(none_stop=True)

@utils.catch_exceptions
def _handle_button_click(bot_client, db_connection, call):
    db.add_vote(
        db_connection,
        call.message.chat.id,
        call.message.message_id,
        call.from_user.id,
        call.data,
    )

    bot.update_buttons(
        bot_client,
        db_connection,
        call.message.chat.id,
        call.message.message_id,
    )
