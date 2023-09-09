from aiogram import types
from aiogram.dispatcher.filters import Command
from config import dp
from controllers.next_week_schedule_controller import next_week_schedule_controller


@dp.message_handler(Command('next_week_schedule'))
async def week_schedule(message: types.Message):
    await message.answer(next_week_schedule_controller())
