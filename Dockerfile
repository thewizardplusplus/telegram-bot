FROM python:3.9.5-alpine3.13

WORKDIR /usr/src/telegram-bot
COPY . .
RUN pip install --no-cache-dir .

CMD ["python", "-m", "telegram_bot"]
