import re

from decimal import Decimal


def format_phone_number(phone):
    # Barcha raqam bo'lmagan belgilarni olib tashlash (+ bundan mustasno)
    cleaned = re.sub(r"[^\d+]", "", phone)

    # Agar + belgisi yo'q bo'lsa, qo'shamiz
    if not cleaned.startswith("+"):
        cleaned = "+998" + cleaned.lstrip("998")

    # 9 ta raqam borligini tekshirish
    if re.fullmatch(r"\+998\d{9}", cleaned):
        return cleaned
    else:
        raise ValueError(
            "Noto'g'ri telefon raqam formati. Telefon raqam +998 bilan boshlanishi va jami 13 ta raqamdan iborat bo‘lishi kerak."
        )


def format_decimal_number(decimal_number: Decimal) -> str:
    try:
        integer_part = int(decimal_number)  # Butun qismini olamiz
        formatted = "{:,}".format(integer_part).replace(",", " ")
        return formatted
    except (ValueError, TypeError, ArithmeticError):
        return "Noto‘g‘ri Decimal"


def format_advance_page(items):
    if not items:
        return "🔕 Hech qanday oldindan olingan maosh topilmadi."
    lines = ["🫵 Siz olgan avanslar:\n"]
    for item in items:
        amount = format_decimal_number(item.amount)
        lines.append(
            f"📅 {item.created_at.strftime('%Y-%m-%d')}\n"
            f"💰 {amount} so‘m\n💬 {item.comment or 'Izoh yo‘q'}\n"
            f"✅ Hisoblangan: {'Ha' if item.is_settled else 'Yo‘q'}\n"
        )
    return "\n".join(lines)


def format_salary_page(items):
    if not items:
        return "🔕 Hech qanday hisoblanga maosh topilmadi."
    lines = ["🫵 Sizning hisoblanga maoshlaringiz:\n"]
    for item in items:
        amount = format_decimal_number(item.amount)
        lines.append(
            f"📅 {item.created_at.strftime('%Y-%m-%d')}\n"
            f"💰 {amount} so‘m\n💬 {item.comment or 'Izoh yo‘q'}\n"
        )
    return "\n".join(lines)


def format_order_products(items):
    if not items:
        return "🔕 Hech qanday sotib olingan mahsulot topilmadi"

    lines = ["🫵 Sizning sotib olingan mahsulotlaringiz:\n"]
    for item in items:
        amount = format_decimal_number(item.total_amount)
        return_amount = format_decimal_number(item.return_amount)
        cash_received = format_decimal_number(item.cash_received)
        transferred_from_account = format_decimal_number(item.transferred_from_account)
        remaining_debt = format_decimal_number(item.remaining_debt)

        description = item.product_description or "Yo'q"
        comment = item.comment or "Izoh yo‘q"
        paid_status = "Xa" if item.completed else "Yo‘q"

        lines.append(
            f"📅 <b>{item.created_at.strftime('%Y-%m-%d')}</b>\n"
            f"🗒 <b>Mahsulot haqida:</b> {description}\n"
            f"💰 <b>To'lanishi shart bo'lgan pul:</b> {amount} so‘m\n"
            f"↩️ <b>Vozvrat bo'lgan miqdor:</b> {return_amount} so'm\n"
            f"💸 <b>Naqt to'langan:</b> {cash_received} so'm\n"
            f"💳 <b>Hisob raqamdan o'tqazma:</b> {transferred_from_account} so'm\n"
            f"💸 <b>Qolgan qarz:</b> {remaining_debt} so'm\n"
            f"💬 {comment}\n"
            f"🔰 <b>To'langanmi?</b> {paid_status}"
        )

    return "\n".join(lines)


def format_payments(items):
    if not items:
        return "🔕 Hech qanday to'lov topilmadi."

    lines = ["🫵 Sizning to'lovlaringiz:\n"]
    for item in items:
        amount = format_decimal_number(item.amount)
        payment_type = "Naqt" if item.payment_type == "cash" else "Schetdan o'tqazma"
        comment = item.comment or "Izoh yo‘q"

        lines.append(
            f"📅 {item.created_at.strftime('%Y-%m-%d')}\n"
            f"💰 {amount} so‘m\n"
            f"💳 To'lov turi: {payment_type}\n"
            f"💬 {comment}\n"
        )

    return "\n".join(lines)
