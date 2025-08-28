from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.crud import get_user, get_user_type, user_update_tg_id
from bot.keyboard.inline import admin_buttons, customer_buttons, employee_buttons
from bot.keyboard.reply import contact_keyboard
from bot.states.register import RegisterUser
from core.settings import TG_ADMINS as ADMINS

router = Router()


@router.message(CommandStart())
async def start_handle(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        return await message.answer(
            text="Siz Adminsiz va Kerakli bolimlarni birini tanlang",
            reply_markup=admin_buttons(),
        )
    check_user = await get_user(str(message.from_user.id))
    user_type = await get_user_type(str(message.from_user.id))
    if not check_user:
        await state.set_state(RegisterUser.contact)
        await message.answer(
            text="*OTZ GROUP* _Korxonasining Rasmiy botiga hush kelibsiz.🙂\n\nRo'yxatdan o'tish uchun_ *Telefon raqamingizni yuboring!👇*",
            reply_markup=contact_keyboard(),
            parse_mode="MARKDOWN",
        )
    elif user_type == "ishchi":
        await message.answer(
            text="SIz ishchi sifatida ro'yxatdan o'tgansiz.",
            reply_markup=employee_buttons(str(message.from_user.id)),
        )
    elif user_type == "mijoz":
        await message.answer(
            text="Siz mijoz sifatida ro'yxatdan o'tgansiz.",
            reply_markup=customer_buttons(str(message.from_user.id)),
        )
    else:
        await message.answer(
            text="Siz ro'yxatdan o'tgansiz, lekin sizning unvoninggiz aniqlanmagan.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(F.chat.type == "private", RegisterUser.contact)
async def register_user_contact(message: types.Message, state: FSMContext):
    await state.clear()
    if (
        message.contact.phone_number.startswith("998")
        or message.contact.phone_number.startswith("+998")
    ) and message.contact.user_id == message.from_user.id:
        await user_update_tg_id(message.contact.phone_number, message.contact.user_id)
        await message.answer(
            text="Siz muvofaqiyatli ro'yxatdan o'tingiz.\n/start ni bosib botni qayta ishga tushuring.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            text="Siz faqat O'zbekiston nomeri orqali ro'yxatdan o'tishin mumkin.\n\nNomeringizni yuborish uchun quyidagi tugmani bosing.👇",
        )
        await state.set_state(RegisterUser.contact)
