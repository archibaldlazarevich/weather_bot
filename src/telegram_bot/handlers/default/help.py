from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from src.config.config import DEFAULT_COMMANDS

help_router = Router()


@help_router.message(Command("help"))
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот для получения прогноза погоды.\nКоманды, которые вы можете использовать:"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
