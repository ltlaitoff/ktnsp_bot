from datetime import datetime
from config import data, lesson_times
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_lesson_message_by_lesson import get_lesson_message_by_lesson
import pandas
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows
from helpers.check_is_even_week import check_is_even_week


def next_lesson_controller():
    now = datetime.now()
    week_day = get_current_week_day()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    is_even_week = check_is_even_week()

    if check_week_day_in_data(week_day):
        return

    todays_schedule = get_todays_schedule_iterrows(week_day)
    lesson = None

    for _, row in todays_schedule:
        if lesson is not None:
            break

        period = row['period']
        lesson_type = str(row['type'])

        time_start, time_end = lesson_times[period - 1]

        start_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_start.split(':')))
        end_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_end.split(':')))

        if (
            (not is_even_week and 'З' in lesson_type) or
            (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
            not pandas.notna(row["subject"])
        ):
            continue

        if lesson is None and (now >= start_datetime and now <= end_datetime or now <= start_datetime):
            lesson = row

    if lesson is not None and (not pandas.isna(lesson["subject"]) and lesson["subject"] != "Null"):
        text_for_send = get_lesson_message_by_lesson(
            time_start,
            time_end,
            lesson
        )

        return text_for_send

    return 'Сьогодні пар більше не має.'
