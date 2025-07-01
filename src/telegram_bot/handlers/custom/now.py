from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

import src.telegram_bot.handlers.custom.standard_func as standard
import src.telegram_bot.keyboards.reply as rep
from src.api.weather_api import get_weather_for_now
from src.database.func import add_coord, check_position, get_users_coord
from src.geolocator.geolocator import define_address

now_router = Router()


class Now(StatesGroup):
    init: State = State()


@now_router.message(Command("now"))
async def now_command_init(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Now.init)
    assert message.from_user is not None
    if await check_position(message.from_user.id):
        location = await get_users_coord(message.from_user.id)
        if location:
            await state.update_data(coord_state=location)
            await message.reply(
                f"Ваша последняя геопозиция по адресу:\n"
                f"{await define_address(coord=location[:2])}",
                reply_markup=ReplyKeyboardRemove(),
            )
            await message.reply_location(location[0], location[1])
            await message.reply(
                "Выберите необходимый пункт меню:",
                reply_markup=rep.geo_with_coord_in_database,
            )
        else:
            await standard.error_db(message=message, state=state)
    else:
        await message.reply(
            "Пожалуйста, отправьте свою геопозицию.",
            reply_markup=rep.geo_without_coord_in_database,
        )


@now_router.message(F.location, Now.init)
async def now_command_loc_new(message: Message, state: FSMContext):
    assert message.location is not None
    assert message.from_user is not None
    coord: tuple[float, float] = (
        message.location.latitude,
        message.location.longitude,
    )
    result = await get_weather_for_now(coord=coord)
    if result:
        await add_coord(coord_with_user_id=(*coord, message.from_user.id))
        place_data = await define_address(coord=coord)
        await state.clear()
        await message.reply(
            f"Прогноз погоды в {place_data} на {result['time']}:\n"
            f"- {result['description']}\n"
            f"- {result['temp']}°C",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.clear()
        await standard.error_db(message=message, state=state)


@now_router.message(F.text == "Старая Геопозиция", Now.init)
async def now_command_loc_old(message: Message, state: FSMContext):
    await state.clear()
    assert message.from_user is not None
    coord = await get_users_coord(message.from_user.id)
    if coord:
        result = await get_weather_for_now(coord=coord)
        if result:
            place_data = await define_address(coord=coord)
            await add_coord(coord_with_user_id=(*coord, message.from_user.id))
            await message.reply(
                f"Прогноз погоды в {place_data} на {result['time']}:\n"
                f"- {result['description']}\n"
                f"- {result['temp']}°C",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await state.clear()
            await standard.error_db(message=message, state=state)
    else:
        await state.clear()
        await standard.error_db(message=message, state=state)
