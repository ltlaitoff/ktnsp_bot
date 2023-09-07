from datetime import datetime
from aiogram import types
from aiogram.dispatcher.filters import Command
import pandas
from config import DAY_NAMES, dp, data, lesson_times
from helpers.get_week_number import get_week_number


@dp.message_handler(Command('week_schedule'))
async def week_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        await message.answer('Розклад на цей тиждень ще не встановлено.')
        return

    is_even_week = get_week_number()
    week_text = f"Розклад на цей тиждень({'Знаменник' if is_even_week else 'Чисельник'}):\n\n"

    for day in range(1, 7):
        todays_schedule = data[data['day_of_the_week'] == day]
        text = f"{DAY_NAMES[day - 1]}:\n"
        for _, row in todays_schedule.iterrows():
            time_start, time_end = lesson_times[row['period'] - 1]
            subject = row['subject']
            lesson_type = row['type']
            type_lesson = row['type_lesson']
            if (
                (not is_even_week and 'З' in lesson_type) or
                (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
                not pandas.notna(subject)
            ):
                continue
            text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
        week_text += text + "\n"
    await message.answer(week_text)
