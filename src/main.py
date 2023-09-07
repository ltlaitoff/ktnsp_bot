import asyncio
import pandas as pd
from datetime import datetime, timedelta, date
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv
from os import getenv
load_dotenv()

API_TOKEN = getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()
schedule_file_path = 's.csv'
sent_notifications = set()
df = pd.read_csv(schedule_file_path)

lesson_times = [
    ('08:30', '09:50'),
    ('10:05', '11:25'),
    ('11:55', '13:15'),
    ('13:25', '14:45'),
    ('14:55', '16:15'),
    ('16:45', '18:05'),
    ('18:15', '19:35'),
    ('19:45', '21:05'),
]

CHAT_ID = -1001971949292

def get_week_number():
    start_date = date(2023, 9, 4)  # Начало учебного года
    today = date.today()
    delta = today - start_date
    days_passed = delta.days
    week_number = days_passed // 7  # Полное количество недель прошло
    is_even_week = week_number % 2 == 0  # 0 - знаменатель, 1 - числитель
    return is_even_week

async def send_lesson_notification(chat_id, lesson, time_start, time_end, text):
    text = (
        f'Наступна пара: "<code>{lesson["Subject"]}</code>"\n'
        f'Викладач: <code>{lesson["Teacher"]}</code>\n'
        f'Час: {time_start} - {time_end}\n'
    )
    if not pd.isna(lesson["Type_lesson"]) and lesson["Type_lesson"] != "Null":
        text += f'Тип пари: "<code>{lesson["Type_lesson"]}</code>"\n'
    if not pd.isna(lesson["Additional Text"]) and lesson["Additional Text"] != "Null":
        text += f'Додадкова інфа: "<code>{lesson["Additional Text"]}</code>"\n'
    if not pd.isna(lesson["Meeting Link"]) and lesson["Meeting Link"] != "Null":
        text += f'<a href="{lesson["Meeting Link"]}">Посилання на зустріч</a>\n'
    if not pd.isna(lesson["zoom_code"]) and lesson["zoom_code"] != "Null":
        text += f'Ідентифікатор Zoom: {lesson["zoom_code"]}\n'
    if not pd.isna(lesson["zoom_password"]) and lesson["zoom_password"] != "Null":
        text += f'Пароль Zoom: {lesson["zoom_password"]}\n'
    if not pd.isna(lesson["email"]) and lesson["email"] != "Null":
        text += f'Електронна адреса: {lesson["email"]}\n'
    if not pd.isna(lesson["telegram"]) and lesson["telegram"] != "Null":
        text += f'Telegram: {lesson["telegram"]}\n'
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML', disable_web_page_preview=True)

async def check_lessons():
    while True:
        now = datetime.now()
        week_day = datetime.now().isoweekday()
        current_week_number = get_week_number()
        if week_day in [1, 2, 3, 4, 5, 6]:
            todays_schedule = df[df['Day of the week'] == week_day]
            for _, row in todays_schedule.iterrows():
                subject = row['Subject']
                period = row['Period']
                if period >= 1 and period <= len(lesson_times):
                    time_start, time_end = lesson_times[period - 1]
                    current_time = now.strftime('%H:%M')
                    time_difference = datetime.strptime(time_start, '%H:%M') - datetime.strptime(current_time, '%H:%M')
                    if (
                        (time_difference <= timedelta(minutes=5))
                        and (time_start > current_time)
                        and (not pd.isna(subject) and subject != "Null")
                        and (not pd.isna(row['Type']) and row['Type'] != "Null")
                        and (('Ч' in row['Type'] and current_week_number == 0) or ('З' in row['Type'] and current_week_number == 1))
                    ):
                        lesson_key = f"{week_day}_{period}"
                        if lesson_key not in sent_notifications:
                            text = (
                                f'Наступна пара: "<code>{subject}</code>"\n'
                                f'Тип пари: {row["Type_lesson"]}\n'
                                f'Викладач: {row["Teacher"]}\n'
                                f'Час: {time_start} - {time_end}\n'
                                f'Ідентифікатор Zoom: {row["zoom_code"]}\n'
                                f'Пароль Zoom: {row["zoom_password"]}\n'
                                f'Електронна адреса: {row["email"]}\n'
                                f'Telegram: {row["telegram"]}\n'
                            )
                            if not pd.isna(row["Additional Text"]) and row["Additional Text"] != "Null":
                                text += f'Додадкова інфа: "<code>{row["Additional Text"]}</code>"\n'
                            if not pd.isna(row["Meeting Link"]) and row["Meeting Link"] != "Null":
                                text += f'Посилання на зустріч: <a href="{row["Meeting Link"]}">{row["Meeting Link"]}</a>\n'
                            await send_lesson_notification(chat_id=CHAT_ID, lesson=row, time_start=time_start, time_end=time_end, text=text)
                            sent_notifications.add(lesson_key)
                            print(sent_notifications)
                            break
        await asyncio.sleep(20)
