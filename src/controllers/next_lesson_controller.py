from datetime import datetime
from config import lesson_times
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.check_week_day_in_data import check_week_day_in_data
from helpers.get_current_week_day import get_current_week_day
from helpers.get_lesson_message_by_lesson import get_lesson_message_by_lesson
import pandas
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def next_lesson_controller():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    week_day = get_current_week_day()
    pair_now = False

    if check_week_day_in_data(week_day):
        return 'Сьогодні неділя! Пар нема! 🏳️‍🌈'

    todays_schedule = get_todays_schedule_iterrows(week_day)
    lesson = None

    for _, row in todays_schedule:
        if lesson is not None:
            break

        period = row['period']
        lesson_type = row['type']

        if (check_lesson_on_week_not_compatibility(
            lesson_type,
            row['subject']
        )):
            continue

        time_start, time_end = lesson_times[period - 1]

        start_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_start.split(':')))
        end_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_end.split(':')))

        if now >= start_datetime and now <= end_datetime:
            pair_now = True
            lesson = row

        if now <= start_datetime:
            lesson = row

    if lesson is not None and pandas.notna(lesson["subject"]):
        text_for_send = get_lesson_message_by_lesson(
            time_start,
            time_end,
            lesson,
            '<u><b>Зараз пара</b></u>' if pair_now else 'Наступна пара',
        )

        return text_for_send

    return 'Сьогодні пар більше немає.'
