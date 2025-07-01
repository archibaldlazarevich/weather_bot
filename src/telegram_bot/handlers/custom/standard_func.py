from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.geolocator.geolocator import define_address


async def error_db(message: Message, state: FSMContext):
    """
    Метод для ответа пользователю при ошибке данных при взамодействии с бд
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await message.reply(
        "Ошибка в работе базы данных.", reply_markup=ReplyKeyboardRemove()
    )


async def wrong_answer(func: Callable, message: Message, state: FSMContext):
    """
    Функция, которая отправляет ответ об некорректном выборе
    данных из предложенных и отправляет заново клавиатуру
    :param state:
    :param message:
    :param func:
    :return:
    """
    await message.reply(
        "Выберите данные из предложенных вариантов, пожалуйста.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await func(message=message, state=state)


async def generate_five_answer(message: Message, result: dict, coord: tuple):
    """
    Функция для отправки ответа при прогнозе 5-ти дней
    :param coord:
    :param message:
    :param result:
    :return:
    """
    place_data = await define_address(coord=coord)
    answer = f"Прогноз погоды в {place_data} на ближайшие 5 дней:\n------\n"
    for key, value in result.items():
        answer += (
            f"На {key}:\n"
            f"- {value['description']}\n"
            f"- {value['templ']}°C\n------\n"
        )
    await message.reply(text=answer, reply_markup=ReplyKeyboardRemove())
