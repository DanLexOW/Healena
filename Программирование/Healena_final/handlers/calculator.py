import logging

from aiogram.enums import parse_mode, ParseMode

from keyboards.reply import koef_kb, del_kb, habits_kb

logger = logging.getLogger(__name__)


from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.orm_query import orm_get_products, orm_get_product, orm_get_uniducts, orm_add_id, \
    orm_get_ids, orm_update_id, orm_get_id
from filters.chat_types import ChatTypeFilter


from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack, get_callback_btns


rt = Router()
rt.message.filter(ChatTypeFilter(["private"]))


class FSM(StatesGroup):
    main__menu = State()
    target_state = State()
    sex_state = State()
    age_state = State()
    weight_state = State()
    height_state = State()
    koef_state = State()
    enter_stat = State()
    stat_entered = State()
    addiction = State()
    sexxx_state = State()
    common_muscle_group_state = State()
    achieve_goal_state = State()
    detailed_muscle_state = State()


@rt.message(CommandStart())
async def start_cmd(message: types.Message):
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await message.answer("Добро пожаловать!")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@rt.message(Command("menu"))
async def menu_cmd(message: types.Message):
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@rt.message(StateFilter("*"), Command("finish_stat"))
async def finish_report(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(send="Нет")
    await state.update_data(calc_data="ничего пока нет")
    data = await state.get_data()
    calc_data = ""
    flag_id = False
    for i in await orm_get_ids(session):
        if i.user_id == message.from_user.id:
            flag_id = True
    if flag_id:
        obj = await orm_get_id(session, message.from_user.id)
        calc_data = obj.calc_data
        await state.update_data(calc_data=calc_data)
    else:
        await state.update_data(calc_data="ничего пока нет")
    data = await state.get_data()
    if not flag_id:
        await orm_add_id(session, data)
    else:
        await orm_update_id(session, message.from_user.id, data)
    await message.answer("Хорошо, больше не буду присылать ежедневные калорийные статистики")


@rt.message(StateFilter("*"), Command("enter_meal_statistics"))
async def cmd_stat(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите одним сообщением список продуктов, входящих в ваш последний прием пищи, в формате\n\nКатегория продукта_Продукт_его масса(в граммах числом)\nКатегория второго продукта_Второй продукт_его масса\n(и так далее)\nПример: фрукты_яблоки_200",
    )
    await message.answer("\n\nмясо\nрыба\nптица\nколбаса\nсосиски\nикра\nморепродукты\nгрибы\nяйца\nмасло\nмолочные продукты\nсыр\nкрупа\nхлебобулочные изделия\nовощи\nфрукты\nягоды\nорехи\nсухофрукты\nвыпечка\nсладости\nнапитки безалкогольные\nнапитки алкогольные\n\n")
    await message.answer("Для каждого записанного продукта выберите одну из категорий продуктов в сообщении выше")
    await state.set_state(FSM.enter_stat)


@rt.message(StateFilter("*"), Command("report"))
async def cmd_stat(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if 'summ' in user_data:
        ans = ""
        ans += "Вот ваша статистика калорий и БЖУ за сегодня:\n"
        summ = user_data['summ']
        ans += "Ккал: " + str(user_data['cal'])
        ans += "\nБелки " + str(int(
        float(user_data['protein']) / summ * 100)) + " %"
        ans += "\nЖиры: " + str(int(
            float(user_data['fat']) / summ * 100)) + " %"
        ans += "\n Углеводы: " + str(int(
            float(user_data['carbohydrate']) / summ * 100)) + " %"
        await message.answer(ans)
    else:
        await message.answer("Похоже сегодня вы ничего не ели. Возвращайтесь, когда подкрепитесь")


@rt.message(FSM.enter_stat, F.text)
async def calc_cal(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state == FSM.enter_stat:
        txt = message.text
        flag = True
        flag_presence = False
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
            if len(st) != 3:
                flag = False
                break
            cat = st[0].strip()
            prod = st[1].strip()
            weight = st[2].strip()
            if ',' in weight:
                weight = weight.replace(',', '.')
                for c in weight:
                    if not ('0' <= c <= '9') and c != '.':
                        flag = False
                        break
            flag_cat = False
            if not flag:
                break
            weight = float(weight)
            for produc in await orm_get_products(session):
                if produc.name == prod:
                    flag_presence = True
                if produc.category == cat:
                    flag_cat = True
            if not flag_cat:
                flag = False
            if flag_presence:
                product = await orm_get_product(session, prod)
                cal += weight * float(product.kkal) / 100
                protein = weight * float(product.belok) / 100
                fat = weight * float(product.fat) / 100
                carbohydrate = weight * float(product.carbohydrate) /100
                summ = weight
            elif (not flag_presence) and flag:
                await message.reply("Похоже, что продукта " + prod + " нет в нашей базе данных или вы написали его название с ошибками\n\nПроверьте написание. \nЕсли вы все же написали правильно, попробуйте вместо него написать один из указанных ниже продуктов, наиболее близкий к вашему\n\n")
                st = ""
                if cat == "рыба" or cat == "колбаса" or cat == "сосиски" or cat == "молочные продукты" or cat == "овощи" or cat == "фрукты":
                    for uniduct in await orm_get_uniducts(session):
                        if cat == uniduct.category:
                            st += (str(uniduct.name) + "\n")
                else:
                    for produ in await orm_get_products(session):
                        if cat == produ.category:
                            st += (str(produ.name) + "\n")
                await message.answer(st + "\n")
        if not flag:
            await message.reply("Проверьте правильность введенных данных, а также, что введенная вами категория "
                                "продуктов есть в списке категорий в сообщении выше")
        else:
            if flag_presence:
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
                user_data = await state.get_data()
                calc_data_hand = str(user_data['summ']) + " " + str(user_data['cal']) + " " + str(user_data['protein']) + " " + str(user_data['fat']) + " " + str(user_data['carbohydrate'])
                await state.update_data(user_id=message.from_user.id)
                await state.update_data(send="Да")
                await state.update_data(calc_data=calc_data_hand)
                data = await state.get_data()
                flag_id = False
                for i in await orm_get_ids(session):
                    if str(i.user_id) == str(message.from_user.id):
                        flag_id = True
                obj = await orm_get_id(session, message.from_user.id)
                if flag_id and obj.calc_data != "ничего пока нет":
                    obj = await orm_get_id(session, message.from_user.id)
                    calc_data_state = str(obj.calc_data).split()
                    summ_state = calc_data_state[0]
                    cal_state = calc_data_state[1]
                    protein_state = calc_data_state[2]
                    fat_state = calc_data_state[3]
                    carbohydrate_state = calc_data_state[4]
                    calc_data = str(float(summ_state) + user_data['summ']) + " " + str(float(cal_state) + user_data['cal']) + " " + str(float(protein_state) + user_data['protein']) + " " + str(float(fat_state) + user_data['fat']) + " " + str(float(carbohydrate_state) + user_data['carbohydrate'])
                    await state.update_data(calc_data=calc_data)
                else:
                    await state.update_data(calc_data=calc_data_hand)
                data = await state.get_data()
                if not flag_id:
                    await orm_add_id(session, data)
                else:
                    await orm_update_id(session, message.from_user.id, data)

                await message.answer("Данные приняты")


@rt.callback_query(StateFilter("*"), MenuCallBack.filter())
async def menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.target_state:
        await state.set_state(FSM.main__menu)
    media, reply_markup = await get_menu_content(level=callback_data.level, menu_name=callback_data.menu_name)
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    if callback_data.level == 1 and callback_data.menu_name == "habits":
        await callback.message.answer(text="🍾/🚬", reply_markup=habits_kb)
        await state.set_state(FSM.addiction)
    await callback.answer()
    if callback_data.menu_name == "calculator":
        await state.set_state(FSM.target_state)
    if callback_data.menu_name == "about":
        await callback.message.answer(
            text="        <b>Healena</b> – это Telegram-бот, созданный, чтобы мотивировать пользователей "
                 "самого популярного мессенджера вести здоровый образ жизни. \n       Если Вы "
                 "хотите начать заботиться о своём здоровье, но испытываете трудности с "
                 "подбором питания или спортивных тренировок, Healena – та, кто может Вам "
                 "помочь. \n \n Над проектом работали студенты-лингвисты НИУ ВШЭ: \n• <b>Марьин "
                 "Даниил</b> (@CrAzY_PiZzAaA) \n• <b>Кукушкина Ольга</b> (@olyonka_777) \n• <b>Данченко "
                 "Алексей</b> (@msby_DanLex)  \n• <b>Герасимова Екатерина</b> (@Pomidorchik_Rina)  "
                 "\n\n        Если Вы испытываете трудности с ботом, нашли какой-то баг или хотите "
                 "предложить, как усовершенствовать Healen’у, можете в любое время написать "
                 "любому из 4 участников проекта. Обещаем ответить Вам в кратчайшие сроки ("
                 "если наш любимый университет не завалит нас дедлайнами ещё больше)! "
                 "\n\n  <b>Приятного пользования! Будьте здоровы!</b>💜", parse_mode=ParseMode.HTML)
        await callback.message.answer_photo(
            photo="https://media1.thehungryjpeg.com/thumbs2/ori_4028488_mubyalpxa3p46fynmhtf2tv0mycfydihik3339el_neon-arrow-realistic-glowing-yellow-sign-abstract-electricity-colore.jpg",
            reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
        )
    if callback_data.menu_name == "train":
        await state.set_state(FSM.sexxx_state)


@rt.callback_query(F.data.startswith('return'))
async def return_to_menu(callback: types.CallbackQuery):
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
            await state.update_data(height=height)
            await state.set_state(FSM.koef_state)


@rt.message(FSM.koef_state, F.text)
async def formula_6(message: types.Message, state: FSMContext, session: AsyncSession):
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
        ans = "Ваша суточная норма калорий составляет "
        if sex == "M" or sex == "М":
            ans += str(int((5 + 10 * weight + 6.25 * height - 5 * age) * koef))
        else:
            ans += str(int((10 * weight + 6.25 * height - 5 * age - 161) * koef))
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
        ans += "\n\nВ начале нового дня (в 00:00) я буду присылать вам статистику за прошедший день. Если пожелаете прекратить отправку регулярных статистик, воспользуйтесь командой finish_stat в меню слева внизу"
        ans += "\n\n ❗️При этом помните, что при каждом повторном прохождении опроса внутри вкладки Калькулятор калорий и выводе рекомендаций по калориям и БЖУ (которые выше) регулярная отправка калорийной статистики возобновляется ❗️"
        await state.update_data(user_id=message.from_user.id)
        await state.update_data(send="Да")
        await state.update_data(calc_data="ничего пока нет")
        data = await state.get_data()
        calc_data = ""
        flag_id = False
        for i in await orm_get_ids(session):
            if i.user_id == message.from_user.id:
                flag_id = True
        if flag_id:
            user_data = await state.get_data()
            obj = await orm_get_id(session, message.from_user.id)
            if obj.calc_data != "ничего пока нет":
                calc_data_state = obj.calc_data.split()
                summ_state = calc_data_state[0]
                cal_state = calc_data_state[1]
                protein_state = calc_data_state[2]
                fat_state = calc_data_state[3]
                carbohydrate_state = calc_data_state[4]
                calc_data = str(float(summ_state) + user_data['summ']) + " " + str(
                    float(cal_state) + user_data['cal']) + " " + str(float(protein_state) + user_data['protein']) + " " + str(
                    float(fat_state) + user_data['fat']) + " " + str(float(carbohydrate_state) + user_data['carbohydrate'])
        else:
            await state.update_data(calc_data="ничего пока нет")
        data = await state.get_data()
        if not flag_id:
            await orm_add_id(session, data)
        else:
            await orm_update_id(session, message.from_user.id, data)
        await message.reply(ans, reply_markup=del_kb)
        photo = "https://media1.thehungryjpeg.com/thumbs2/ori_4028488_mubyalpxa3p46fynmhtf2tv0mycfydihik3339el_neon-arrow-realistic-glowing-yellow-sign-abstract-electricity-colore.jpg"
        await message.answer_photo(
                photo=photo,
                reply_markup=get_callback_btns(btns={
                    'Вернуться в главное меню': 'return'
                })
            )
