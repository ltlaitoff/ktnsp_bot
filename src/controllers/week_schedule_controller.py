from config import DAY_NAMES, lesson_times
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_lesson_type_text import get_lesson_type_text
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def week_schedule_controller():
    week_day = get_current_week_day()

    if check_week_day_in_data(week_day):
        return 'Розклад на цей тиждень ще не встановлено.'

    week_text = f"Розклад на цей тиждень({get_lesson_type_text()}):\n\n"

    for day in range(1, 7):
        todays_schedule = get_todays_schedule_iterrows(week_day)
        text = f"{DAY_NAMES[day - 1]}:\n"

        for _, row in todays_schedule:
            time_start, time_end = lesson_times[row['period'] - 1]
            subject = row['subject']
            type_lesson = row['type_lesson']

            if (check_lesson_on_week_not_compatibility(
                row['type'],
                subject
            )):
                continue

            text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

        week_text += text + "\n"

    return week_text
