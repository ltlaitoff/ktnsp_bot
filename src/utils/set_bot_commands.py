from loguru import logger
from aiogram import types


@logger.catch
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("next_lesson", "nextlesson"),
            types.BotCommand("daily_schedule", "daily_schedule"),
            types.BotCommand("week_schedule", "week_schedule"),
            types.BotCommand("next_week_schedule", "next_week_schedule"),
        ]
    )
