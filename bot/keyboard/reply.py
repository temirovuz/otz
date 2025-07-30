from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder


def contact_keyboard():
    keyword = ReplyKeyboardBuilder()
    keyword.row(KeyboardButton(text='☎️ Telefon raqamzini yuborish', request_contact=True))
    return keyword.as_markup(resize_keyboard=True)