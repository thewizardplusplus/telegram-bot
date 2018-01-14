import sys

from . import logger
from . import cli
from . import env
from . import bot
from . import bot_thread
from . import server

def main():
    try:
        options = cli.parse_options()
        logger.init_logger(options['log_file'])
        env.load_env()

        bot_client = bot.init_bot()
        bot_thread.init_bot_thread(bot_client)
        server.init_server(bot_client)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
