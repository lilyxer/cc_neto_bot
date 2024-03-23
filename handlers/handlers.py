from random import choice, shuffle

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from keyboards.keyboards import BotKeyBoardStart, BotKeyBoard, BotKeyBoardProgres, BotKeyBoardCancel
from sqlalchemy import select, delete, and_, func, union_all
from sqlalchemy.ext.asyncio import AsyncSession
from states.states import FSMInProgress

from lexicon.lexicon import answers
from core.scripts import parse_words
from database.models import User, Word, UserAddWord


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
    stmt1 = select(Word.word_eng, Word.word_rus).order_by(func.random())
    stmt2 = (select(UserAddWord.word_eng, UserAddWord.word_rus)
             .filter(UserAddWord.user_id == msg.from_user.id).order_by(func.random()))
    u = union_all(stmt1, stmt2)
    u = u.limit(4)
    words = await session.execute(u)
    words = words.fetchall()
    shuffle(words)
    kb = BotKeyBoard(choice(words)[1], [x[1] for x in words])()
    await msg.answer(text=f'Пробуем, нажми на верный ответ для слова:\n{words[0][0]}',
                     reply_markup=kb)


@router.message(F.text.in_({'Удалить слово🔙', 'Добавить слово ➕'}),
                StateFilter(FSMInProgress.progress))
async def process_enter_to_add_word(msg: Message, state: FSMContext):
    if msg.text == 'Добавить слово ➕':
        await msg.answer(text=answers['Добавление'], reply_markup=BotKeyBoardCancel()())
        await state.set_state(FSMInProgress.add_word)
    else:
        await msg.answer(text=answers['Удаление'], reply_markup=BotKeyBoardCancel()())
        await state.set_state(FSMInProgress.del_word)


@router.callback_query(F.data == 'cancel', StateFilter(FSMInProgress.add_word))
async def process_cancel(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.delete_reply_markup()
    await state.set_state(FSMInProgress.progress)
    await clbk.message.answer(text='Вы отменили процесс редактироваыния',
                              reply_markup=BotKeyBoardProgres()())


@router.message(StateFilter(FSMInProgress.add_word))
async def process_add_word(msg: Message, state: FSMContext, session: AsyncSession):
    msg.delete_reply_markup()
    await state.set_state(FSMInProgress.progress)
    if ',' in msg.text:
        text = msg.text.split(',')
        try:
            for row in text:
                eng, rus = parse_words(row)
                new_data = UserAddWord(word_eng=eng, word_rus=rus, user_id=msg.from_user.id)
                session.add(new_data)
            await session.commit()
            await msg.answer(text='ОК, едем дальше?', reply_markup=BotKeyBoardProgres()())
        except Exception as e:
            await session.rollback()
            await msg.answer(
                text=f'Ошибка при обработке: {str(e)}',
                reply_markup=BotKeyBoardProgres()(),
            )
    else:
        try:
            eng, rus = parse_words(msg.text)
            new_data = UserAddWord(word_eng=eng, word_rus=rus, user_id=msg.from_user.id)
            session.add(new_data)
            await session.commit()
            await msg.answer(text='ОК, едем дальше?', reply_markup=BotKeyBoardProgres()())
        except Exception as e:
            await session.rollback()
            await msg.answer(
                text=f'Ошибка при обработке: {str(e)}',
                reply_markup=BotKeyBoardProgres()(),
            )


@router.message(StateFilter(FSMInProgress.del_word))
async def process_add_word(msg: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(FSMInProgress.progress)
    async with session as db_session:
        delete_stmt = delete(UserAddWord).where(
            and_(UserAddWord.user_id == msg.from_user.id,
                 UserAddWord.word_eng == msg.text.strip().capitalize())
        )
        result = await db_session.execute(delete_stmt)
        deleted_rows = result.rowcount
        if deleted_rows:
            await db_session.commit()
            await msg.answer(f'{msg.text} удалено', reply_markup=BotKeyBoardProgres()())
        else:
            await db_session.rollback()
            await msg.answer(f'{msg.text} не найдено', reply_markup=BotKeyBoardProgres()())


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
