from datetime import datetime
from config import DAY_NAMES, data, lesson_times
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.check_is_even_week import check_is_even_week


def week_schedule_controller():
    week_day = get_current_week_day()

    if check_week_day_in_data(week_day):
        return 'Розклад на цей тиждень ще не встановлено.'

    is_even_week = check_is_even_week()
    week_text = f"Розклад на цей тиждень({'Знаменник' if is_even_week else 'Чисельник'}):\n\n"

    for day in range(1, 7):
        todays_schedule = data[data['day_of_the_week'] == day]
        text = f"{DAY_NAMES[day - 1]}:\n"

        for _, row in todays_schedule.iterrows():
            time_start, time_end = lesson_times[row['period'] - 1]
            subject = row['subject']
            lesson_type = row['type']
            type_lesson = row['type_lesson']

            if (check_lesson_on_week_not_compatibility(
                is_even_week,
                lesson_type,
                subject
            )):
                continue

            text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

        week_text += text + "\n"

    return week_text
