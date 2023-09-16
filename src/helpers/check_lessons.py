import asyncio
from datetime import datetime, timedelta
from config import bot, CHAT_ID, lesson_times, data, TIMER_DELAY, TIMER_LONG_DELAY
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from helpers.get_lesson_message_by_lesson import get_lesson_message_by_lesson


async def check_lessons(sent_notifications):
    while True:
        await asyncio.sleep(TIMER_DELAY)

        now = datetime.now()
        week_day = now.isoweekday()

        if not week_day in [1, 2, 3, 4, 5, 6]:
            continue

        todays_schedule = data[data['day_of_the_week'] == week_day]
        current_time = now.strftime('%H:%M')

        for _, row in todays_schedule.iterrows():
            subject = row['subject']
            period = row['period']

            time_start, time_end = lesson_times[period - 1]

            time_difference = datetime.strptime(
                time_start, '%H:%M') - datetime.strptime(current_time, '%H:%M')

            if (
                (time_difference <= timedelta(minutes=5))
                and (time_start > current_time)
                and not check_lesson_on_week_not_compatibility(row["type"], subject)
            ):
                lesson_key = f"{week_day}_{period}"

                if lesson_key in sent_notifications:
                    continue

                text_for_send = get_lesson_message_by_lesson(
                    time_start,
                    time_end,
                    row,
                    f"Пара через {time_difference.seconds // 60} хвилин"
                )

                await bot.send_message(chat_id=CHAT_ID, text=text_for_send, parse_mode='HTML', disable_web_page_preview=True)
                sent_notifications.add(lesson_key)
                await asyncio.sleep(TIMER_LONG_DELAY)
                break
