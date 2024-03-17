from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config_data.config import _CONFIG


dp = Dispatcher()
bot = Bot(_CONFIG.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))