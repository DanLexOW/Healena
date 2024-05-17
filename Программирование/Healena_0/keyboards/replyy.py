from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

del_kb = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Кнопка4"),
    KeyboardButton(text="Кнопка5"),
)
start_kb2.adjust(1, 1)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.add(KeyboardButton(text="Добавочная кнопка"),)
start_kb2.adjust(1, 1)
#start_kb3.row(KeyboardButton(text="Добавочная кнопка"),)

test_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Создать опрос", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Отправить номер", request_contact=True),
            KeyboardButton(text="Создать опрос", request_location=True),
        ],
    ],
    resize_keyboard=True,
)
'''inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="меню"),
        ],
    ],
)'''

'''inline_kb = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_kb)'''