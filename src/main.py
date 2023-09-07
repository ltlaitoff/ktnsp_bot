import asyncio
import pandas as pd
from datetime import datetime, timedelta
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv
from os import getenv
from config import bot, dp, schedule_file_path, lesson_times, CHAT_ID
from helpers.get_week_number import get_week_number
from helpers.get_day_name import get_day_name
load_dotenv()

loop = asyncio.get_event_loop()
sent_notifications = set()
data = pd.read_csv(schedule_file_path)


def get_lesson_message(
    time_start,
    time_end,
    subject,
    teacher,
    type_lesson,
    additional_text,
    meeting_link,
    zoom_code,
    zoom_password,
    email,
    telegram,
):
    text = (
        f'Наступна пара: "<code>{subject}</code>"\n'
        f'Викладач: <code>{teacher}</code>\n'
        f'Час: {time_start} - {time_end}\n'
    )

    if not pd.isna(type_lesson) and type_lesson != "Null":
        text += f'Тип пари: "<code>{type_lesson}</code>"\n'

    if not pd.isna(additional_text) and additional_text != "Null":
        text += f'Додадкова інфа: "<code>{additional_text}</code>"\n'

    if not pd.isna(meeting_link) and meeting_link != "Null":
        text += f'<a href="{meeting_link}">Посилання на зустріч</a>\n'

    if not pd.isna(zoom_code) and zoom_code != "Null":
        text += f'Ідентифікатор Zoom: {zoom_code}\n'

    if not pd.isna(zoom_password) and zoom_password != "Null":
        text += f'Пароль Zoom: {zoom_password}\n'

    if not pd.isna(email) and email != "Null":
        text += f'Електронна адреса: {email}\n'

    if not pd.isna(telegram) and telegram != "Null":
        text += f'Telegram: {telegram}\n'

    return text


async def check_lessons():
    while True:
        now = datetime.now()
        week_day = datetime.now().isoweekday()
        current_week_number = get_week_number()

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
                and (not pd.isna(subject) and subject != "Null")
                and (not pd.isna(row['Type']) and row['Type'] != "Null")
                and (('Ч' in row['Type'] and current_week_number == 0) or ('З' in row['Type'] and current_week_number == 1))
            ):
                lesson_key = f"{week_day}_{period}"

                if lesson_key not in sent_notifications:
                    text_for_send = get_lesson_message(
                        time_start,
                        time_end,
                        subject,
                        row['teacher'],
                        row['type_lesson'],
                        row['additional_text'],
                        row['meeting_link'],
                        row['zoom_code'],
                        row['zoom_password'],
                        row['email'],
                        row['telegram'],
                    )

                    await bot.send_message(chat_id=chat_id, text=text_for_send, parse_mode='HTML', disable_web_page_preview=True)
                    sent_notifications.add(lesson_key)
                    print(sent_notifications)
                    break

        await asyncio.sleep(20)


