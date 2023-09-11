import pandas
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from config import lesson_times
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def get_pairs_by_week_day(week_day, next=False):
    todays_schedule = get_todays_schedule_iterrows(week_day)
    text = ''

    for _, row in todays_schedule:
        type_lesson = row['type_lesson']
        period = row['period']
        time_start, time_end = lesson_times[period - 1]
        subject = row['subject']

        if pandas.isna(type_lesson):
            continue

        if (check_lesson_on_week_not_compatibility(
            row['type'],
            subject,
            next
        )):
            continue 

        "🐤🐧🐦"

        if (type_lesson == "ЛК"):
            smile_type = "🐦"
        elif (type_lesson == "ЛБ"):
            smile_type = "🐤"
        elif (type_lesson == "ПР"):
            smile_type = "🐧"
        else:
            smile_type = "🐔"

        smile = "🧖🏿‍♀️" if subject == 'Л-МВ' else "🧖🏻‍♀️" if subject == 'ВТтаВД' else "" 

        text += f'{period} | {time_start} - {time_end}: {smile_type}{type_lesson} {smile}{subject} \n'

    if (len(text) == 0):
        text = "Пар немає\n"

    return text
