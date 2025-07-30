import re

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from rest_framework_simplejwt.utils import aware_utcnow

from bot.crud import get_manager, create_manager
from bot.filters.custom import format_phone_number
from bot.keyboard.inline import cancel_button
from bot.states.register import AdminRegister

router = Router()


@router.callback_query(F.data == 'add_manager')
async def add_manager_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Ish boshqaruvchini Telefon raqamini yuboring!\n*Namuna:* +99894 123 45 67",
                                     reply_markup=cancel_button())
    await state.set_state(AdminRegister.phone_number)


@router.message(AdminRegister.phone_number)
async def manager_phone_number_handler(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    # Format tekshiruvi
    try:
        format_phone_number(phone)
    except Exception as e:
        return await message.answer(text=f"{e}")
    # Telefon raqam mavjudligini tekshirish — ASYNC
    if await get_manager(phone):
        return await message.answer("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")

    await state.update_data(phone_number=phone)
    await state.set_state(AdminRegister.password)
    return await message.answer("Parolingizni kiriting:", reply_markup=cancel_button(admin=True))


@router.message(AdminRegister.password)
async def manager_password_handler(message: types.Message, state: FSMContext):
    password = message.text.strip()
    if len(password) < 8:
        return await message.answer("Parol juda qisqa. Kamida 8 ta belgidan iborat bo'lishi kerak.")
    data = await state.get_data()

    await create_manager(phone=data['phone_number'], password=password)
    return await message.answer(text="Ish boshaqaruvchi yaratildi.")
