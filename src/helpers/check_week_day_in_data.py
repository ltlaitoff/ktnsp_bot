from config import data


def check_week_day_in_data(week_day):
    return not week_day in data['day_of_the_week'].tolist()
