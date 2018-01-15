import threading

import termcolor

from . import bot
from . import db
from . import logger
from . import utils

class BotThread(threading.Thread):
    def __init__(self, bot_client):
        super().__init__()

        self.bot_client = bot_client

    def run(self):
        logger.get_logger().info(
            'run a %s bot polling',
            termcolor.colored('Telegram', 'magenta'),
        )

        db_connection = db.init_db()
        @self.bot_client.callback_query_handler(func=lambda call: call.data in [
            'accept',
            'reject',
        ])
        def _buttons_callback(call):
            _handle_button_click(self.bot_client, db_connection, call)

        self.bot_client.polling(none_stop=True)

def init_bot_thread(bot_client):
    thread = BotThread(bot_client)
    thread.setDaemon(True)
    thread.start()

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
