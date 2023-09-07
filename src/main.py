import asyncio
import pandas as pd
from datetime import datetime, timedelta
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv
from os import getenv
from config import bot, dp, schedule_file_path, lesson_times, CHAT_ID, DAY_NAMES
from helpers.get_week_number import get_week_number
load_dotenv()

loop = asyncio.get_event_loop()
sent_notifications = set()
data = pd.read_csv(schedule_file_path)


def get_lesson_message_by_lesson(
    time_start,
    time_end,
    lesson
):
    return get_lesson_message(
        time_start,
        time_end,
        lesson['subject'],
        lesson['teacher'],
        lesson['type_lesson'],
        lesson['additional_text'],
        lesson['meeting_link'],
        lesson['zoom_code'],
        lesson['zoom_password'],
        lesson['email'],
        lesson['telegram'],
    )


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
                and (not pd.isna(row['type']) and row['type'] != "Null")
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

                await bot.send_message(chat_id=chat_id, text=text_for_send, parse_mode='HTML', disable_web_page_preview=True)
                sent_notifications.add(lesson_key)
                break

        await asyncio.sleep(20)


@dp.message_handler(commands=['nextlesson'])
async def next_lesson(message: types.Message):
    now = datetime.now()
    week_day = datetime.now().isoweekday()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    is_even_week = get_week_number()

    if not week_day in data['day_of_the_week'].tolist():
        return

    todays_schedule = data[data['day_of_the_week'] == week_day]
    lesson = None

    for _, row in todays_schedule.iterrows():
        if lesson is not None:
            break

        period = row['period']
        lesson_type = str(row['type'])

        time_start, time_end = lesson_times[period - 1]
        start_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_start.split(':')))
        end_datetime = datetime(
            current_year, current_month, current_day, *map(int, time_end.split(':')))

        if (
            (not is_even_week and 'З' in lesson_type) or
            (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
            not pd.notna(row["subject"])
        ):
            continue

        if lesson is None and (now >= start_datetime and now <= end_datetime or now <= start_datetime):
            lesson = row

    if lesson is not None and (not pd.isna(lesson["subject"]) and lesson["subject"] != "Null"):
        text_for_send = get_lesson_message_by_lesson(
            time_start,
            time_end,
            lesson
        )

        await message.answer(text_for_send, parse_mode='HTML', disable_web_page_preview=True)
        return

    await message.answer('Сьогодні пар більше не має.')


@dp.message_handler(commands=['daily_schedule'])
async def daily_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()

    if not week_day in data['day_of_the_week'].tolist():
        await message.answer("Пар не має")
        return

    todays_schedule = data[data['day_of_the_week'] == week_day]
    is_even_week = get_week_number()
    schedule_text = f"Розклад на сьогодні ({'Знаменник' if is_even_week else 'Чисельник'}):\n"

    for _, row in todays_schedule.iterrows():
        time_start, time_end = lesson_times[row['period'] - 1]

        subject = row['subject']
        type_lesson = row['type_lesson']
        lesson_type = row['type']
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
    week_text = f"Розклад на цей тиждень({'Знаменник' if is_even_week else 'Чисельник'}):\n\n"

    for day in range(1, 7):
        todays_schedule = data[data['day_of_the_week'] == day]
        text = f"{DAY_NAMES[day - 1]}:\n"

        for _, row in todays_schedule.iterrows():
            time_start, time_end = lesson_times[row['period'] - 1]
            subject = row['subject']
            lesson_type = row['type']
            type_lesson = row['type_lesson']

            if (
                (not is_even_week and 'З' in lesson_type) or
                (is_even_week and 'Ч' in lesson_type and not 'З' in lesson_type) or
                not pd.notna(subject)
            ):
                continue

            text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'

        week_text += text + "\n"

    await message.answer(week_text)


if __name__ == '__main__':
    # asyncio.run(main())
    loop.create_task(check_lessons())
    executor.start_polling(dp, skip_updates=True)
