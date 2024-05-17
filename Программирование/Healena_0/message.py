from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.filters.command import Command
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold

rt = Router()
rt.message.filter(ChatTypeFilter(["private"]))

from keyboards import reply

''''@rt.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=reply.start_kb)'''

@rt.message(or_f(Command("menu"), F.text.lower() == "меню"))
async def cmd_menu(message: types.Message):
    await message.reply("Вот меню", reply_markup=reply.del_kb)

@rt.message(Command("music"))
async def cmd_music(message: types.Message):
    await message.reply("Вот музыка", reply_markup=reply.start_kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Что вас интересует?"
    ))

@rt.message(F.text.lower().contains('кто'))
async def cmd_music(message: types.Message):
    await message.reply("Это магический фильтр", inline_markup=reply.inline_kb)

@rt.message(F.text.lower().contains('рамм'))
async def cmd_music(message: types.Message):
    await message.reply("Вот вам ссылка на кринж, ловити и сосити: https://youtu.be/sqBtdEsP3Uw?si=4VX0doSVSiGDWPI6")

@rt.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))

@rt.message(F.location)
async def get_contact(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))

@rt.message(F.text.lower() == "варианты навалить кринжа")
@rt.message(Command("Кнопка4"))
async def cringe_ways(message: types.Message):
    text = as_marked_section(
        Bold("Способы навалить кринжа"),
        "Сказать что-то кринжовое",
        "Сделать что-то кринжовое",
        marker="🙈"
    )
    await message.answer(text.as_html())


@rt.message(or_f(Command("mood"), F.text.lower() == "Хочешь узнать какое у меня настроение?"))
async def cmd_menu(message: types.Message):
    await message.reply("Вот ", reply_markup=reply.start_kb2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Что вас интересует?"
    ))

