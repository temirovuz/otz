from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.crud import get_user, create_user
from bot.keyboard.inline import admin_buttons
from bot.keyboard.reply import contact_keyboard
from bot.states.register import RegisterUser
from core.settings import TG_ADMINS as ADMINS

router = Router()


@router.message(CommandStart())
async def start_handle(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        return await message.answer(text='Siz Adminsiz va Kerakli bolimlarni birini tanlang', reply_markup=admin_buttons())
    check_user = await get_user(str(message.from_user.id))
    if not check_user:
        await state.set_state(RegisterUser.contact)
        await message.answer(
            text="*OTZ GROUP* _Korxonasining Rasmiy botiga hush kelibsiz.🙂\n\nRo'yxatdan o'tish uchun_ *Telefon raqamingizni yuboring!👇*",
            reply_markup=contact_keyboard(), parse_mode="MARKDOWN")
    else:
        await message.answer(text="Tez orada ishlaydi")


@router.message(F.chat.type == 'private', RegisterUser.contact)
async def register_user_contact(message: types.Message, state: FSMContext):
    await state.clear()
    if message.contact.phone_number.startswith('+998') and message.contact.user_id == message.from_user.id:
        await create_user(str(message.from_user.id), message.contact.phone_number)
        await message.answer(text="Siz muvofaqiyatli ro'yxatdan o'tingiz.\nTez orada javob olasiz.",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="Siz faqat O'zbekiston nomeri orqali ro'yxatdan o'tishin mumkin.")
