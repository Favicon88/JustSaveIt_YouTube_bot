from dotenv import dotenv_values
import random
import sqlite3
import telebot
from requests.exceptions import ReadTimeout
import json
import yt_dlp


env = {
    **dotenv_values("/home/ChatGPT_telegram_bot/.env.prod"),
    **dotenv_values(".env.dev"),  # override
}

bot = telebot.TeleBot(env["TG_BOT_TOKEN"])
db_link = env["DB_LINK"]

REKLAMA_MSG = [
    "🔥 Валютный вклад для россиян (до 12% годовых) https://crypto-fans.club",
    "🔥 Если думаешь купить или продать криптовалюту, рекомендую Bybit https://cutt.ly/D7rsbVG",
    "🔥 Если думаешь купить или продать криптовалюту, рекомендую Binance https://cutt.ly/87rsjAV",
]


def write_to_db(message):
    conn = sqlite3.connect(db_link)
    cursor = conn.cursor()
    select_id = cursor.execute(
        "SELECT id FROM user WHERE chat_id = ?", (str(message.chat.id),)
    )
    select_id = select_id.fetchone()
    if select_id:
        try:
            cursor.execute(
                "UPDATE user SET last_msg=?, last_login=? WHERE chat_id=?",
                (
                    message.text,
                    str(message.date),
                    str(message.chat.id),
                ),
            )
        except:
            conn.commit()
            conn.close()
            bot.send_message(
                612063160,
                f"Ошибка при добавлении (INSERT) данных в базе Пользователь: {message.chat.id}",
            )
    else:
        try:
            cursor.execute(
                "INSERT INTO user (chat_id, last_login, username, first_name, last_name, last_msg) VALUES (?,?,?,?,?,?)",
                (
                    str(message.chat.id),
                    str(message.date),
                    message.chat.username if message.chat.username else "-",
                    message.chat.first_name
                    if message.chat.first_name
                    else "-",
                    message.chat.last_name if message.chat.last_name else "-",
                    message.text,
                ),
            )
        except:
            conn.commit()
            conn.close()
            bot.send_message(
                612063160,
                f"Ошибка при добавлении (INSERT) данных в базе Пользователь: {message.chat.id}",
            )
    conn.commit()
    conn.close()


def make_request(message, api_key_numb):
    chance = random.choices((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
    try:
        bot.send_message(message.chat.id, piece_of_answer)
        if chance == [1]:
            bot.send_message(message.chat.id, random.choices(REKLAMA_MSG))
    except ReadTimeout:
        bot.send_message(
            message.chat.id,
            "ChatGPT в данный момент перегружен запросами, пожалуйста повторите свой запрос чуть позже.",
        )


def create_table():
    """Create table if not exists."""

    conn = sqlite3.connect(db_link)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            last_login TEXT,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            last_msg TEXT
        );
        """
    )
    conn.commit()
    conn.close()


@bot.message_handler(commands=["start"])
def send_start(message):
    text = """Приветствую ✌

Я - ChatGPT, крупнейшая языковая модель, созданная OpenAI. 

Я разработана для обработки естественного языка и могу помочь вам ответить на вопросы, 
обсудить темы или предоставить информацию на различные темы.

🔥В том числе на русском языке....🔥

👇Я постараюсь ответить на твои вопросы👇
"""
    write_to_db(message)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def send_msg_to_chatgpt(message):
    write_to_db(message)
    make_request(message, api_key_numb)


if __name__ == "__main__":
    yt_opts = {}
    url = "https://www.youtube.com/shorts/j-AkzBTmrTs"
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # info = ydl.extract_info(url, download=False)
        ydl.download(url)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        # print(json.dumps(ydl.sanitize_info(info)))
    # videos = yt.get_videos()
    # print(yt)
    # key_end = False
    # create_table()
    # target = bot.infinity_polling()
