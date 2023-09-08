import pandas
from config import lesson_times
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_lesson_type_text import get_lesson_type_text
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def daily_schedule_controller():
    week_day = get_current_week_day()

    if check_week_day_in_data(week_day):
        return "Пар немає"

    todays_schedule = get_todays_schedule_iterrows(week_day)
    text = f"Розклад на сьогодні ({get_lesson_type_text()}):\n"

    for _, row in todays_schedule:
        type_lesson = row['type_lesson']

        if pandas.isna(type_lesson):
            continue

        subject = row['subject']

        if (check_lesson_on_week_not_compatibility(
            row['type'],
            subject
        )):
            continue

        time_start, time_end = lesson_times[row['period'] - 1]

        text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

    return text
