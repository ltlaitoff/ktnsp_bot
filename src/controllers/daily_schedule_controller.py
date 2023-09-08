import pandas
from config import lesson_times
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows
from helpers.check_is_even_week import check_is_even_week


def daily_schedule_controller():
    week_day = get_current_week_day()

    if check_week_day_in_data(week_day):
        return "Пар немає"

    todays_schedule = get_todays_schedule_iterrows(week_day)
    is_even_week = check_is_even_week()

    text = f"Розклад на сьогодні ({'Знаменник' if is_even_week else 'Чисельник'}):\n"

    for _, row in todays_schedule:
        time_start, time_end = lesson_times[row['period'] - 1]

        subject = row['subject']
        type_lesson = row['type_lesson']
        lesson_type = row['type']

        if pandas.na(type_lesson):
            continue

        if (check_lesson_on_week_not_compatibility(
            is_even_week,
            lesson_type,
            subject
        )):
            continue

        text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

    return text
