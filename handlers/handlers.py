import sqlalchemy.exc
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from states.states import FSMInProgress
from database.models import User, Word, UserAddWord
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from keyboards.keyboards import BotKeyBoardStart, BotKeyBoard, BotKeyBoardProgres
from loader import scheduler
from sqlalchemy import select, desc, insert
from random import choice

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import answers
from core.scripts import get_samples, get_words

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(msg: Message, state: FSMContext,
                                session: AsyncSession):
    """запускаем бота, входим в состяние прогресса
    добавляем пользователя в базу и здороваемся"""
    await msg.answer(text=answers['/start'], reply_markup=BotKeyBoardStart()())
    await state.set_state(FSMInProgress.progress)
    query = select(User).where(User.user_id == msg.from_user.id)
    answer = await session.execute(query)
    if not answer.scalars().first():
        new_user = User(user_id=msg.from_user.id, name=msg.from_user.full_name)
        session.add(new_user)
        await session.commit()
        await msg.answer(f'Добро пожаловать {msg.from_user.full_name}')
    else:
        await msg.answer(f'С возвращением {msg.from_user.full_name}')


@router.message(F.text.in_({'Учить', 'Дальше ⏭'}), StateFilter(FSMInProgress.progress))
async def process_in_learn(msg: Message, session: AsyncSession):
    await msg.answer(text=answers['Учить'])
    words = await session.execute(select(Word))
    user_words = await session.execute(select(UserAddWord).where(UserAddWord.user_id == msg.from_user.id))
    all_words = set(words).union(set(user_words))
    words, ans = get_samples(get_words(all_words))
    kb = BotKeyBoard(words[1], ans)()
    await msg.answer(text=f'Пробуем, нажми на верный ответ для слова:\n{words[0]}',
                     reply_markup=kb)



@router.callback_query()
async def check_query(clbk: CallbackQuery):
    await clbk.message.delete_reply_markup()
    text='Поздравляю, вы верно ответили' if clbk.data.strip() else 'Извини, ты не прав'
    await clbk.message.answer(text=text,
                              reply_markup=BotKeyBoardProgres()())


@router.message(F.text.in_({'Добавить слово ➕', 'Удалить слово🔙'}),
                ~StateFilter(FSMInProgress.progress))
async def process_not_entry(msg: Message):
    """если не запустили бота через start - команды не поддерживаются"""
    await msg.answer(text='пожалуйста нажми /start - запусти меня '
                          'и пользуйся клавиатурой',
                          reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]],
                                                           resize_keyboard=True))




@router.message()
async def send_answer(msg: Message):
    await msg.answer(text='Я не знаю таких команд, пожалуйста нажми'
                     '\n/start - запусти меня и пользуйся клавиатурой')
