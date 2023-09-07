from aiogram import types
from aiogram.dispatcher.filters import Command
from datetime import datetime
import pandas
from config import dp, data, lesson_times
from helpers.get_week_number import get_week_number


@dp.message_handler(Command('daily_schedule'))
async def daily_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        await message.answer("Пар не має")
        return

    todays_schedule = data[data['day_of_the_week'] == week_day]
    is_even_week = get_week_number()
    schedule_text = f"Розклад на сьогодні ({'Знаменник' if is_even_week else 'Чисельник'}):\n"

    for _, row in todays_schedule.iterrows():
        time_start, time_end = lesson_times[row['period'] - 1]

        subject = row['subject']
        type_lesson = row['type_lesson']
        lesson_type = row['type']
        if pandas.notna(type_lesson) and pandas.notna(subject):
            if ('Ч' in lesson_type and is_even_week) or ('З' in lesson_type and not is_even_week):
                lesson_type_text = "Чисельник" if is_even_week else "Знаменник"
                schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
    await message.answer(schedule_text)
