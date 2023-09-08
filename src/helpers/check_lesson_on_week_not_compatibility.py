import pandas

from helpers.check_is_even_week import check_is_even_week


def check_lesson_on_week_not_compatibility(lesson_type, subject):
    is_even_week = check_is_even_week()

    return ((not is_even_week and 'З' in lesson_type) or
            (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
            pandas.isna(subject))
