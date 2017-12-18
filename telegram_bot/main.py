import sys

from . import logger
from . import cli
from . import env
from . import bot
from . import server

def main():
    logger.init_logger()

    try:
        options = cli.parse_options()
        env.load_env()

        bot_client = bot.init_bot()
        server.init_server(bot_client)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
