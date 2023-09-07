from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
