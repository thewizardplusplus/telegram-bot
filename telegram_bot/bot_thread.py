import threading
import random

from . import bot

class BotThread(threading.Thread):
    def __init__(self, bot_client):
        super().__init__()

        self.bot_client = bot_client

    def run(self):
        @self.bot_client.callback_query_handler(func=lambda call: call.data in [
            'accept',
            'reject',
        ])
        def _buttons_callback(call):
            data = random.randint(0, 100)
            bot.update_buttons(
                self.bot_client,
                call.message.chat.id,
                call.message.message_id,
                **{call.data: data},
            )

        self.bot_client.polling(none_stop=True)

def init_bot_thread(bot_client):
    thread = BotThread(bot_client)
    thread.setDaemon(True)
    thread.start()
