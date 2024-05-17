from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str


def get_user_main_btns(*, level: int, sizes: tuple[int] = (1, 1, 2, 1)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Калькулятор калорий 🧮": "calculator",
        "Вредные привычки 🚬": "habits",
        "Тренировки 💪": "train",
        "Поговорить 🤭": "talk",
        "О нас ℹ️": "about",
    }
    for text, menu_name in btns.items():
        if menu_name == 'calculator':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'talk':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'about':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'habits':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'train':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_calc_btns(*, level: int, sizes: tuple[int] = (1, 2)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Начать калькулировать калории": "Start_calc",
        "Главное меню": "main"
    }
    for text, menu_name in btns.items():
        if level == 1 and menu_name == "Start_calc":
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1,
                                                                         menu_name="calculator").pack()))
        elif menu_name == "Back" and level != 1:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level - 1, menu_name="calculator").pack()))
        elif menu_name == "main":
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=0, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_talk_btns(*, level: int, sizes: tuple[int] = (1, 2)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Главное меню": "Main"
    }

    for text, menu_name in btns.items():
        keyboard.add(InlineKeyboardButton(text=text,
                                          callback_data=MenuCallBack(level=0, menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_habits_btns(*, level: int, sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Алкогольная": "Drink",
        "Никотиновая": "Smoke",
        "Назад": "Back",
        "Главное меню": "Main"
    }

    for text, menu_name in btns.items():
        if menu_name == "Back" and level != 1:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level - 1, menu_name="habits").pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_train_btns(*, level: int, sizes: tuple[int] = (1, 2)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Начать качаться": "Start_train",
        "Назад": "Back",
        "Главное меню": "main"
    }
    for text, menu_name in btns.items():
        if level == 1 and menu_name == "Start_train":
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1,
                                                                         menu_name="train").pack()))
        elif menu_name == "main":
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=0, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


return_menu = InlineKeyboardBuilder()
return_menu.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="return"))


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
