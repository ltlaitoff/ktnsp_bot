from loguru import logger
from aiogram import types


@logger.catch
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Показати справку"),
            types.BotCommand("next_lesson", "Наступна пара сьогодні"),
            types.BotCommand("daily_schedule", "Пари на день"),
            types.BotCommand("daily_schedule_detailed",
                             "Пари на день детально"),
            types.BotCommand("week_schedule", "Розклад на тиждень"),
            types.BotCommand("next_week_schedule",
                             "Розклад на наступний тиждень"),
            types.BotCommand("get_all", "Показати всю інформацію")
        ]
    )