@dp.message_handler(commands=['nextlesson'])
async def next_lesson(message: types.Message):
    now = datetime.now()
    week_day = now.isoweekday()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_week_number = int(get_week_number())

    if not week_day in data['day_of_the_week'].tolist():
        return

    todays_schedule = data[data['day_of_the_week'] == week_day]
    current_lesson = None
    next_lesson = None
    time_start_current = ""
    time_end_current = ""
    time_start_next = ""
    time_end_next = ""
    subject = ""

    for _, row in todays_schedule.iterrows():
        period = row['period']
        if period >= 1 and period <= len(lesson_times):
            time_start, time_end = lesson_times[period - 1]
            start_datetime = datetime(
                current_year, current_month, current_day, *map(int, time_start.split(':')))
            end_datetime = datetime(
                current_year, current_month, current_day, *map(int, time_end.split(':')))
            if (('Ч' in str(row['Type']) and current_week_number == 0) or ('З' in str(row['Type']) and current_week_number == 1)):
                if current_lesson is None and now >= start_datetime and now <= end_datetime:
                    current_lesson = row
                    time_start_current = time_start
                    time_end_current = time_end
                    subject = row['subject']
                if next_lesson is None and now <= start_datetime:
                    next_lesson = row
                    time_start_next = time_start
                    time_end_next = time_end
                    subject = row['subject']
                if current_lesson is not None and next_lesson is not None:
                    break
    if next_lesson is not None and (not pd.isna(next_lesson["subject"]) and next_lesson["subject"] != "Null"):
        text_for_send = get_lesson_message(
            time_start,
            time_end,
            next_lesson['subject'],
            next_lesson['teacher'],
            next_lesson['type_lesson'],
            next_lesson['additional_text'],
            next_lesson['meeting_link'],
            next_lesson['zoom_code'],
            next_lesson['zoom_password'],
            next_lesson['email'],
            next_lesson['telegram'],
        )
        await message.answer(text_for_send, parse_mode='HTML', disable_web_page_preview=True)
        print("Відправлено наступне повідомлення")
    elif current_lesson is not None and (not pd.isna(current_lesson["subject"]) and current_lesson["subject"] != "Null"):
        text_for_send = get_lesson_message(
            time_start,
            time_end,
            current_lesson['subject'],
            current_lesson['teacher'],
            current_lesson['type_lesson'],
            current_lesson['additional_text'],
            current_lesson['meeting_link'],
            current_lesson['zoom_code'],
            current_lesson['zoom_password'],
            current_lesson['email'],
            current_lesson['telegram'],
        )

        await message.answer(text_for_send, parse_mode='HTML', disable_web_page_preview=True)
        print("Відправлено поточне повідомлення")
    else:
        await message.answer('Сьогодні пар більше не має.')
        print("Пар більше не має")


@dp.message_handler(commands=['daily_schedule'])
async def daily_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        await message.answer("Пар не має")
        return

    todays_schedule = data[data['day_of_the_week'] == week_day]
    is_even_week = get_week_number()
    schedule_text = f"Розклад на сьогодні ({'Чисельник' if is_even_week else 'Знаменник'}):\n"
    for _, row in todays_schedule.iterrows():
        period = row['period']
        if period >= 1 and period <= len(lesson_times):
            time_start, time_end = lesson_times[period - 1]
            subject = row['subject']
            type_lesson = row['type_lesson']
            lesson_type = row['Type']
            if pd.notna(type_lesson) and pd.notna(subject):
                if ('Ч' in lesson_type and is_even_week) or ('З' in lesson_type and not is_even_week):
                    lesson_type_text = "Чисельник" if is_even_week else "Знаменник"
                    schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
    await message.answer(schedule_text)


@dp.message_handler(commands=['week_schedule'])
async def week_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        await message.answer('Розклад на цей тиждень ще не встановлено.')
        return

    is_even_week = get_week_number()
    week_schedule_text = f"Розклад на цей тиждень({'Знаменник' if is_even_week else 'Чисельник'}):\n\n"

    for day in range(1, 7):
        day_name = get_day_name(day)
        todays_schedule = data[data['day_of_the_week'] == day]
        schedule_text = f"{day_name}:\n"
        for _, row in todays_schedule.iterrows():
            period = row['period']
            if period >= 1 and period <= len(lesson_times):
                time_start, time_end = lesson_times[period - 1]
                subject = row['subject']
                lesson_type = row['Type']
                type_lesson = row['type_lesson']
                if (is_even_week and 'З' in lesson_type) or (not is_even_week and 'Ч' in lesson_type):
                    if pd.notna(subject):
                        schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
        week_schedule_text += schedule_text + "\n"

    await message.answer(week_schedule_text)


if __name__ == '__main__':
    # asyncio.run(main())
    loop.create_task(check_lessons())
    executor.start_polling(dp, skip_updates=True)
