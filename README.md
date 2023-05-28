# JustSaveIt_YouTube_bot

Телеграм бот скачивальщик

# Для обхода ограничения в 50МБ

Нобходимо запустить локальный телеграм сервер
Подробнее тут https://github.com/tdlib/telegram-bot-api

```
./telegram-bot-api.exe --api-id=1208003 --api-hash=3a1617006097879fcff9f4312eeb692b --http-port=4200

```

До запуска локального сервера необходимо отвязать бота от сервера телеграм
Документация telebot https://pypi.org/project/pyTelegramBotAPI/#using-local-bot-api-sever

```
from telebot import apihelper

bot.log_out()
apihelper.API_URL = "http://localhost:4200/bot{0}/{1}"

```
