from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from advance.models import Advance, Salary
from bot.crud import get_manager, create_manager
from bot.filters.custom import format_phone_number, get_data_by_months, write_advances_to_excel, write_foreign_orders_to_excel, write_local_delivary_to_excel, write_local_payments_to_excel, write_salaries_to_excel, write_transaction_to_excel
from bot.keyboard.inline import cancel_button, data_categries, select_month_keyboard
from bot.states.register import AdminRegister
from exchange.models import ProductOrder, Transaction
from local_trading.models import LocalPartnerDelivery, LocalPayment

router = Router()

# -------------------------> add manager handler <------------------------- #


@router.callback_query(F.data == "add_manager")
async def add_manager_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Ish boshqaruvchini Telefon raqamini yuboring!\n*Namuna:* +99894 123 45 67",
        reply_markup=cancel_button(True),
    )
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
    return await message.answer(
        "Parolingizni kiriting:", reply_markup=cancel_button(admin=True)
    )


@router.message(AdminRegister.password)
async def manager_password_handler(message: types.Message, state: FSMContext):
    password = message.text.strip()
    if len(password) < 8:
        return await message.answer(
            "Parol juda qisqa. Kamida 8 ta belgidan iborat bo'lishi kerak."
        )
    data = await state.get_data()

    await create_manager(phone=data["phone_number"], password=password)
    return await message.answer(text="Ish boshaqaruvchi yaratildi.")


# -------------------------> Dowland data handler in check data categories <------------------------- #


@router.callback_query(F.data == "downland_data")
async def downland_data_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="<b>Sizga qaysi bo`limni malumotlari kerak bo`lsa.</b>\n\n<i>Kerakli bo`limni tanlang:</i>",
        reply_markup=data_categries(),
    )


# ----------------------------> Dowland data handler in select the desired month <---------------------------- #


@router.callback_query(F.data.startswith("category:"))
async def select_data_category_handler(callback: types.CallbackQuery):
    category = callback.data.split(":")[1]

    await callback.message.edit_text(
        text=f"<b>Siz tanlagan bo`lim:</b> {category}\n\n"
        "<i>Malumotlarni necha oylik olish kerak?</i>",
        reply_markup=select_month_keyboard(category),
    )

# ----------------------------> Send file <---------------------------- #


@router.callback_query(F.data.startswith("month:"))
async def send_file_handler(callback: types.CallbackQuery):
    worker, month = callback.data.split(":")[1:]
    if worker == "saleries":
        data = await get_data_by_months(Salary, int(month))
        file = await write_salaries_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"oylik_maoshlar.xlsx"),
            caption=f"📄 Hisoblangan Maoshlar",
            reply_markup=cancel_button(True),
        )
    elif worker == "advances":
        data = await get_data_by_months(Advance, int(month))
        file = await write_advances_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"avanslar.xlsx"),
            caption=f"📄 Avanslar", reply_markup=cancel_button(True)
        )
    elif worker == "local_delivare":
        data = await get_data_by_months(LocalPartnerDelivery, int(month))
        file = await write_local_delivary_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"local_delivary.xlsx"),
            caption=f"📄 Mahaliy chiqarilgan yuklar",
            reply_markup=cancel_button(True),
        )
    elif worker == "local_payments":
        data = await get_data_by_months(LocalPayment, int(month))
        file = await write_local_payments_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"local_payments.xlsx"),
            caption=f"📄 Mahaliy qabul qilingan to`lovlar",
            reply_markup=cancel_button(True),
        )
    elif worker == "foreign_payments":
        data = await get_data_by_months(Transaction, int(month))
        file = await write_transaction_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"foreign_payments.xlsx"),
            caption=f"📄 Toshkent to`lovlari",
            reply_markup=cancel_button(True),
        )
    elif worker == "foreign_orders":  
        data = await get_data_by_months(ProductOrder, int(month))
        file = await write_foreign_orders_to_excel(data)
        await callback.message.answer_document(
            types.BufferedInputFile(file.read(), filename=f"foreign_orders.xlsx"),
            caption=f"📄 Toshkent buyurtmalari",
            reply_markup=cancel_button(True),
        )
