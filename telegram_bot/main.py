import sys

from . import logger
from . import cli
from . import env
from . import bot
from . import server
from . import db

def main():
    logger.init_logger()

    try:
        options = cli.parse_options()
        env.load_env()

        db_connection = db.init_db()
        bot_client, _ = bot.init_bot()
        server.init_server(bot_client)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
