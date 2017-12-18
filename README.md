# Telegram Bot

[Telegram](https://telegram.org/) channel bot.

## Features

- publication into a specified channel:
  - sending of text messages;
- working mode:
  - run as a web service;
  - control via the RESTful API;
- utility for a sending of requests to the API.

## Installation

Clone this repository:

```
$ git clone https://github.com/thewizardplusplus/telegram-bot.git
$ cd telegram-bot
```

Then install the utility with [pip](https://pip.pypa.io/) tool:

```
$ sudo -H python3 -m pip install .
```

`sudo` command is required to install `telegram-bot` console script. If it's not required, `sudo` command can be omitted:

```
$ python3 -m pip install .
```

But then the utility should be started as `python3 -m telegram_bot`.

## Usage

```
$ telegram-bot -v | --version
$ telegram-bot -h | --help
$ telegram-bot
```

Options:

- `-v`, `--version` &mdash; show the version message and exit;
- `-h`, `--help` &mdash; show this help message and exit.

Environment variables:

- `TELEGRAM_BOT_TOKEN` &mdash; [Telegram](https://telegram.org/) API access token;
- `TELEGRAM_BOT_CHANNEL` &mdash; [Telegram](https://telegram.org/) channel name;
- `TELEGRAM_BOT_PORT` &mdash; bot API port (default: `4000`).

Environment variables can be specified in a `.env` config in the format:

```
NAME_1=value_1
NAME_2=value_2
...
```

See details about the format: https://github.com/motdotla/dotenv#rules.

A `.env` config will never modify any environment variables that have already been set.

## Usage of the Utility for a Sending of Requests to the API

```
$ ./tools/sender.bash -h
$ ./tools/sender.bash [-H HOST] [-P PORT] -t TEXT
```

Options:

- `-h` &mdash; show this help message;
- `-H HOST` &mdash; set a host name (default: `localhost`);
- `-P PORT` &mdash; set a port number (default: `4000`);
- `-t TEXT` &mdash; set a message text.

## API Description

API description in the [Swagger](http://swagger.io/) format: [docs/swagger.yaml](docs/swagger.yaml).

## License

GPL-3.0-or-later

Copyright &copy; 2017 thewizardplusplus
