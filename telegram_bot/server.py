import logging

import tornado.ioloop
import tornado.web
import termcolor

from . import env
from . import logger

class MessageHandler(tornado.web.RequestHandler):
    def post(self):
        pass

def init_server():
    for name in ['tornado.access', 'tornado.application', 'tornado.general']:
        logging.getLogger(name).setLevel(logging.DEBUG)

    port = int(env.get_env('PORT', 4000))
    server = tornado.web.Application([
        ('/api/v1/message', MessageHandler),
    ])
    server.listen(port)

    logger.get_logger().info(
        'initialize the server on the %s port',
        termcolor.colored(str(port), 'yellow'),
    )

    tornado.ioloop.IOLoop.current().start()
