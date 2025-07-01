from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

geo_without_coord_in_database = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Новая Геопозиция", request_location=True)]
    ],
    resize_keyboard=True,
)

geo_with_coord_in_database = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Новая Геопозиция", request_location=True)],
        [KeyboardButton(text="Старая Геопозиция")],
    ],
    resize_keyboard=True,
)
