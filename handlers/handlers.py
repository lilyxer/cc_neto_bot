from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, ContentType


router = Router()


@router.message(CommandStart())
async def process_start_command(msg: Message):
    await msg.answer(text='hello')

@router.message()
async def send_answer(msg: Message):
    await msg.answer(text='Я не знаю таких команд, пожалуйста нажми'
                     '\n/start - запусти меня и пользуйся клавиатурой')