from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password

from account.models import CustomUser
from advance.models import Advance, Salary
from local_trading.models import LocalPartnerDelivery, LocalPayment
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


@sync_to_async()
def get_user_type(tg_id: str):
    user = User.objects.filter(tg_id=tg_id).first()
    if user:
        return user.user_type
    return False


@sync_to_async()
def user_about(tg_id: str):
    user = User.objects.filter(tg_id=tg_id).first()
    if user:
        return user
    return False


@sync_to_async
def employee_advances(user_id):
    return list(
        Advance.objects.filter(employee__id=user_id, is_settled=False)
        .select_related("employee")
        .order_by("-created_at")
    )


@sync_to_async
def employee_salaries(user_id):
    return list(
        Salary.objects.filter(employee__id=user_id)
        .select_related("employee")
        .order_by("-created_at")
    )


@sync_to_async
def partner_orders(user_id):
    return list(
        LocalPartnerDelivery.objects.filter(partner__id=user_id)
        .select_related("partner")
        .order_by("-created_at")
    )


@sync_to_async
def partner_payments(user_id):
    return list(
        LocalPayment.objects.filter(partner__id=user_id)
        .select_related("partner")
        .order_by("-created_at")
    )


@sync_to_async
def models_data(model, start_date, end_date):
    return list(
        model.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
    )
