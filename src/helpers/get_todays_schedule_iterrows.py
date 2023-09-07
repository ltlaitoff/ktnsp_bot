from config import data


def get_todays_schedule_iterrows(week_day):
    return data[data['day_of_the_week'] == week_day].iterrows()
