# Change Log

## [v1.9](https://github.com/thewizardplusplus/telegram-bot/tree/v1.9) (2021-06-18)

- publication into a specified channel:
  - sending of text messages:
    - support emojis (with aliases);
  - sending of photo messages:
    - support a photo caption:
      - support emojis (with aliases);
- voting for messages (optional):
  - decor:
    - displaying of a voting result on buttons instead placeholders:
      - total number of votes.

## [v1.8](https://github.com/thewizardplusplus/telegram-bot/tree/v1.8) (2021-06-17)

- publication into a specified channel:
  - sending of text messages:
    - support the markup specifying:
      - allowed markups:
        - `Markdown`;
        - `MarkdownV2`;
        - `HTML`;
  - sending of photo messages:
    - support a photo caption:
      - support the markup specifying:
        - allowed markups:
          - `Markdown`;
          - `MarkdownV2`;
          - `HTML`;
- perform the refactoring:
  - add the `server.RequestHandler` class;
- add the documentation:
  - add the [Postman](https://www.postman.com/) collection.

## [v1.7](https://github.com/thewizardplusplus/telegram-bot/tree/v1.7) (2019-04-02)

- make voting for messages optional.

## [v1.6](https://github.com/thewizardplusplus/telegram-bot/tree/v1.6) (2019-04-01)

- add [Docker](https://www.docker.com/) configurations:
  - `Dockerfile`:
    - add a base configuration;
    - install app dependencies;
  - `docker-compose.yml`:
    - add a base configuration;
    - add a [Swagger](https://swagger.io/) configuration;
    - use a `.env` file outside an image.

## [v1.5](https://github.com/thewizardplusplus/telegram-bot/tree/v1.5) (2018-01-21)

- errors handling:
  - restart a bot polling on errors;
  - support a specified delay before a bot polling restart.

## [v1.4](https://github.com/thewizardplusplus/telegram-bot/tree/v1.4) (2018-01-15)

- custom logger:
  - log message format:
    - add a name of a logger to its messages;
    - automatically add a color into log messages:
      - for a JSON data;
      - for an URL;
      - for a path;
  - support a filtering of log messages by a specification of a minimal allowed log level;
  - logging to a file:
    - add a saving of log messages to a specified file;
    - support an automatic daily rotation of log files;
- use settings of the custom logger:
  - for the web server logger;
  - for the Telegram Bot API client logger;
- errors handling:
  - extend a logging of errors in the message button handler to all errors types;
  - add a logging of all errors types in the bot polling loop.

## [v1.3](https://github.com/thewizardplusplus/telegram-bot/tree/v1.3) (2017-12-23)

- support placeholders in a buttons text:
  - for a number of votes;
  - for a percent of votes;
- support a reverse of a buttons order;
- support emojis in a buttons text.

## [v1.2](https://github.com/thewizardplusplus/telegram-bot/tree/v1.2) (2017-12-20)

- support a voting for messages:
  - support inline keyboards in messages;
  - support an update of inline keyboards;
  - save a vote to a database.

## [v1.1](https://github.com/thewizardplusplus/telegram-bot/tree/v1.1) (2017-12-18)

- support a sending of photo messages:
  - in the web service;
  - in the sending utility;
- making of a path to a photo absolute in the sending utility.

## [v1.0](https://github.com/thewizardplusplus/telegram-bot/tree/v1.0) (2017-12-18)
