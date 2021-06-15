import logging

import tornado.ioloop
import tornado.web
import termcolor

from . import env
from . import logger
from . import bot

_REQUIRED_ARGUMENT = tornado.web.RequestHandler._ARG_DEFAULT
_ALLOWED_FORMATS = ['Markdown', 'MarkdownV2', 'HTML']

class RequestHandler(tornado.web.RequestHandler):
    def _get_custom_argument(
        self,
        name,
        defaultValue=_REQUIRED_ARGUMENT,
        allowedValues=None,
    ):
        value = self.get_body_argument(name, defaultValue)
        if value is None:
            return None

        value = value.strip()
        if defaultValue == _REQUIRED_ARGUMENT and value == '':
            raise tornado.web.HTTPError(400, f'Argument {name} cannot be empty')
        if allowedValues is not None and value not in allowedValues:
            message = \
                f'Argument {name} is incorrect; allowed values: {allowedValues}'
            raise tornado.web.HTTPError(400, message)

        return value

class MessageHandler(RequestHandler):
    def initialize(self, bot_client):
        self._bot_client = bot_client

    def post(self):
        text = self._get_custom_argument('text')
        format = self._get_custom_argument('format', None, _ALLOWED_FORMATS)
        bot.send_message(self._bot_client, text, format)

class PhotoHandler(RequestHandler):
    def initialize(self, bot_client):
        self._bot_client = bot_client

    def post(self):
        filename = self._get_custom_argument('file')
        text = self._get_custom_argument('text', None)
        format = self._get_custom_argument('format', None, _ALLOWED_FORMATS)
        bot.send_photo(self._bot_client, filename, text, format)

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
