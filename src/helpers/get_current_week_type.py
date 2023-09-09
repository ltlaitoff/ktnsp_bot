from datetime import date


def get_current_week_type():
    start_date = date(2023, 9, 4)  # Начало учебного года
    today = date.today()
    delta = today - start_date
    days_passed = delta.days
    week_number = days_passed // 7  # Полное количество недель прошло
    current_week_type = week_number % 2 == 0  # 0 - знаменатель, 1 - числитель
    return current_week_type
