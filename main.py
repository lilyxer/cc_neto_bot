import asyncio

from database.engine import create_db, insert_db, session_maker
from db_scripts.create_db import create_database
from handlers import handlers
from loader import bot, dp
from middlewares.db import DataBaseSession


STATUS_DB = True

async def on_startup(bot):
    if STATUS_DB:
        await create_db()
        await insert_db()
    print('запускаемся...\n')

async def on_shutdown(bot):
    print('Бот прекратил работу!')

async def main() -> None:
    dp.include_router(handlers.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    wb_info = await bot.get_webhook_info()

    if wb_info.allowed_updates:
        await dp.start_polling(bot, allowed_updates=[])
    else:
        await dp.start_polling(bot)


if __name__ == '__main__':
    STATUS_DB = create_database()
    asyncio.run(main())