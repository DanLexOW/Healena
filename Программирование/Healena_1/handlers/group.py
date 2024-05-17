from string import punctuation
from aiogram import F, types, Router
from aiogram.filters.command import Command
from filters.chat_types import ChatTypeFilter

rt_group = Router()
rt_group.message.filter(ChatTypeFilter(["group"]))

restricted_words = {"ой", "всё"}

def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))

@rt_group.message()
@rt_group.edited_message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.delete()
        #await message.chat.ban(message.from_user.id)