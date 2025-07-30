from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_buttons():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="👮🏻‍♂️ Ish boshqaruvchi qo'shish", callback_data='add_manager'),
        InlineKeyboardButton(text="📥 Malumotlar excel filega yozib olish", callback_data="downland_data")
    )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


def cancel_button(admin: bool = False):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f'cancel:{admin}'))
    return keyboard.as_markup(resize_keyboard=True)
