import os
from datetime import datetime

import telebot
from dotenv import load_dotenv


DATE_FORMATS = [
    "%d.%m.%y",
    "%d.%m.%Y",
    "%d/%m/%y",
    "%d/%m/%Y",
    "%Y-%m-%d"
]


def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    bot = telebot.TeleBot(bot_token)
    bot.set_my_commands([telebot.types.BotCommand("today", "Узнать номер текущей недели.")])

    @bot.message_handler(commands=['today'])
    def send_week(message):
        bot.reply_to(message, f"Неделя №{datetime.now().isocalendar().week}")

    @bot.message_handler(func=lambda m: True)
    def find_week(message):
        try:
            date = get_date(message.text)
            bot.send_message(message.chat.id, f"Неделя №{date.isocalendar().week}")
        except WrongDateException:
            bot.send_message(message.chat.id, "Введена некорректная дата, либо формат даты не был распознан. Попробуй формат 01.01.23")

    bot.infinity_polling()


def get_date(input_date: str):
    for date_format in DATE_FORMATS:
        try:
            date = datetime.strptime(input_date.strip(), date_format)
            return date
        except ValueError:
            continue
    raise WrongDateException()


class WrongDateException(Exception):
    def __init__(self, message="Wrong date format!"):
        super().__init__(message)


if __name__ == "__main__":
    main()
