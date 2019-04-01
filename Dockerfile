FROM python:3.7.3-alpine3.9

COPY . /usr/src/telegram-bot

WORKDIR /usr/src/telegram-bot

RUN pip install --no-cache-dir .

CMD ["python", "-m", "telegram_bot"]
