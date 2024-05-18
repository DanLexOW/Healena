import logging

logger = logging.getLogger(__name__)

from aiogram import F, types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.orm_query import orm_get_trainings
from filters.chat_types import ChatTypeFilter

from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack, get_callback_btns

rt_train = Router()
rt_train.message.filter(ChatTypeFilter(["private"]))


class FSM(StatesGroup):
    main__menu = State()
    sexxx_state = State()
    common_muscle_group_state = State()
    achieve_goal_state = State()
    detailed_muscle_state = State()


@rt_train.callback_query(F.data.startswith('return'))
async def return_to_menu(callback: types.CallbackQuery):
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


@rt_train.callback_query(StateFilter("*"), MenuCallBack.filter())
async def menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.sexxx_state:
        await state.set_state(FSM.main__menu)
    media, reply_markup = await get_menu_content(level=callback_data.level, menu_name=callback_data.menu_name)
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()
    if callback_data.menu_name == "train":
        await state.set_state(FSM.sexxx_state)


@rt_train.message(FSM.sexxx_state, F.text)
async def stage_1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.sexxx_state:
        sexxx = message.text
        sexxx = sexxx.strip().upper()
        flag = True
        if sexxx != "М" and sexxx != "Ж" and sexxx != "M":
            flag = False
        if not flag:
            await message.reply("Проверьте правильность введённых данных")
        else:
            await message.answer("Какие группы мышц вы хотите тренировать?\n\nВерхние\nНижние\nНа всё тело")
            if sexxx == "M" or sexxx == "М":
                await state.update_data(sexxx="М")
            if sexxx == "Ж":
                await state.update_data(sexxx="Ж")
            await state.set_state(FSM.common_muscle_group_state)


