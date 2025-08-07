from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_buttons():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="👮🏻‍♂️ Ish boshqaruvchi qo'shish", callback_data="add_manager"
        ),
        InlineKeyboardButton(
            text="📥 Malumotlar excel filega yozib olish", callback_data="downland_data"
        ),
    )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


def cancel_button(admin: bool = False):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel:{admin}")
    )
    return keyboard.as_markup(resize_keyboard=True)


def employee_buttons(employee: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="💸 Hisobim", callback_data=f"balans:{employee}"),
        InlineKeyboardButton(
            text="📋 Olingan avanslar", callback_data=f"advances:{employee}"
        ),
        InlineKeyboardButton(
            text="📊 Hisoblanga maoshlar", callback_data=f"saleries:{employee}"
        ),
    )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


def customer_buttons(customer: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="💸 Hisobim", callback_data=f"balans:{customer}"),
        InlineKeyboardButton(
            text="📋 Sotib olingan mahsulotlar",
            callback_data=f"order_products:{customer}",
        ),
        InlineKeyboardButton(text="📊 To'lovlar", callback_data=f"payments:{customer}"),
    )
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


class SimplePaginator:
    def __init__(self, items: list, page_title: str, page: int = 0, page_size: int = 3):
        self.items_per_page = page_size
        self.page_title = page_title
        self.page = page
        self.reversed_items = list(reversed(items))  # Eng so‘nggilari oldinda
        self.total_items = len(self.reversed_items)
        self.max_pages = (
            self.total_items + self.items_per_page - 1
        ) // self.items_per_page

        # Start va End hisoblash
        self.start = self.page * self.items_per_page
        self.end = self.start + self.items_per_page
        self.current_items = self.reversed_items[
            self.start : self.end
        ]  # Shu sahifadagi elementlar

    def get_keyboard(self):
        buttons = []

        if self.page > 0:
            buttons.append(
                InlineKeyboardButton(
                    text="◀️ Oldingi", callback_data=f"{self.page_title}:{self.page - 1}"
                )
            )

        if self.page < self.max_pages - 1:
            buttons.append(
                InlineKeyboardButton(
                    text="Keyingi ▶️", callback_data=f"{self.page_title}:{self.page + 1}"
                )
            )

        keyboard = InlineKeyboardBuilder()
        keyboard.add(*buttons)
        keyboard.row(
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel:False")
        )

        return keyboard.as_markup(resize_keyboard=True)


def select_month_keyboard(worker: str):
    keyboard = InlineKeyboardBuilder()
    for i in range(1, 13):
        keyboard.add(
            InlineKeyboardButton(
                text=f"{i} - oylik", callback_data=f"month:{worker}:{i}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel:True")
    )
    keyboard.adjust(4)
    return keyboard.as_markup(resize_keyboard=True)


def data_categries():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="📊 Hisoblangan maoshlar", callback_data="category:saleries"
        ),
        InlineKeyboardButton(
            text="📋 Olingan avanslar", callback_data="category:advances"
        ),
        InlineKeyboardButton(
            text="📥 Mahaliy chiqarilgan yuklar",
            callback_data="category:local_delivare",
        ),
        InlineKeyboardButton(
            text="💰 Mahaliy Hamkorlar to`lovlari",
            callback_data="category:local_payments",
        ),
        InlineKeyboardButton(
            text="💵 Toshkent uchun to`lovlar",
            callback_data="category:foreign_payments",
        ),
        InlineKeyboardButton(
            text="📦 Toshkentdan Olingan Mahsulotlar",
            callback_data="category:foreign_orders",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel:True")
    )
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
