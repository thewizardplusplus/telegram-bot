import logging

import tornado.ioloop
import tornado.web
import termcolor

from . import env
from . import logger
from . import bot

class MessageHandler(tornado.web.RequestHandler):
    def initialize(self, bot_client):
        self._bot_client = bot_client

    def post(self):
        text = self.get_body_argument('text').strip()
        if len(text) == 0:
            raise tornado.web.HTTPError(400, "Argument text can't be empty")

        bot.send_message(self._bot_client, text)

def init_server(bot_client):
    for name in ['tornado.access', 'tornado.application', 'tornado.general']:
        logging.getLogger(name).setLevel(logging.DEBUG)

    port = int(env.get_env('PORT', 4000))
    server = tornado.web.Application([
        ('/api/v1/message', MessageHandler, {'bot_client': bot_client}),
    ])
    server.listen(port)

    logger.get_logger().info(
        'initialize the server on the %s port',
        termcolor.colored(str(port), 'yellow'),
    )

    tornado.ioloop.IOLoop.current().start()
