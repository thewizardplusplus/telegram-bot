import os

import dotenv
import termcolor

from . import logger

def load_env():
    env_path = dotenv.find_dotenv(usecwd=True)
    if len(env_path) == 0:
        return

    dotenv.load_dotenv(env_path)
    logger.get_logger().info(
        'load the %s config %s',
        termcolor.colored('.env', 'magenta'),
        termcolor.colored(env_path, 'green'),
    )

def get_env(name, default=None):
    full_name = __package__.upper() + '_' + name
    return os.environ.get(full_name, default) \
        if default is not None \
        else os.environ[full_name]
