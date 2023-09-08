from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from config import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    text = 'Привіт! Я бот групи КНТ-113сп для розкладу занять\n' + \
        'Переглянути всі команди: /help'

    await message.answer(text)


@dp.message_handler(CommandHelp())
async def help(message: types.Message):
    text = 'Всі команди:\n' + \
        '/next_lesson - Наступна пара\n' + \
        '/daily_schedule - Всі пари на день\n' + \
        '/week_schedule - Всі пари на тиждень\n'

    await message.answer(text)
