# Telegram Bot

[Telegram](https://telegram.org/) channel bot.

## Features

- publication into a specified channel:
  - sending of text messages;
  - sending of photo messages;
- voting for messages:
  - restrictions (via a remembering in an SQLite database):
    - one vote per one user;
    - possibility change an own vote (optionally, i.e. may be disabled);
  - decor:
    - voting by an inline keyboard;
    - reverse of a buttons order (optionally);
    - customizable a buttons text via individual templates;
    - displaying of a voting result on buttons instead placeholders:
      - number of votes;
      - percent of votes;
    - support emojis (with aliases) in a buttons text;
- working mode:
  - run as a web service;
  - control via the RESTful API;
- utility for a sending of requests to the API:
  - making of a path to a photo absolute.

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
$ telegram-bot [options]
```

Options:

- `-v`, `--version` &mdash; show the version message and exit;
- `-h`, `--help` &mdash; show this help message and exit;
- `-f PATH`, `--log-file PATH` &mdash; base filename for rotated log files (default: `./logs/app.log`);
- `-l NAME`, `--log-level NAME` &mdash; minimal allowed log level (default: `info`).

Environment variables:

- `TELEGRAM_BOT_TOKEN` &mdash; [Telegram](https://telegram.org/) API access token;
- `TELEGRAM_BOT_CHANNEL` &mdash; [Telegram](https://telegram.org/) channel name;
- `TELEGRAM_BOT_PORT` &mdash; bot API port (default: `4000`);
- `TELEGRAM_BOT_ACCEPT_TEXT` &mdash; text of the accept button (default: `:thumbsup: #{number} (#{percents}%)`);
- `TELEGRAM_BOT_REJECT_TEXT` &mdash; text of the reject button (default: `:thumbsdown: #{number} (#{percents}%)`);
- `TELEGRAM_BOT_DATABASE` &mdash; path to the [SQLite](https://www.sqlite.org/) database file (default: `./votes.db`);
- `TELEGRAM_BOT_CHANGEABLE_VOTE` &mdash; flag denoting changeability of a vote (allowed: `FALSE` and `TRUE`; default: `TRUE`);
- `TELEGRAM_BOT_SWAP_BUTTONS` &mdash; flag denoting inversion of the order of the buttons (allowed: `FALSE` and `TRUE`; default: `TRUE`);
- `TELEGRAM_BOT_RESTART_DELAY` &mdash; delay before a bot polling restart (in milliseconds; default: `1000`).

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
$ ./tools/sender.bash [-H HOST] [-P PORT] -f PATH
```

Options:

- `-h` &mdash; show this help message;
- `-H HOST` &mdash; set a host name (default: `localhost`);
- `-P PORT` &mdash; set a port number (default: `4000`);
- `-t TEXT` &mdash; set a message text;
- `-f PATH` &mdash; set a path to a message photo.

## Documentation

- API description in the [Swagger](http://swagger.io/) format: [docs/swagger.yaml](docs/swagger.yaml);
- UML component diagram:
  - in the [PlantUML](https://plantuml.com/) language: [docs/architecture.plantuml](docs/architecture.plantuml);
  - render: [docs/architecture.svg](docs/architecture.svg).

## License

GPL-3.0-or-later

Copyright &copy; 2017-2018 thewizardplusplus
