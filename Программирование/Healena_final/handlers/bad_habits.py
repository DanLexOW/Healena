import logging

from handlers.calculator import FSM

logger = logging.getLogger(__name__)


from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter

from handlers.menu_processing import get_menu_content
from keyboards import reply, inline
from keyboards.inline import MenuCallBack, get_callback_btns

from aiogram.enums import ParseMode

rt_habits = Router()
rt_habits.message.filter(ChatTypeFilter(["private"]))


@rt_habits.callback_query(F.data.startswith('return'))
async def return_to_menu(callback: types.CallbackQuery):
    media, reply_markup = await get_menu_content(level=0, menu_name="main")
    await callback.message.edit_media(media=media, reply_markup=reply.del_kb and reply_markup)
    await callback.answer()


@rt_habits.message(F.text == "Никотиновая")
async def select_habits(message: types.Message, state: FSMContext):
    await message.answer(
        "1) Бросить курить мгновенно практически невозможно, поэтому советую Вам выбрать определённый <b>день X</b> в календаре, когда Вы хотите отказаться от сигарет.\n2) <b>Постепенно уменьшайте</b> количество употребляемых сигарет на пути к дню X.\n3) Первое время после дня X <b>сохраняйте привычки</b>, которые сопровождали процесс курения. Например, выходите на свежий воздух во время перерыва, но не поддавайтесь соблазну покурить.\n4) Всё, что ассоциируется с курением, лучше <b>убрать из зоны видимости</b>, чтобы лишний раз не напоминать себе о сигаретах.\n5) Найдите кого-то (возможно, целую компанию), <b>кто поддержит вашу инициативу</b> и сохраняйте <b>позитив</b>, чтобы не думать о курении.\n6) <b>Измените свой рацион</b>. Добавьте в него больше молочных продуктов, а также витамины, минералы и клетчатку. Старайтесь не употреблять «тяжёлую пищу» и пейте больше воды. \n7)	Попробуйте <b>занятия спортом</b>. Если у Вас есть затруднения с выбором тренировок, я могу посоветовать Вам некоторые варианты, исходя из Ваших предпочтений.\n8)	Помочь бросить курить также могут <b>жевательные резинки</b>, пластыри и таблетки, однако перед их употреблением советую Вам посоветоваться с врачом.\n9)	Как утверждают специалисты, в среднем, тяга к курению проходит через 15-20 дней, поэтому <b>всё в Ваших руках!</b>",
        parse_mode=ParseMode.HTML, reply_markup=reply.del_kb)

    await message.answer_photo(
        photo="https://media1.thehungryjpeg.com/thumbs2/ori_4028488_mubyalpxa3p46fynmhtf2tv0mycfydihik3339el_neon-arrow-realistic-glowing-yellow-sign-abstract-electricity-colore.jpg",
        reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
    )
    await state.set_state(FSM.main__menu)


@rt_habits.message(FSM.addiction, F.text == "Алкогольная")
async def select_habits(message: types.Message, state: FSMContext):
    await message.answer(
        "1) Одной из главных ошибок при борьбе с алкоголизмом является постепенное «понижение градуса». В данном случае это не поможет, поэтому советую Вам <b>отказаться от всего алкогольного насовсем</b>, если Вы решили бросить пить.\n2)	По возможности откажитесь от посещения мест, где будет спиртное (клубы, бары и другие торжества). Если же отказ невозможен, во время мероприятия алкоголю нужно <b>найти альтернативу</b> (подойдут, например, сок или обычная вода).\n3)	Предупредите всех своих близких и знакомых о вашей цели. Попросите их лишний раз не напоминать Вам об алкоголе. \n4)	Все <b>имеющиеся у Вас дома алкогольные напитки</b> советуем отдать Вашим знакомым или просто <b>выбросить</b>.\n5)	Пейте <b>больше воды</b> и сократите употребление кофе и чая. Добавьте в рацион <b>больше фруктов и овощей</b> и избегайте солёную и острую пищу.\n6)	Для поддержания эмоционального фона найдите для себя <b>новое хобби</b>. Начните больше времени проводить на свежем воздухе и заниматься спортом. Если у Вас есть затруднения с выбором тренировок, я могу посоветовать Вам некоторые варианты, исходя из Ваших предпочтений.😉\n7)	Помните, что резкий отказ от спиртного может привести к сбою привычного ритма организма, что повлечёт за собой плохое самочувствие, перепады в настроении и другие негативные последствия. Если Вы не уверены в своих собственных силах, советую <b>обратиться к врачу-специалисту</b>. Он обязательно поможет и подберёт для Вас индивидуальный план по отказу от алкоголя.",
        parse_mode=ParseMode.HTML, reply_markup=reply.del_kb)

    await message.answer_photo(
        photo="https://media1.thehungryjpeg.com/thumbs2/ori_4028488_mubyalpxa3p46fynmhtf2tv0mycfydihik3339el_neon-arrow-realistic-glowing-yellow-sign-abstract-electricity-colore.jpg",
        reply_markup=get_callback_btns(btns={'Вернуться в главное меню': 'return'})
    )
    await state.set_state(FSM.main__menu)
