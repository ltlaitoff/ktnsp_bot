from aiogram import types
from aiogram.dispatcher.filters import Command
from config import dp
from controllers.week_schedule_controller import week_schedule_controller


@dp.message_handler(Command('week_schedule'))
async def week_schedule(message: types.Message):
    await message.answer(week_schedule_controller())
