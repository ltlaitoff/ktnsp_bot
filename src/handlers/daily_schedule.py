from aiogram import types
from aiogram.dispatcher.filters import Command
from config import dp
from controllers.daily_schedule_controller import daily_schedule_controller


@dp.message_handler(Command('daily_schedule'))
async def daily_schedule(message: types.Message):
    await message.answer(daily_schedule_controller(), parse_mode='HTML', disable_web_page_preview=True)


@dp.message_handler(Command('daily_schedule_detailed'))
async def daily_schedule(message: types.Message):
    await message.answer(daily_schedule_controller(detailed=True), parse_mode='HTML', disable_web_page_preview=True)
