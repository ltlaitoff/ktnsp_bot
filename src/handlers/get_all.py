from aiogram import types
from aiogram.dispatcher.filters import Command
from config import dp
from controllers.get_all_controller import get_all_controller


@dp.message_handler(Command('get_all'))
async def get_all(message: types.Message):
    await message.answer(get_all_controller(), parse_mode='HTML', disable_web_page_preview=True)
