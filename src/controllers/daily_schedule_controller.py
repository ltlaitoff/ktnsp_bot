from datetime import datetime
import pandas
from config import data, lesson_times
from helpers.get_week_number import get_week_number

def daily_schedule_controller():
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        return "Пар не має"

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
                schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
    return schedule_text
