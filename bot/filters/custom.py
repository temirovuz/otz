import re


def format_phone_number(phone):
    # Barcha raqam bo'lmagan belgilarni olib tashlash (+ bundan mustasno)
    cleaned = re.sub(r'[^\d+]', '', phone)

    # Agar + belgisi yo'q bo'lsa, qo'shamiz
    if not cleaned.startswith('+'):
        cleaned = '+998' + cleaned.lstrip('998')

    # 9 ta raqam borligini tekshirish
    if re.fullmatch(r'\+998\d{9}', cleaned):
        return cleaned
    else:
        raise ValueError(
            "Noto'g'ri telefon raqam formati. Telefon raqam +998 bilan boshlanishi va jami 13 ta raqamdan iborat bo‘lishi kerak.")
