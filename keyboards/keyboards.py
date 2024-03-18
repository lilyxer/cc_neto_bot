from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class BotKeyBoardStart:
    def __call__(self) -> ReplyKeyboardMarkup:
        board = ReplyKeyboardBuilder()
        board.row(KeyboardButton(text='Учить'))
        board.row(KeyboardButton(text='Добавить слово ➕'), KeyboardButton(text='Удалить слово🔙'))
        return board.as_markup(one_time_keyboard=True, resize_keyboard=True)


class BotKeyBoard:
    def __init__(self, word: str, keys: tuple[str]) -> None:
        self._buttons = [InlineKeyboardButton(text=x,
                                              callback_data='True' if word==x else ' ') for x in keys]

    def __call__(self, width: int=2) -> InlineKeyboardMarkup:
        board = InlineKeyboardBuilder()
        board.row(*self._buttons, width=width)
        return board.as_markup()


class BotKeyBoardProgres:
    def __call__(self) -> ReplyKeyboardMarkup:
        board = ReplyKeyboardBuilder()
        board.row(KeyboardButton(text='Дальше ⏭'))
        board.row(KeyboardButton(text='Добавить слово ➕'), KeyboardButton(text='Удалить слово🔙'))
        return board.as_markup(one_time_keyboard=True, resize_keyboard=True)


class BotKeyBoardCancel:
    def __call__(self) -> InlineKeyboardMarkup:
        board = InlineKeyboardBuilder()
        board.row(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
        return board.as_markup()