from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

import src.telegram_bot.handlers.custom.standard_func as standard
import src.telegram_bot.keyboards.reply as rep
from src.api.weather_api import get_weather_five_day
from src.database.func import check_position, get_users_coord, add_coord
from src.geolocator.geolocator import define_address

five_router = Router()


class Five(StatesGroup):
    init: State = State()


@five_router.message(Command("5_days"))
async def now_command_init(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Five.init)
    if await check_position(message.from_user.id):
        location = await get_users_coord(message.from_user.id)
        if location:
            await state.update_data(coord_state=location)
            await message.reply(
                f"Ваша последняя геопозиция по адресу:\n{await define_address(coord=location[:2])}",
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


@five_router.message(F.location, Five.init)
async def now_command_loc_new(message: Message, state: FSMContext):
    coord: tuple[float, float] = (
        message.location.latitude,
        message.location.longitude,
    )
    result: dict = await get_weather_five_day(coord=coord)
    if result:
        await add_coord(coord_with_user_id=(*coord, message.from_user.id))
        await standard.generate_five_answer(message= message, coord= coord, result= result)
    else:
        await state.clear()
        await standard.error_db(message=message, state=state)


@five_router.message(F.text == "Старая Геопозиция", Five.init)
async def now_command_loc_old(message: Message, state: FSMContext):
    await state.clear()
    coord = await get_users_coord(message.from_user.id)
    if coord:
        result: dict = await get_weather_five_day(coord=coord)
        if result:
            await add_coord(coord_with_user_id=(*coord, message.from_user.id))
            await standard.generate_five_answer(message= message, coord= coord, result= result)

        else:
            await state.clear()
            await standard.error_db(message=message, state=state)
    else:
        await state.clear()
        await standard.error_db(message=message, state=state)
