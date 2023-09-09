from helpers.get_current_week_type import get_current_week_type


def get_lesson_type_text():
    current_week_type = get_current_week_type()
    return 'Знаменник' if current_week_type else 'Чисельник'
