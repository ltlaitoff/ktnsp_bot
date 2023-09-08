from helpers.check_is_even_week import check_is_even_week


def get_lesson_type_text():
    is_even_week = check_is_even_week()
    return 'Знаменник' if is_even_week else 'Чисельник'
