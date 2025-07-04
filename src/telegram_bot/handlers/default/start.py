from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.config.config import DEFAULT_COMMANDS
from src.database.func import check_position

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот для получения прогноза погоды.\n"
        f"Команды, которые вы можете использовать:\n"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
    assert message.from_user is not None
    await check_position(message.from_user.id)
