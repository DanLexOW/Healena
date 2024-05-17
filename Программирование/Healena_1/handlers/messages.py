import logging

import letter

from keyboards.reply import koef_kb, del_kb

logger = logging.getLogger(__name__)

from curses.ascii import isdigit

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import or_f, StateFilter, callback_data
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputFile
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.orm_query import orm_get_products, orm_get_product, orm_get_training
from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from handlers.menu_processing import get_menu_content
from keyboards import reply, inline
from keyboards.inline import MenuCallBack, get_callback_btns

rt = Router()
rt.message.filter(ChatTypeFilter(["private"]))



'''@rt.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=reply.start_kb)

@rt.message(or_f(Command("menu"), F.text.lower() == "меню"))
async def cmd_menu(message: types.Message):
    await message.reply("Вот меню", reply_markup=reply.del_kb)

@rt.message(or_f(Command("mood"), F.text.lower() == "Хочешь узнать какое у меня настроение?"))
async def cmd_menu(message: types.Message):
    await message.reply("Как настроение?", reply_markup=reply.mood_kb)
    .as_markup(
        resize_keyboard=True,
        input_field_placeholder="Какое у вас сейчас настроение?"
    ))


@rt.message(or_f(Command('inline_keyboard'), F.text.lower() == "Клавиатура"))
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=reply.inline_kb)

@rt.message(F.photo)
async def rollers(message: types.Message):
    #await message.reply("Поздравляю с приобретением")
    await message.answer_photo(photo="https://avatars.dzeninfra.ru/get-zen_doc/1900266/pub_5e99f4f091221741687d5b9f_5e99f71e0efcae26c2f46bab/scale_1200")
'''


class FSM(StatesGroup):
    main__menu = State()
    #enter_report = State()
    target_state = State()
    sex_state = State()
    age_state = State()
    weight_state = State()
    height_state = State()
    koef_state = State()
    enter_stat = State()
    stat_entered = State()


@rt.message(CommandStart())
async def start_cmd(message: types.Message):
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    #await message.answer("Добро пожаовать!")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@rt.message(StateFilter("*"), Command("enter_meal_statistics"))
async def cmd_stat(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите одним сообщением список продуктов в единственном числе и начальной форме, входящих в ваш последний прием пищи, в формате\nПродукт_его масса(в граммах числом)\nВторой продукт_его масса\n(и так далее)",
    )
    '''current_state = await state.get_state()
    if current_state == :'''
    await state.set_state(FSM.enter_stat)


@rt.message(StateFilter("*"), Command("report"))
async def cmd_stat(message: types.Message, state: FSMContext):
    await message.answer(
        "Вот ваша статистика калорий и БЖУ за сегодня:\n",
    )
    user_data = await state.get_data()
    summ = user_data['summ']
    await message.answer("Количество ккал - " + str(user_data['cal']))
    await message.answer("\nПроцентное соотношение белка ко всей съеденной за сегодня пище составляет " + str(
        float(user_data['protein']) / summ * 100) + " процентов")
    await message.answer("\nПроцентное соотношение жиров ко всей съеденной за сегодня пище составляет " + str(
        float(user_data['fat']) / summ * 100) + " процентов")
    await message.answer("\nПроцентное соотношение углеводов ко всей съеденной за сегодня пище составляет " + str(
        float(user_data['carbohydrate']) / summ * 100) + " процентов")
    await state.clear()
    #await state.set_state(FSM.stat_entered)


