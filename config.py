from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

load_dotenv()

API_TOKEN = getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)