loop.create_task(check_lessons())

@dp.message_handler(commands=['nextlesson'])
async def next_lesson(message: types.Message):
    now = datetime.now()
    week_day = datetime.now().isoweekday()
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    current_week_number = int(get_week_number())
    if week_day in df['Day of the week'].tolist():
        todays_schedule = df[df['Day of the week'] == week_day]
        current_lesson = None
        next_lesson = None
        time_start_current = ""
        time_end_current = ""
        time_start_next = ""
        time_end_next = ""
        subject = ""
        for _, row in todays_schedule.iterrows():
            period = row['Period']
            if period >= 1 and period <= len(lesson_times):
                time_start, time_end = lesson_times[period - 1]
                start_datetime = datetime(current_year, current_month, current_day, *map(int, time_start.split(':')))
                end_datetime = datetime(current_year, current_month, current_day, *map(int, time_end.split(':')))
                if (('Ч' in str(row['Type']) and current_week_number == 0) or ('З' in str(row['Type']) and current_week_number == 1)):
                    if current_lesson is None and now >= start_datetime and now <= end_datetime:
                        current_lesson = row
                        time_start_current = time_start
                        time_end_current = time_end
                        subject = row['Subject']
                    if next_lesson is None and now <= start_datetime:
                        next_lesson = row
                        time_start_next = time_start
                        time_end_next = time_end
                        subject = row['Subject']
                    if current_lesson is not None and next_lesson is not None:
                        break
        if next_lesson is not None and (not pd.isna(next_lesson["Subject"]) and next_lesson["Subject"] != "Null"):
            text = (
                f'Наступна пара: "<code>{next_lesson["Subject"]}</code>"\n'
                f'Викладач: <code>{next_lesson["Teacher"]}</code>\n'
                f'Час: {time_start_next} - {time_end_next}\n'
            )
            if not pd.isna(next_lesson["Type_lesson"]) and next_lesson["Type_lesson"] != "Null":
                text += f'Тип пари: "<code>{next_lesson["Type_lesson"]}</code>"\n'
            if not pd.isna(next_lesson["Additional Text"]) and next_lesson["Additional Text"] != "Null":
                text += f'Додаткова інформація: "<code>{next_lesson["Additional Text"]}</code>"\n'
            if not pd.isna(next_lesson["Meeting Link"]) and next_lesson["Meeting Link"] != "Null":
                text += f'Посилання на зустріч: {next_lesson["Meeting Link"]}\n'
            if not pd.isna(next_lesson["zoom_code"]) and next_lesson["zoom_code"] != "Null":
                text += f'Ідентифікатор Zoom: {next_lesson["zoom_code"]}\n'
            if not pd.isna(next_lesson["zoom_password"]) and next_lesson["zoom_password"] != "Null":
                text += f'Пароль Zoom: {next_lesson["zoom_password"]}\n'
            if not pd.isna(next_lesson["email"]) and next_lesson["email"] != "Null":
                text += f'Електронна пошта: {next_lesson["email"]}\n'
            if not pd.isna(next_lesson["telegram"]) and next_lesson["telegram"] != "Null":
                text += f'Telegram: {next_lesson["telegram"]}\n'
            await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
            print("Відправлено наступне повідомлення")
        elif current_lesson is not None and (not pd.isna(current_lesson["Subject"]) and current_lesson["Subject"] != "Null"):
            text = (
                f'Зараз пара: "<code>{subject}</code>"\n'
                f'Викладач: <code>{current_lesson["Teacher"]}</code>\n'
                f'Час: {time_start_current} - {time_end_current}\n'
            )
            if not pd.isna(next_lesson["Type_lesson"]) and next_lesson["Type_lesson"] != "Null":
                text += f'Тип пари: "<code>{next_lesson["Type_lesson"]}</code>"\n'
            if not pd.isna(current_lesson["Additional Text"]) and current_lesson["Additional Text"] != "Null":
                text += f'Додаткова інформація: "<code>{current_lesson["Additional Text"]}</code>"\n'
            if not pd.isna(current_lesson["Meeting Link"]) and current_lesson["Meeting Link"] != "Null":
                text += f'Посилання на зустріч: {current_lesson["Meeting Link"]}\n'
            if not pd.isna(current_lesson["zoom_code"]) and current_lesson["zoom_code"] != "Null":
                text += f'Ідентифікатор Zoom: {current_lesson["zoom_code"]}\n'
            if not pd.isna(current_lesson["zoom_password"]) and current_lesson["zoom_password"] != "Null":
                text += f'Пароль Zoom: {current_lesson["zoom_password"]}\n'
            if not pd.isna(current_lesson["email"]) and current_lesson["email"] != "Null":
                text += f'Електронна пошта: {current_lesson["email"]}\n'
            if not pd.isna(current_lesson["telegram"]) and current_lesson["telegram"] != "Null":
                text += f'Telegram: {current_lesson["telegram"]}\n'
            await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
            print("Відправлено поточне повідомлення")
        else:
            await message.answer('Сьогодні пар більше не має.')
            print("Пар більше не має")


