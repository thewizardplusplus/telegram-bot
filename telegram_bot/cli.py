import argparse

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
        version='{}, v{}\n'.format(consts.APP_NAME, consts.APP_VERSION) \
            + 'Copyright (C) 2017 thewizardplusplus',
    )

    return vars(parser.parse_args())
