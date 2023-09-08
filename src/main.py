import asyncio
from aiogram.utils import executor
from dotenv import load_dotenv
from config import dp
from helpers.check_lessons import check_lessons
import handlers
from utils.set_bot_commands import set_default_commands
load_dotenv()

loop = asyncio.get_event_loop()
sent_notifications = set()


async def on_startup(dispatcher):
    print('on_startup')
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop.create_task(check_lessons(sent_notifications))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
