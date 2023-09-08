import pandas


def check_lesson_on_week_not_compatibility(is_even_week, lesson_type, subject):
    return ((not is_even_week and 'З' in lesson_type) or
            (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
            not pandas.notna(subject))