@rt.message(FSM.enter_stat, F.text)
async def calc_cal(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state == FSM.enter_stat:
        txt = message.text
        flag = True
        lst = txt.split("\n")
        d = dict()
        cal = 0
        protein = 0
        fat = 0
        carbohydrate = 0
        summ = 0
        for st in lst:
            if not flag:
                break
            st = st.split("_")
            if len(st) != 2:
                flag = False
                break
            prod = st[0]
            weight = st[1]
            prod = prod.replace(" ", "")
            if ',' in weight:
                weight = weight.replace(',', '.')
                for c in weight:
                    if not ('0' <= c <= '9') and c != '.':
                        flag = False
                        break
            if not flag:
                break
            weight = float(weight)
            product = await orm_get_product(session, prod)
            cal += weight * float(product.kkal) / 100
            protein = weight * float(product.belok) / 100
            fat = weight * float(product.fat) / 100
            carbohydrate = weight * float(product.carbohydrate) /100
            summ = weight

        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            user_data = await state.get_data()
            if 'summ' in user_data:
                await state.update_data(summ=summ + user_data['summ'])
            else:
                await state.update_data(summ=summ)
            if 'cal' in user_data:
                await state.update_data(cal=cal + user_data['cal'])
            else:
                await state.update_data(cal=cal)
            if 'protein' in user_data:
                await state.update_data(protein=protein + user_data['protein'])
            else:
                await state.update_data(protein=protein)
            if 'fat' in user_data:
                await state.update_data(fat=fat + user_data['fat'])
            else:
                await state.update_data(fat=fat)
            if 'carbohydrate' in user_data:
                await state.update_data(carbohydrate=carbohydrate + user_data['carbohydrate'])
            else:
                await state.update_data(carbohydrate=carbohydrate)
            #await message.answer(str(user_data['summ']))
            #await state.set_data()
            #await state.clear()
            await message.answer("Данные приняты")


@rt.callback_query(StateFilter("*"), MenuCallBack.filter())
async def menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.target_state:
        await state.set_state(FSM.main__menu)
    #print(callback_data.level, callback_data.menu_name)
    '''if callback_data.level == 2:
        text = as_marked_section(
            Bold("Способы навалить кринжа"),
            "Сказать что-то кринжовое",
            "Сделать что-то кринжовое",
            marker="🙈"
        )
        await callback.answer(text.as_html())'''
    #print(1111, callback_data.level, callback_data.menu_name)
    media, reply_markup = await get_menu_content(level=callback_data.level, menu_name=callback_data.menu_name)
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()
    if callback_data.menu_name == "calculator":
        await state.set_state(FSM.target_state)


#func=lambda c: c.data == 'return'
@rt.callback_query(F.data.startswith('return'))
async def return_to_menu(callback: types.CallbackQuery):
    #print("callback")
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


@rt.message(FSM.target_state, F.text)
async def formula(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.target_state:
        txt = message.text
        txt = txt.strip().lower()
        if txt == "похудеть" or txt == "набрать вес" or txt == "поддерживать вес":
            flag = True
        else:
            flag = False

        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            await state.update_data(target=txt)
            await state.set_state(FSM.sex_state)
            await message.answer("Укажите свой пол(М или Ж)")


@rt.message(FSM.sex_state, F.text)
async def formula_2(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.sex_state:
        sex = message.text
        sex = sex.strip().upper()
        flag = True
        if sex != "М" and sex != "Ж" and sex != "M":
            flag = False
        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            await message.answer("Укажите свой возраст (количество полных лет)")
            await state.update_data(sex=sex)
            await state.set_state(FSM.age_state)


@rt.message(FSM.age_state, F.text)
async def formula_3(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.age_state:
        age = message.text
        age = age.strip()
        flag = True
        if not age.isdigit():
            flag = False
        else:
            age = int(age)
        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            await message.answer("Укажите свой вес (целым числом)")
            await state.update_data(age=age)
            await state.set_state(FSM.weight_state)


@rt.message(FSM.weight_state, F.text)
async def formula_4(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.weight_state:
        weight = message.text
        weight = weight.strip()
        flag = True
        if not weight.isdigit():
            flag = False
        else:
            weight = int(weight)
        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            await message.answer("Укажите свой рост (целым числом)")
            await state.update_data(weight=weight)
            await state.set_state(FSM.height_state)


@rt.message(FSM.height_state, F.text)
async def formula_5(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.height_state:
        height = message.text
        height = height.strip()
        flag = True
        if not height.isdigit():
            flag = False
        else:
            height = int(height)
        if not flag:
            await message.reply("Проверьте правильность введенных данных")
        else:
            await message.answer(
                text="Скажите, как бы вы оценили уровень своей физической активности. Нажмите на соответствующую кнопку ниже",
                reply_markup=koef_kb)
            #"Укажите коэффициент вашей физической активности (одним из пяти чисел, указанных ниже)\n\n(Коэффициент физической активности может принимать значения: 1.3(при минимальной физической активности), 1.5(при низкой физической активности), 1.75(при умеренной), 2.15(при высокой), 2.5(при экстремальной физической активности))")
            await state.update_data(height=height)
            await state.set_state(FSM.koef_state)

@rt.message(FSM.koef_state, F.text)
async def formula_6(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.koef_state:
        koef = message.text
        if koef == 'Минимальная':
            koef = 1.3
        elif koef == 'Низкая':
            koef = 1.5
        elif koef == 'Умеренная':
            koef = 1.75
        elif koef == 'Высокая':
            koef = 2.15
        else:
            koef = 2.5
        flag = True
        user_data = await state.get_data()
        target = str(user_data['target'])
        sex = str(user_data['sex'])
        age = int(user_data['age'])
        weight = int(user_data['weight'])
        height = int(user_data['height'])
        koef = float(koef)
        #print(target, sex, age, weight, height,koef)
        ans = "Ваша суточная норма калорий составляет "
        if sex == "M" or sex == "М":
            ans += str((5 + 10 * weight + 6.25 * height - 5 * age) * koef)
        else:
            ans += str((10 * weight + 6.25 * height - 5 * age - 161) * koef)
        ans += "\nДля оценки вашей суточной нормы была использована формула Миффлина - Сан Жеора\n"
        ans += "\n\nЧтобы выполнить поставленную задачу, для начала нужно взять силу в кулак и кулак в силу"
        if target == "похудеть":
            ans += " и понизить суточную норму на 300-500 калорий"
            ans += "\n\nРекомендуемое соотношение БЖУ: \nбелки - 20 %\nжиры - 30 %\nуглеводы - 50 %"
        elif target == "поддерживать вес":
            ans += " и придерживаться суточной нормы"
            ans += "\n\nРекомендуемое соотношение БЖУ: \nбелки - 15 %\nжиры - 30 %\nуглеводы - 55 %"
        else:
            ans += " и повысить суточную норму на 300-500 калорий"
            ans += "\n\nРекомендуемое соотношение БЖУ: \nбелки - 12 %\nжиры - 30 %\nуглеводы - 58 %"
        ans += "\n\nПосле каждого приема пищи присылайте граммовки съеденных продуктов и еды, я посчитаю потребленные вами за день калории и в конце дня скажу, получили ли вы необходимую суточную норму"
        ans += "\nДля этого воспользуйтесь специальной командой - enter_meal_statistics в меню слева снизу"
        ans += "\nКогда поймете, что сегодня больше не будете есть, и захотите узнать вашу статистику калорий и БЖУ за день, воспользуйтесь командой - report  в меню слева снизу"
        #await state.clear()
        await message.reply(ans, reply_markup=del_kb)
        await message.answer_photo(
                photo="https://media.istockphoto.com/id/945048938/ru/векторная/назад-стрелка-значок-специальная-фиолетовая-круглая-кнопка.jpg?s=612x612&w=0&k=20&c=95BOTDGGWYf7QQJAWPPJSF-J-sksNFku97AqpmFSx7Q=",
                reply_markup=get_callback_btns(btns={
                    'Вернуться в главное меню': 'return'
                })
            )






@rt.message(F.text == "15")
async def cringe1(message: types.Message, state: FSMContext):
    num = int(message.text)
    await state.update_data(number=num)
    '''async with state.storage as data:
        data['num'] = num'''
    await message.reply("Number is accepted")


@rt.message(F.text == "20")
async def cringe1(message: types.Message, state: FSMContext):
    '''async with state.storage as data:
        num = data['num']'''
    user_data = await state.get_data()
    num = user_data['number']
    await message.reply(str(num))


@rt.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    product = await orm_get_product(session, "свинина ")
    await message.answer(text=str(product.kkal))
    #await message.answer("ОК, вот список товаров ⏫")
