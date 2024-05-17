from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from keyboards.inline import MenuCallBack

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="меню"),

        ],
        [
            KeyboardButton(text="Кнопка2"),
            KeyboardButton(text="Кнопка3"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

mood_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="хорошее, спасибо, что спросила😁"),
        ],
        [
            KeyboardButton(text="Настроение сделать что-нибудь кринжовое🙈, можешь посоветовать что-то?"),
        ],
        [
            KeyboardButton(text="Ужас, я сижу дома целыми днями одержимая учебой, и когда меня зовут куда-нибудь, я всегда отказываюсь под тупым предлогом.🧟‍♀️"),
        ],
        [
            KeyboardButton(text="Гамаю и смотрю хентай🍹"),
        ],
        [
            KeyboardButton(text="Ой все💅"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Какое у вас настроение?"
)


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

