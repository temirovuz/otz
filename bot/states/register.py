from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    contact = State()

class AdminRegister(StatesGroup):
    phone_number = State()
    password = State()