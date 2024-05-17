import logging

import letter

from handlers.messages import FSM
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
from datetime import datetime, time

from data_base.orm_query import orm_get_products, orm_get_product, orm_get_training, orm_get_uniducts
from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from handlers.menu_processing import get_menu_content
from keyboards import reply, inline
from keyboards.inline import MenuCallBack, get_callback_btns

rt_habits = Router()
rt_habits.message.filter(ChatTypeFilter(["private"]))




@rt_habits.callback_query(F.data.startswith('return'))
async def return_to_menu(callback: types.CallbackQuery):
    #print("callback")
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await callback.message.edit_media(media=media, reply_markup=reply.del_kb and reply_markup)
    await callback.answer()

'''reply_markup=reply.del_kb and get_callback_btns(btns={
            'Вернуться в главное меню': 'return'
        }'''


@rt_habits.message(F.text == "Никотиновая")
async def select_habits(message: types.Message, state: FSMContext):
    await message.answer("1) Бросить курить мгновенно практически невозможно, поэтому советую Вам выбрать определённый день X в календаре, когда Вы хотите отказаться от сигарет.\n2) Постепенно уменьшайте количество употребляемых сигарет на пути к дню X.\n3) Первое время после дня X сохраняйте привычки, которые сопровождали процесс курения. Например, выходите на свежий воздух во время перерыва, но не поддавайтесь соблазну покурить.\n4) Всё, что ассоциируется с курением, лучше убрать из зоны видимости, чтобы лишний раз не напоминать себе о сигаретах.\n5) Найдите кого-то (возможно, целую компанию), кто поддержит вашу инициативу и сохраняйте позитив, чтобы не думать о курении.\n6) Измените свой рацион. Добавьте в него больше молочных продуктов, а также витамины, минералы и клетчатку. Старайтесь не употреблять «тяжёлую пищу» и пейте больше воды. \n7)	Попробуйте занятия спортом. Если у Вас есть затруднения с выбором тренировок, я могу посоветовать Вам некоторые варианты, исходя из Ваших предпочтений.\n8)	Помочь бросить курить также могут жевательные резинки, пластыри и таблетки, однако перед их употреблением советую Вам посоветоваться с врачом.\n9)	Как утверждают специалисты, в среднем, тяга к курению проходит через 15-20 дней, поэтому всё в Ваших руках!", reply_markup=reply.del_kb)
    await message.answer_photo(
        photo="https://media.istockphoto.com/id/945048938/ru/векторная/назад-стрелка-значок-специальная-фиолетовая-круглая-кнопка.jpg?s=612x612&w=0&k=20&c=95BOTDGGWYf7QQJAWPPJSF-J-sksNFku97AqpmFSx7Q=",
        reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
    )
    #await message.answer(text="\n\nВот так!")
    await state.set_state(FSM.main__menu)


'''reply_markup=reply.del_kb and get_callback_btns(btns={
            'Вернуться в главное меню': 'return'
        })'''


@rt_habits.message(FSM.addiction, F.text == "Алкогольная")
async def select_habits(message: types.Message, state: FSMContext):
    await message.answer("1) Одной из главных ошибок при борьбе с алкоголизмом является постепенное «понижение градуса». В данном случае это не поможет, поэтому советую Вам отказаться от всего алкогольного насовсем, если Вы решили бросить пить.\n2)	По возможности откажитесь от посещения мест, где будет спиртное (клубы, бары и другие торжества). Если же отказ невозможен, во время мероприятия алкоголю нужно найти альтернативу (подойдут, например, сок или обычная вода).\n3)	Предупредите всех своих близких и знакомых о вашей цели. Попросите их лишний раз не напоминать Вам об алкоголе. \n4)	Все имеющиеся у Вас дома алкогольные напитки советуем отдать Вашим знакомым или просто выбросить.\n5)	Пейте больше воды и сократите употребление кофе и чая. Добавьте в рацион больше фруктов и овощей и избегайте солёную и острую пищу.\n6)	Для поддержания эмоционального фона найдите для себя новое хобби. Начните больше времени проводить на свежем воздухе и заниматься спортом. Если у Вас есть затруднения с выбором тренировок, я могу посоветовать Вам некоторые варианты, исходя из Ваших предпочтений.\n7)	Помните, что резкий отказ от спиртного может привести к сбою привычного ритма организма, что повлечёт за собой плохое самочувствие, перепады в настроении и другие негативные последствия. Если Вы не уверены в своих собственных силах, советую обратиться к врачу-специалисту. Он обязательно поможет и подберёт для Вас индивидуальный план по отказу от алкоголя.", reply_markup=reply.del_kb)
    await message.answer_photo(
        photo="https://media.istockphoto.com/id/945048938/ru/векторная/назад-стрелка-значок-специальная-фиолетовая-круглая-кнопка.jpg?s=612x612&w=0&k=20&c=95BOTDGGWYf7QQJAWPPJSF-J-sksNFku97AqpmFSx7Q=",
        reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
    )
    #await message.answer(text="\n\nВот так!")
    await state.set_state(FSM.main__menu)
