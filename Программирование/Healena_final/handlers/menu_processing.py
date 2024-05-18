from aiogram.types import InputMediaPhoto
from keyboards.inline import get_user_main_btns, get_user_calc_btns, get_user_talk_btns, get_user_train_btns, \
    get_user_habits_btns


async def main_menu(level, menu_name):
    image = InputMediaPhoto(media="https://img.goodfon.ru/original/2000x1117/8/bd/noch-neon-gorod-krysha-devushka.jpg")

    kbds = get_user_main_btns(level=level)

    return image, kbds


async def calc_menu(level, menu_name):
    image = InputMediaPhoto(media="https://apollo.online/wp-content/uploads/2021/10/kkal_01-768x512.jpg", caption="Займёмся математикой")
    capt = ""
    if level == 2:
        capt = "Укажите свою цель (так, как указано здесь): \n\nпохудеть\nнабрать вес\nподдерживать вес"
    image.caption = capt
    kbds = get_user_calc_btns(level=level)

    return image, kbds


async def talk_menu(level, menu_name):
    image = InputMediaPhoto(media="https://img.goodfon.ru/original/2000x1117/8/bd/noch-neon-gorod-krysha-devushka.jpg", caption="В данный момент функция находится в разработке и временно недоступна. Спасибо за проявленный интерес, следите за обновлениями!")

    kbds = get_user_talk_btns(level=level)

    return image, kbds


async def about_menu(level, menu_name):
    image = InputMediaPhoto(media="https://img.goodfon.ru/original/2000x1117/8/bd/noch-neon-gorod-krysha-devushka.jpg")

    kbds = get_user_talk_btns(level=level)

    return image, kbds


async def habits_menu(level, menu_name):
    image = InputMediaPhoto(media="https://img.freepik.com/free-photo/cocktail-refreshment-in-neo-futuristic-style_23-2151370363.jpg?size=626&ext=jpg&ga=GA1.1.2008272138.1712707200&semt=ais")
    image.caption = "Помогу изабавиться от вредной привычки, будь то алкогольная или никотиновая зависимость. Но я довольно молодая, а также не доктор и реалист. Понимаю, что избавиться от зависимости очень тяжело, а в формате общения со мной тем более."
    image.caption += "\nПоэтому могу лишь дать пару-тройку советов, как при сильном желании упростить себе задачу.👌"
    image.caption += "\n\nУкажите, от какой зависимости страдаете. Если таковой нет, поздравляю! Возвращайтесь в главное меню"
    kbds = get_user_habits_btns(level=level)

    return image, kbds


async def train_menu(level, menu_name):
    image = InputMediaPhoto(media="https://sportishka.com/uploads/posts/2023-03/1678236260_sportishka-com-p-energiya-sporta-sport-krasivo-2.jpg")
    image.caption = "Время растрясти жирок!🤩\n\n"
    if level == 2:
        image.caption += "Давайте я задам вам пару вопросов с целью определить, какие тренировки вам подойдут на данный момент\n"
        image.caption += "\nВведите М или Ж в зависимости от того, кого бы вам хотелось видеть в качестве тренера"

    kbds = get_user_train_btns(level=level)

    return image, kbds


async def get_menu_content(
    level: int,
    menu_name: str,
):
    if level == 0 and menu_name == "main":
        return await main_menu(level, menu_name)
    elif level == 1 and menu_name == "talk":
        return await talk_menu(level, menu_name)
    elif level == 1 and menu_name == "about":
        return await about_menu(level, menu_name)
    elif menu_name == "habits":
        return await habits_menu(level, menu_name)
    elif menu_name == "train":
        return await train_menu(level, menu_name)
    elif menu_name == "calculator":
        return await calc_menu(level, menu_name)