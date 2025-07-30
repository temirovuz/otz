from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password

from account.models import CustomUser
from user.models import User


@sync_to_async()
def get_user(tg_id: str):
    user = User.objects.filter(tg_id=tg_id).exists()
    return user


@sync_to_async()
def create_user(tg_id: str, phone: str):
    user = User.objects.create(tg_id=tg_id, phone_number=phone)
    return user

@sync_to_async()
def get_manager(phone):
    return CustomUser.objects.filter(phone_number=phone).exists()

@sync_to_async()
def create_manager(phone, password):
    CustomUser.objects.create(phone_number=phone, password=make_password(password))