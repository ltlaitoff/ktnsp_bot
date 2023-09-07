DAY_NAMES = [
    'Понеділок',
    'Вівторок',
    'Середа',
    'Четвер',
    "П'ятниця",
    'Субота'
]


def get_day_name(day):
    return DAY_NAMES[day - 1]
