import argparse
import logging

from . import consts

class HelpFormatter(
    argparse.RawTextHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
):
    pass

def parse_options():
    parser = argparse.ArgumentParser(
        prog=__package__,
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        help='show the version message and exit',
        version='Telegram Bot, v{}\n'.format(consts.APP_VERSION) \
            + 'Copyright (C) 2017-2018 thewizardplusplus',
    )
    parser.add_argument(
        '-f',
        '--log-file',
        metavar='PATH',
        default='./logs/app.log',
        help='base filename for rotated log files',
    )
    parser.add_argument(
        '-l',
        '--log-level',
        type=_parse_log_level,
        metavar='NAME',
        default='info',
        help='minimal allowed log level',
    )

    return vars(parser.parse_args())

def _parse_log_level(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise argparse.ArgumentTypeError('invalid log level: ' + level)

    return numeric_level
