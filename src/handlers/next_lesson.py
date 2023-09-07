from aiogram import types
from aiogram.dispatcher.filters import Command
from config import dp
from controllers.next_lesson_controller import next_lesson_controller


@dp.message_handler(Command('nextlesson'))
async def next_lesson(message: types.Message):
    await message.answer(next_lesson_controller(), parse_mode='HTML', disable_web_page_preview=True)
