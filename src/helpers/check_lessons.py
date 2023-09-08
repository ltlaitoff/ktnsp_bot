import asyncio
from datetime import datetime, timedelta

import pandas
from config import bot, CHAT_ID, lesson_times, data
from helpers.get_lesson_message_by_lesson import get_lesson_message_by_lesson

from helpers.check_is_even_week import check_is_even_week


async def check_lessons(sent_notifications):
    while True:
        now = datetime.now()
        week_day = datetime.now().isoweekday()
        current_week_number = check_is_even_week()

        if not week_day in [1, 2, 3, 4, 5, 6]:
            continue

        todays_schedule = data[data['day_of_the_week'] == week_day]

        for _, row in todays_schedule.iterrows():
            subject = row['subject']
            period = row['period']

            time_start, time_end = lesson_times[period - 1]

            current_time = now.strftime('%H:%M')

            time_difference = datetime.strptime(
                time_start, '%H:%M') - datetime.strptime(current_time, '%H:%M')

            if (
                (time_difference <= timedelta(minutes=5))
                and (time_start > current_time)
                and (not pandas.isna(subject) and subject != "Null")
                and (not pandas.isna(row['type']) and row['type'] != "Null")
                and (('Ч' in row['type'] and current_week_number == 0) or ('З' in row['type'] and current_week_number == 1))
            ):
                lesson_key = f"{week_day}_{period}"

                if lesson_key in sent_notifications:
                    continue

                text_for_send = get_lesson_message_by_lesson(
                    time_start,
                    time_end,
                    row
                )

                await bot.send_message(chat_id=CHAT_ID, text=text_for_send, parse_mode='HTML', disable_web_page_preview=True)
                sent_notifications.add(lesson_key)
                break

        await asyncio.sleep(25)
