from datetime import date


def check_is_even_week():
    start_date = date(2023, 9, 4)  # Начало учебного года
    today = date.today()
    delta = today - start_date
    days_passed = delta.days
    week_number = days_passed // 7  # Полное количество недель прошло
    is_even_week = week_number % 2 == 0  # 0 - знаменатель, 1 - числитель
    return is_even_week
