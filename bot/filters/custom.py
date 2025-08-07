import re
import pandas as pd


from io import BytesIO
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from asgiref.sync import sync_to_async

from bot.crud import models_data


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


# -------------------------> Write advances to excel <------------------------- #


@sync_to_async
def write_advances_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Ishchi": (advance.employee.full_name if advance.employee else "N/A"),
                "Pul miqdori": float(advance.amount),
                "Izoh": advance.comment or "",
                "Hisoblanganmi": "Ha" if advance.is_settled else "Yo'q",
                "Qolgan pul miqdori": float(advance.settled_amount),
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Avanslar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Avanslar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("F:F", 15)  # Hisoblanganmi
        worksheet.set_column("G:G", 18)  # Qolgan pul miqdori
        worksheet.set_column("H:H", 15)  # Yaratilgan sana

    file.seek(0)
    return file


# --------------------------> Write salaries to excel <-------------------------- #


@sync_to_async
def write_salaries_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Ishchi": (advance.employee.full_name if advance.employee else "N/A"),
                "Pul miqdori": float(advance.amount),
                "Izoh": advance.comment or "",
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Oylik maoshlar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Oylik maoshlar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("H:H", 15)  # Yaratilgan sana

    file.seek(0)
    return file


# -------------------------> Write local dilevare to excel <-------------------------- #


@sync_to_async
def write_local_delivary_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Hamkor": (advance.partner.full_name if advance.partner else "N/A"),
                "Mahsulot haqida": advance.product_description or "Yo'q",
                "Pul miqdori": float(advance.total_amount),
                "Vozvrat": float(advance.return_amount),
                "Naqt to'langan": float(advance.cash_received),
                "Schetdan o'tqazma": float(advance.transferred_from_account),
                "Qolgan qarz": float(advance.remaining_debt),
                "To'langanmi": "Xa" if advance.completed else "Yo'q",
                "Izoh": advance.comment or "",
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Chikarilgan yuklar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Chikarilgan yuklar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("F:F", 15)  # Hisoblanganmi
        worksheet.set_column("H:H", 15)  # Yaratilgan sana
        worksheet.set_column("I:I", 15)  # Yaratilgan vaqt

    file.seek(0)
    return file


# -------------------------------> Write local payments to excel <------------------------------- #


@sync_to_async
def write_local_payments_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Hamkor": (advance.partner.full_name if advance.partner else "N/A"),
                "Pul miqdori": float(advance.amount),
                "To'lov turi": (
                    "Naqt" if advance.payment_type == "cash" else "Schetdan o'tqazma"
                ),
                "Izoh": advance.comment or "",
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Chikarilgan yuklar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Chikarilgan yuklar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("F:F", 15)  # Hisoblanganmi
        worksheet.set_column("H:H", 15)  # Yaratilgan sana
        worksheet.set_column("I:I", 15)  # Yaratilgan vaqt

    file.seek(0)
    return file


# -------------------------------> Write foreign payments to excel <------------------------------- #


@sync_to_async
def write_transaction_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Hamkor": (advance.partner.full_name if advance.partner else "N/A"),
                "Pul miqdori": float(advance.amount),
                "Boshlang`ich valyuta": (
                    advance.original_currency if advance.original_currency else "N/A"
                ),
                "Valyuta kursi": (
                    float(advance.exchange_rate) if advance.exchange_rate else 0.0
                ),
                "Konvertatsiya qilingan miqdor": (
                    float(advance.converted_amount) if advance.converted_amount else 0.0
                ),
                "O'tkazilgan pul miqdori UZS da": (
                    float(advance.uzs_amount) if advance.uzs_amount else 0.0
                ),
                "Izoh": advance.comment or "",
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Chikarilgan yuklar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Chikarilgan yuklar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("F:F", 15)  # Hisoblanganmi
        worksheet.set_column("H:H", 15)  # Yaratilgan sana
        worksheet.set_column("I:I", 15)  # Yaratilgan vaqt

    file.seek(0)
    return file


# -------------------------> Write foreign orders to excel <-------------------------- #


@sync_to_async
def write_foreign_orders_to_excel(advances: list) -> BytesIO:
    data = []
    for advance in advances:
        data.append(
            {
                "Hamkor": (advance.partner.full_name if advance.partner else "N/A"),
                "Pul miqdori": float(advance.amount),
                "Boshlang`ich valyuta": (
                    advance.original_currency if advance.original_currency else "N/A"
                ),
                "Valyuta kursi": (
                    float(advance.exchange_rate) if advance.exchange_rate else 0.0
                ),
                "Konvertatsiya qilingan miqdor": (
                    float(advance.converted_amount) if advance.converted_amount else 0.0
                ),
                "O'tkazilgan pul miqdori UZS da": (
                    float(advance.uzs_amount) if advance.uzs_amount else 0.0
                ),
                "Izoh": advance.comment or "",
                "Yaratilgan sana": (
                    advance.created_at.strftime("%Y-%m-%d")
                    if hasattr(advance, "created_at")
                    else ""
                ),
            }
        )

    df = pd.DataFrame(data)
    file = BytesIO()

    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Chikarilgan yuklar")

        # Worksheet obyektini olish
        worksheet = writer.sheets["Chikarilgan yuklar"]

        # Ustunlar kengligini sozlash
        worksheet.set_column("B:B", 20)  # Ishchi
        worksheet.set_column("D:D", 15)  # Pul miqdori
        worksheet.set_column("E:E", 30)  # Izoh
        worksheet.set_column("F:F", 15)  # Hisoblanganmi
        worksheet.set_column("H:H", 15)  # Yaratilgan sana
        worksheet.set_column("I:I", 15)  # Yaratilgan vaqt

    file.seek(0)
    return file


# -------------------------> Save data by months <------------------------- #


async def get_data_by_months(model, months: int):
    today = timezone.now()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if months > 1:
        for _ in range(months - 1):
            start_date = (start_date - timedelta(days=1)).replace(day=1)
    end_date = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    query = await models_data(model, start_date, end_date)
    return query