@dp.message_handler(commands=['daily_schedule'])
async def daily_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()
    if week_day in df['Day of the week'].tolist():
        todays_schedule = df[df['Day of the week'] == week_day]
        is_even_week = get_week_number()
        schedule_text = f"Розклад на сьогодні ({'Чисельник' if is_even_week else 'Знаменник'}):\n"
        for _, row in todays_schedule.iterrows():
            period = row['Period']
            if period >= 1 and period <= len(lesson_times):
                time_start, time_end = lesson_times[period - 1]
                subject = row['Subject']
                type_lesson = row['Type_lesson']
                lesson_type = row['Type']
                if pd.notna(type_lesson) and pd.notna(subject):
                    if ('Ч' in lesson_type and is_even_week) or ('З' in lesson_type and not is_even_week):
                        lesson_type_text = "Чисельник" if is_even_week else "Знаменник"
                        schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
        await message.answer(schedule_text)
    else:
        await message.answer("Пар не має")

@dp.message_handler(commands=['week_schedule'])
async def week_schedule(message: types.Message):
    week_day = datetime.now().isoweekday()
    if week_day in df['Day of the week'].tolist():
        is_even_week = get_week_number()
        week_schedule_text = f"Розклад на цей тиждень({'Знаменник' if is_even_week else 'Чисельник'}):\n\n"
        for day in range(1, 7):
            day_name = get_day_name(day)
            todays_schedule = df[df['Day of the week'] == day]
            schedule_text = f"{day_name}:\n"
            for _, row in todays_schedule.iterrows():
                period = row['Period']
                if period >= 1 and period <= len(lesson_times):
                    time_start, time_end = lesson_times[period - 1]
                    subject = row['Subject']
                    lesson_type = row['Type']
                    type_lesson = row['Type_lesson']
                    if (is_even_week and 'З' in lesson_type) or (not is_even_week and 'Ч' in lesson_type):
                        if pd.notna(subject):
                            schedule_text += f'{time_start} - {time_end}: {type_lesson} {subject}\n'
            week_schedule_text += schedule_text + "\n"
        await message.answer(week_schedule_text)
    else:
        await message.answer('Розклад на цей тиждень ще не встановлено.')

def get_day_name(day):
    day_names = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота']
    return day_names[day - 1]

if __name__ == '__main__':
    # asyncio.run(main())
    executor.start_polling(dp, skip_updates=True)