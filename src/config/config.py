import os
from typing import cast

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не найдены, т.к. отсутствует файл .env")
else:
    load_dotenv()

DATABASE_URL: str = cast(str, os.getenv("DATABASE_URL"))
BOT_TOKEN: str = cast(str, os.getenv("BOT_TOKEN"))
API_KEY: str = cast(str, os.getenv("API_KEY"))

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Справка"),
    ("now", "Погода в настоящее время"),
    ("5_days", "Прогноз погоды на 5 дней"),
)