@rt_train.message(FSM.common_muscle_group_state, F.text)
async def stage_2(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.common_muscle_group_state:
        muscle = message.text
        muscle = muscle.strip().lower()
        if muscle == "верхние" or muscle == "нижние" or muscle == "на всё тело":
            flag = True
        else:
            flag = False
        if not flag:
            await message.reply("Проверьте правильность введённых данных")
        else:
            if muscle == "верхние":
                await state.update_data(muscl="Upper")
            if muscle == "нижние":
                await state.update_data(muscl="Lower")
            if muscle == "на всё тело":
                await state.update_data(muscl="Full")
            await state.set_state(FSM.detailed_muscle_state)
            st = "Выберите и напишите из списка ниже, что хотите прокачать. Ответ мозг не принимается"
            if muscle == "верхние":
                st += "\n\nкор\nруки\nгрудь\nпресс"
            elif muscle == "нижние":
                st += "\n\nноги\nкор\n"
            else:
                st += "\n\nкардио\nсила\nпилатес\nйога"
            await message.answer(st)


@rt_train.message(FSM.detailed_muscle_state, F.text)
async def stage_3(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSM.detailed_muscle_state:
        musc = message.text
        musc = musc.strip().lower()
        flag = True
        for muscl in musc.split():
            if not(muscl == "кардио" or muscl == "сила" or muscl == "пилатес" or muscl == "йога" or muscl == "ноги" or muscl == "кор" or muscl == "руки" or muscl == "грудь" or muscl == "пресс"):
                flag = False

        if not flag:
            await message.reply("Проверьте правильность введённых данных")
        else:
            ans = ""
            muscl = musc
            if muscl == "кардио":
                ans = "cardio"
            elif muscl == "сила":
                ans = "strength"
            elif muscl == "пилатес":
                ans = "pilates"
            elif muscl == "йога":
                ans = "yoga"
            elif muscl == "ноги":
                ans = "legs"
            elif muscl == "руки":
                ans = "arms"
            elif muscl == "кор":
                ans = "core"
            elif muscl == "грудь":
                ans = "chest"
            elif muscl == "пресс":
                ans = "abs"
            await state.update_data(detail_goal=ans)
            await state.set_state(FSM.achieve_goal_state)
            await message.answer(
                "Укажите свою первостепенную цель (так, как указано здесь): \n\nпохудеть\nнабрать вес\nподдерживать вес\nвзбодриться")


@rt_train.message(FSM.achieve_goal_state, F.text)
async def stage_4(message: types.Message, state: FSMContext,  session: AsyncSession):
    current_state = await state.get_state()
    flag_print = False
    k = 0
    if current_state == FSM.achieve_goal_state:
        goal = message.text
        goal = goal.strip().lower()
        if goal == "похудеть" or goal == "набрать вес" or goal == "поддерживать вес" or goal == "взбодриться":
            flag = True
        else:
            flag = False
        if not flag:
            await message.reply("Проверьте правильность введённых данных")
        else:
            await state.update_data(goal=goal)
            if goal == "похудеть":
                await state.update_data(goal="weight_loss")
            if goal == "набрать вес":
                await state.update_data(goal="weight_gain")
            if goal == "поддерживать вес":
                await state.update_data(goal="keep_shape")
            if goal == "взбодриться":
                await state.update_data(goal="energy_feelins")
            parametrs = await state.get_data()
            for training in await orm_get_trainings(session):
                flag = True
                flag_goal = False
                if not (training.sex == parametrs['sexxx'] and training.common_muscle_group == parametrs['muscl']):
                    flag = False
                if parametrs['goal'] == training.weight_loss and (training.weight_loss == 'High' or training.weight_loss == 'Mid'):
                    flag_goal = True
                if parametrs['goal'] == training.weight_gain and (training.weight_gain == 'High' or training.weight_gain == 'Mid'):
                    flag_goal = True
                if parametrs['goal'] == training.keep_shape and (training.keep_shape == 'High' or training.keep_shape == 'Mid'):
                    flag_goal = True
                if parametrs['goal'] == training.energy_feelins and (training.energy_feelins == 'High' or training.energy_feelins == 'Mid'):
                    flag_goal = True
                flag_detailed = False
                for muscle in training.detailed_muscle_group.split():
                    if muscle == parametrs['detail_goal']:
                        flag_detailed = True
                if flag and flag_detailed:
                    await message.answer(str(training.link))
                    k += 1
                    flag_print = True
            if not flag_print:
                for training in await orm_get_trainings(session):
                    flag = True
                    flag_goal = False
                    if not training.common_muscle_group == parametrs['muscl']:
                        flag = False
                    if parametrs['goal'] == training.weight_loss and (
                            training.weight_loss == 'High' or training.weight_loss == 'Mid'):
                        flag_goal = True
                    if parametrs['goal'] == training.weight_gain and (
                            training.weight_gain == 'High' or training.weight_gain == 'Mid'):
                        flag_goal = True
                    if parametrs['goal'] == training.keep_shape and (
                            training.keep_shape == 'High' or training.keep_shape == 'Mid'):
                        flag_goal = True
                    if parametrs['goal'] == training.energy_feelins and (
                            training.energy_feelins == 'High' or training.energy_feelins == 'Mid'):
                        flag_goal = True
                    flag_detailed = False
                    for muscle in training.detailed_muscle_group.split():
                        if muscle == parametrs['detail_goal']:
                            flag_detailed = True
                    if flag and flag_detailed:
                        await message.answer(str(training.link))
                        flag_print = True
                        k += 1
        if flag_print:
            await message.answer(text="Тренировки взяты с каналов Nike Training и Jordan Yeoh Fitness")

    if not flag_print:
        await message.answer("Извините, я не нашла подходящую тренировку")

    await message.answer_photo(
        photo="https://media1.thehungryjpeg.com/thumbs2/ori_4028488_mubyalpxa3p46fynmhtf2tv0mycfydihik3339el_neon-arrow-realistic-glowing-yellow-sign-abstract-electricity-colore.jpg"
              "/векторная/назад-стрелка-значок-специальная-фиолетовая-круглая-кнопка.jpg?s=612x612&w=0&k=20&c"
              "=95BOTDGGWYf7QQJAWPPJSF-J-sksNFku97AqpmFSx7Q=",
        reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
    )
