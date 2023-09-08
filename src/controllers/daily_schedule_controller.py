from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_lesson_type_text import get_lesson_type_text
from helpers.get_pairs_by_week_day import get_pairs_by_week_day


def daily_schedule_controller():
    week_day = get_current_week_day()

    if check_week_day_in_data(week_day):
        return "Пар немає"

    return f"Розклад на сьогодні ({get_lesson_type_text()}):\n" + \
        get_pairs_by_week_day(week_day)
