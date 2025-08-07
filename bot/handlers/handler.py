from aiogram import Router, F, types

from bot.crud import (
    employee_advances,
    employee_salaries,
    partner_orders,
    partner_payments,
    user_about,
)
from bot.filters.custom import (
    format_advance_page,
    format_decimal_number,
    format_order_products,
    format_payments,
    format_salary_page,
)
from bot.keyboard.inline import (
    SimplePaginator,
    admin_buttons,
    cancel_button,
    customer_buttons,
    employee_buttons,
)

router = Router()

# ---------------------> Balance handler for employees and customers <--------------------------------#


@router.callback_query(F.data.startswith("balans"))
async def handle_balance_query(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split(":")[1]
    user_info = await user_about(user_id)
    if user_info.balans >= 0:
        await callback_query.message.edit_text(
            f"*Sizning hisobingiz:* {format_decimal_number(user_info.balans)} so'm",
            parse_mode="MarkdownV2",
            reply_markup=cancel_button(False),
        )
    else:
        await callback_query.message.edit_text(
            f"<b>Sizning hisobingiz:</b> {format_decimal_number(user_info.balans)} so'm (qarzda)\nSiz <b>{user_info.director.capitalize()}</b> dan qarzdorsiz.",
            reply_markup=cancel_button(False),
        )


# ---------------------------------> Employee advances <--------------------------------#


@router.callback_query(F.data.startswith("advances"))
async def handle_advance_query(callback_query: types.CallbackQuery, page: int = 0):
    employee_id = callback_query.data.split(":")[1]
    user = await user_about(employee_id)
    items = await employee_advances(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="adance_page", page=page)
    text = format_advance_page(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=None)


@router.callback_query(F.data.startswith("adance_page"))
async def handle_page_query(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    user = await user_about(str(callback_query.from_user.id))
    items = await employee_advances(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="adance_page", page=page)
    text = format_advance_page(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=None)


# ---------------------------------> End of Employee salaries <--------------------------------#


@router.callback_query(F.data.startswith("saleries"))
async def handle_salaries_query(callback_query: types.CallbackQuery, page: int = 0):
    employee_id = callback_query.data.split(":")[1]
    user = await user_about(employee_id)
    items = await employee_salaries(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="salary_page", page=page)
    text = format_salary_page(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=None)


@router.callback_query(F.data.startswith("salary_page"))
async def handle_page_query(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    user = await user_about(str(callback_query.from_user.id))
    items = await employee_advances(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="salary_page", page=page)
    text = format_salary_page(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=None)


# ------------------------------------------------------------------------------------------- #

# ---------------------------------> Partner Deliveriy<--------------------------------#


@router.callback_query(F.data.startswith("order_products"))
async def handle_order_products_query(callback_query: types.CallbackQuery, page=0):
    customer_id = callback_query.data.split(":")[1]
    user = await user_about(customer_id)
    items = await partner_orders(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="order_product_page", page=page)
    text = format_order_products(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("order_product_page"))
async def handle_order_product_page_query(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    user = await user_about(str(callback_query.from_user.id))
    items = await partner_orders(user_id=user.id)
    paginator = SimplePaginator(items=items, page_title="order_product_page", page=page)
    text = format_order_products(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard)


# -------------------------------------------------------------------------------- #


# ---------------------------------> Partner Payments <--------------------------------#
@router.callback_query(F.data.startswith("payments"))
async def handle_payments_query(callback_query: types.CallbackQuery, page=0):
    customer_id = callback_query.data.split(":")[1]
    user = await user_about(customer_id)
    items = await partner_payments(user_id=user.id)
    paginator = SimplePaginator(
        items=items, page_title="partner_payment_page", page=page
    )
    text = format_payments(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("partner_payment_page"))
async def handle_partner_payment_page_query(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    user = await user_about(str(callback_query.from_user.id))
    items = await partner_payments(user_id=user.id)
    paginator = SimplePaginator(
        items=items, page_title="partner_payment_page", page=page
    )
    text = format_payments(paginator.current_items)
    keyboard = paginator.get_keyboard()
    await callback_query.message.edit_text(text, reply_markup=keyboard)


# -------------------------------------------------------------------------------- #

# ---------------------------------> Cancel buttons <--------------------------------#


@router.callback_query(F.data == "cancel:False")
async def cancel_handler(callback_query: types.CallbackQuery):
    user = await user_about(str(callback_query.from_user.id))
    if user.user_type == "ishchi":
        await callback_query.message.edit_text(
            text="SIz ishchi sifatida ro'yxatdan o'tgansiz.",
            reply_markup=employee_buttons(str(callback_query.from_user.id)),
        )
    elif user.user_type == "mijoz":
        await callback_query.message.edit_text(
            text="Siz mijoz sifatida ro'yxatdan o'tgansiz.",
            reply_markup=customer_buttons(str(callback_query.from_user.id)),
        )


@router.callback_query(F.data == "cancel:True")
async def cancel_handler_true(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(
            text="Siz Adminsiz va Kerakli bolimlarni birini tanlang",
            reply_markup=admin_buttons(),
        )
    except Exception as e:
        await callback_query.message.answer(
            text="Siz Adminsiz va Kerakli bolimlarni birini tanlang",
            reply_markup=admin_buttons(),
        )
