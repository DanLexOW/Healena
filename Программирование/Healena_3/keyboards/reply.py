from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


koef_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Минимальная"),
            KeyboardButton(text="Низкая"),
            KeyboardButton(text="Умеренная"),
        ],
        [
            KeyboardButton(text="Высокая"),
            KeyboardButton(text="Экстремальная"),
        ],
    ],
    resize_keyboard=True,
)

habits_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Алкогольная"),
            KeyboardButton(text="Никотиновая")
        ],
    ],
    resize_keyboard=True,
)

del_kb = ReplyKeyboardRemove()

