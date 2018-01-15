import logging
import os
import re

import termcolor

class Formatter(logging.Formatter):
    _LEVELS_COLORS = {
        '[DEBUG]': 'cyan',
        '[INFO]': 'green',
        '[WARNING]': 'yellow',
        '[ERROR]': 'red',
    }
    _PATTERNS_COLORS = {
        re.compile(r'\{.*\}'): 'cyan', # JSON
        re.compile(r'https?:\/\/[\w-]+(\.[\w-]+)+([/?#]\S*)?'): 'green', # URL
        re.compile(r'(?<=\s)\/\S*'): 'green', # path
    }

    def format(self, record):
        message = super().format(record)
        for level, color in self._LEVELS_COLORS.items():
            message = message.replace(level, termcolor.colored(level, color))
        for pattern, color in self._PATTERNS_COLORS.items():
            message = pattern.sub(
                lambda match: termcolor.colored(match.group(0), color),
                message,
            )

        return message

def get_logger():
    return logging.getLogger(__package__)

def init_logger(logger, options):
    logger.handlers = []
    logger.addHandler(_make_stream_handler())
    logger.addHandler(_make_file_handler(options['log_file']))

    logger.setLevel(options['log_level'])

def _make_stream_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(_make_formatter())

    return handler

def _make_file_handler(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    handler = logging.handlers.TimedRotatingFileHandler(filename, when='d')
    handler.setFormatter(_make_formatter())

    return handler

def _make_formatter():
    return Formatter(
        fmt='{} [%(levelname)s] {} %(message)s'.format(
            termcolor.colored('%(asctime)s', 'grey'),
            termcolor.colored('(%(name)s)', 'blue'),
        ),
    )
