from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config_data.config import _CONFIG
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
dp = Dispatcher()
bot = Bot(_CONFIG.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))