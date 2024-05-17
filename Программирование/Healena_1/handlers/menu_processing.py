from aiogram.types import InputMediaPhoto
from aiogram.utils.formatting import Bold
from aiogram.utils.markdown import bold, italic
from sqlalchemy.ext.asyncio import AsyncSession

#from data_base.orm_query import orm_get_banner
from keyboards.inline import get_user_main_btns, get_user_calc_btns, get_user_talk_btns, get_user_train_btns


async def main_menu(level, menu_name):
    image = InputMediaPhoto(media="https://vkusvill.ru/upload/resize/624924/624924_1200x600x70_c.webp", caption="Добро пожаловать!")

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
    image = InputMediaPhoto(media="https://vkusvill.ru/upload/resize/624924/624924_1200x600x70_c.webp", caption="Абонент в данный момент не может разговаривать. Перезвоните позднее, а лучше никогда")

    kbds = get_user_talk_btns(level=level)

    return image, kbds


async def about_menu(level, menu_name):
    image = InputMediaPhoto(media="https://vkusvill.ru/upload/resize/624924/624924_1200x600x70_c.webp", caption="Один раз - не ананас")

    kbds = get_user_talk_btns(level=level)

    return image, kbds


async def habits_menu(level, menu_name):
    image = InputMediaPhoto(media="https://img.freepik.com/free-photo/cocktail-refreshment-in-neo-futuristic-style_23-2151370363.jpg?size=626&ext=jpg&ga=GA1.1.2008272138.1712707200&semt=ais")
    image.caption = "Помогу изабавиться от вредной привычки, будь то злоупотребление алкоголем, курением или сидячий образ жизни"
    image.caption += "\nP.S.\nБудет больно😈"
    kbds = get_user_talk_btns(level=level)

    return image, kbds


async def train_menu(level, menu_name):
    image = InputMediaPhoto(media="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7-AHOS-kb7GFREW7Tyz48AyilMs-hx-LzIDtzx6vtYfmouxXAorEPwoyPKie1v3q9GBc&usqp=CAU")
    image.caption = "Время растрясти жирок"
    if level == 2:
        image.caption = "План тренировок появится позже, когда программист закончит смотреть Евангелион🤖"
    kbds = get_user_train_btns(level=level)

    return image, kbds


'''async def return_menu(level, menu_name):
    image = InputMediaPhoto(media="https://media.istockphoto.com/id/945048938/ru/векторная/назад-стрелка-значок-специальная-фиолетовая-круглая-кнопка.jpg?s=612x612&w=0&k=20&c=95BOTDGGWYf7QQJAWPPJSF-J-sksNFku97AqpmFSx7Q=")
    kbds = get_return_menu_button(level=level)
    return image, kbds'''


async def get_menu_content(
    #session: AsyncSession,
    level: int,
    menu_name: str,
):
    print(level, menu_name)
    if level == 0 and menu_name == "main":
        return await main_menu(level, menu_name)
    elif level == 1 and menu_name == "talk":
        return await talk_menu(level, menu_name)
    elif level == 1 and menu_name == "about":
        return await about_menu(level, menu_name)
    elif level == 1 and menu_name == "habits":
        return await habits_menu(level, menu_name)
    elif level == 1 and menu_name == "train":
        return await train_menu(level, menu_name)
    elif level == 2 and menu_name == "train":
        return await train_menu(level, menu_name)
    elif menu_name == "calculator":
        return await calc_menu(level, menu_name)