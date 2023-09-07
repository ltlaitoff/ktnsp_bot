from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

load_dotenv()

# 'dev' | 'prod'
MODE = 'dev'


BOT_TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


schedule_file_path = 'src/data/data.csv'

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

DAY_NAMES = [
    'Понеділок',
    'Вівторок',
    'Середа',
    'Четвер',
    "П'ятниця",
    'Субота'
]

if (MODE == 'prod'):
    CHAT_ID = -1001971949292
else:
    CHAT_ID = -657080651
