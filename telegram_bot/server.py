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

class PhotoHandler(tornado.web.RequestHandler):
    def initialize(self, bot_client):
        self._bot_client = bot_client

    def post(self):
        filename = self.get_body_argument('file').strip()
        if len(filename) == 0:
            raise tornado.web.HTTPError(400, "Argument file can't be empty")

        bot.send_photo(self._bot_client, filename)

def init_server(bot_client, options):
    for name in ['tornado.access', 'tornado.application', 'tornado.general']:
        logger.init_logger(logging.getLogger(name), options)

    port = int(env.get_env('PORT', 4000))
    server = tornado.web.Application([
        ('/api/v1/message', MessageHandler, {'bot_client': bot_client}),
        ('/api/v1/photo', PhotoHandler, {'bot_client': bot_client}),
    ])
    server.listen(port)

    logger.get_logger().info(
        'run the server on the %s port',
        termcolor.colored(str(port), 'yellow'),
    )

    tornado.ioloop.IOLoop.current().start()
