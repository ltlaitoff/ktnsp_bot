from datetime import datetime


def get_current_week_day():
    return datetime.now().isoweekday()
