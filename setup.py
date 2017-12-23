import sys
import os.path
import re
import setuptools

_PACKAGE_NAME = 'telegram_bot'
_PROJECT_NAME = _PACKAGE_NAME.replace('_', '-')

if not (0x030500f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.5, <4.0')

with open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    _PACKAGE_NAME,
    'consts.py',
), encoding='utf-8') as consts_file:
    version = re.search(
        "^APP_VERSION = '([^']+)'$",
        consts_file.read(),
        re.MULTILINE,
    ).group(1)

setuptools.setup(
    name=_PROJECT_NAME,
    version=version,
    license='GPL-3.0-or-later',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    packages=[_PACKAGE_NAME],
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'python-dotenv >=0.7.1, <1.0',
        'pyTelegramBotAPI >=3.5.1, <4.0',
        'tornado >=4.5.2, <5.0',
        'emoji >=0.4.5, <1.0',
    ],
    python_requires='>=3.5, <4.0',
    entry_points={'console_scripts': ['{} = {}:main'.format(
        _PROJECT_NAME,
        _PACKAGE_NAME,
    )]},
)
