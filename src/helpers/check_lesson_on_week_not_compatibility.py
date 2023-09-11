import pandas

from helpers.get_current_week_type import get_current_week_type


def check_lesson_on_week_not_compatibility(lesson_type, subject, next=False):
    current_week_type = get_current_week_type()

    if (next == True):
        current_week_type = not current_week_type

    first = (not current_week_type and 'З' in lesson_type and not 'Ч' in lesson_type)
    second = (current_week_type and 'Ч' in lesson_type and not 'З' in lesson_type)
    third = pandas.isna(subject)

    return (first or second or third)
