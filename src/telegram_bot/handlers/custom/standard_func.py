from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove


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
