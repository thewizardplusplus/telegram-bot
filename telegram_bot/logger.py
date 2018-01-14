import logging

import termcolor

class Formatter(logging.Formatter):
    _LEVELS_COLORS = {
        '[DEBUG]': 'cyan',
        '[INFO]': 'green',
        '[WARNING]': 'yellow',
        '[ERROR]': 'red',
    }

    def format(self, record):
        message = super().format(record)
        for level, color in self._LEVELS_COLORS.items():
            message = message.replace(level, termcolor.colored(level, color))

        return message

def get_logger():
    return logging.getLogger(__package__)

def init_logger():
    get_logger().addHandler(_make_stream_handler())
    get_logger().setLevel(logging.DEBUG)

def _make_stream_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(_make_formatter())

    return handler

def _make_formatter():
    return Formatter(
        fmt=termcolor.colored('%(asctime)s', 'grey') \
            + ' [%(levelname)s] %(message)s',
    )
