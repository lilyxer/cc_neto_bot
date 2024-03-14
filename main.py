import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config_data.config import load_config, Config
from db_scripts.create_db import create_database
from handlers import handlers
from classes.classes import PostgresDB


async def main(_config: Config) -> None:

    bot = Bot(token=_config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    db = PostgresDB(_config.db.DSN)

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    wb_info = await bot.get_webhook_info()

    if wb_info.allowed_updates:
        await dp.start_polling(bot, allowed_updates=[])
    else:
        await dp.start_polling(bot)


if __name__ == '__main__':
    _config = load_config()
    if create_database(_config.db):
        ...
    print('запускаемся...\n')
    asyncio.run(main(_config))