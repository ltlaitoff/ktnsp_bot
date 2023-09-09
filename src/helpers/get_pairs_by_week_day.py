import pandas
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from config import lesson_times
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def get_pairs_by_week_day(week_day, next=False):
    todays_schedule = get_todays_schedule_iterrows(week_day)
    text = ''

    for _, row in todays_schedule:
        type_lesson = row['type_lesson']
        time_start, time_end = lesson_times[row['period'] - 1]
        subject = row['subject']

        if pandas.isna(type_lesson):
            continue

        if (check_lesson_on_week_not_compatibility(
            row['type'],
            subject,
            next
        )):
            continue

        text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

    return text
