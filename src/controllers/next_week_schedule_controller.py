from config import DAY_NAMES
from helpers.get_lesson_type_text import get_lesson_type_text
from helpers.get_pairs_by_week_day import get_pairs_by_week_day


def next_week_schedule_controller():
    week_text = f"Розклад на наступний тиждень({get_lesson_type_text(True)}):\n\n"

    for day in range(1, 7):
        week_text += DAY_NAMES[day - 1] + ":\n" + \
            get_pairs_by_week_day(day, True) + "\n"

    return week_text
