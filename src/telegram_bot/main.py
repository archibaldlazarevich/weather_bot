import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.config.config import BOT_TOKEN, DEFAULT_COMMANDS
from src.telegram_bot.handlers.custom.five_days import five_router
from src.telegram_bot.handlers.custom.now import now_router
from src.telegram_bot.handlers.default.help import help_router
from src.telegram_bot.handlers.default.start import start_router
from src.telegram_bot.middlewares.middleware import Middleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(start_router, help_router, five_router, now_router)
    dp.startup.register(start_bot)
    dp.message.middleware(Middleware())
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_description(
            "WeatherBot - Это телеграмм-бот, который предоставляет\n"
            "прогноз погоды по вашему местоположению на текущее\n"
            "время либо на ближайшие пять суток.",
            language_code="ru",
        )
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
