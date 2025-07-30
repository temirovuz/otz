from decimal import Decimal

from django.db import transaction
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from local_trading.models import LocalPartnerDelivery, LocalPayment


@receiver(post_delete, sender=LocalPartnerDelivery)
def post_delete_local_partner_delivery(sender, instance, **kwargs):
    if instance.partner:
        user = instance.partner
        user.balans += instance.total_amount
        user.save(update_fields=['balans'])


@receiver(pre_save, sender=LocalPartnerDelivery)
def handle_remaining_debt_and_update_balance(sender, instance, **kwargs):
    if not instance.partner:
        return

    user = instance.partner

    # Avval: total_paid asosida remaining_debt hisoblanadi
    total_paid = (instance.cash_received or Decimal('0')) + \
                 (instance.return_amount or Decimal('0')) + \
                 (instance.transferred_from_account or Decimal('0'))
    new_debt = (instance.total_amount or Decimal('0')) - total_paid
    new_debt = new_debt.quantize(Decimal('0.01'))

    # --- Yangi object bo'lsa: balansdan avtomatik to'lash ---
    if not instance.pk:
        if user.balans > 0 and new_debt > 0:
            used = min(user.balans, new_debt)
            instance.cash_received = (instance.cash_received or Decimal('0')) + used
            total_paid += used
            new_debt -= used
            user.balans -= used
            user.save(update_fields=['balans'])

    # --- Eski object bo‘lsa: old value ni topamiz ---
    old_debt = Decimal('0')
    if instance.pk:
        try:
            old_instance = LocalPartnerDelivery.objects.get(pk=instance.pk)
            old_debt = old_instance.remaining_debt or Decimal('0')
        except LocalPartnerDelivery.DoesNotExist:
            pass

    # Farq asosida balansni yangilash
    delta = new_debt - old_debt
    if delta != 0:
        user.balans -= delta
        user.save(update_fields=['balans'])

    # Final qarz qiymatini yozamiz
    instance.remaining_debt = new_debt


@receiver(post_save, sender=LocalPayment)
def post_save_local_payment(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.partner
    payment_type = instance.payment_type
    amount = instance.amount or Decimal('0')

    remaining = amount

    deliveries = LocalPartnerDelivery.objects.filter(partner=user, completed=False).order_by('created_at')

    with transaction.atomic():
        for delivery in deliveries:
            if remaining <= 0:
                break

            unpaid = delivery.remaining_debt
            pay_amount = min(unpaid, remaining)

            if payment_type == "cash":
                delivery.cash_received += pay_amount
            elif payment_type == "transferred_from_account":
                delivery.transferred_from_account += pay_amount

            remaining -= pay_amount

            total_paid = delivery.cash_received + delivery.return_amount + delivery.transferred_from_account
            delivery.remaining_debt = delivery.total_amount - total_paid
            delivery.completed = delivery.remaining_debt <= 0
            delivery.save()

        # 🔧 Qo'shimcha: ortiqcha to'lov bo‘lsa — foydalanuvchi balansiga qo‘shiladi
        if remaining > 0:
            user.balans += remaining
            user.save(update_fields=['balans'])


@receiver(pre_delete, sender=LocalPayment)
def pre_delete_local_payment(sender, instance, **kwargs):
    user = instance.partner
    amount = instance.amount
    payment_type = instance.payment_type

    # Balansdan ayiramiz
    user.balans -= amount
    user.save(update_fields=['balans'])

    remaining = amount

    # Eng yangi to‘lovlar bilan bog‘langan deliverylarni qayta ko‘rib chiqamiz
    deliveries = LocalPartnerDelivery.objects.filter(partner=user).order_by('-created_at')

    with transaction.atomic():
        for delivery in deliveries:
            if remaining <= 0:
                break

            if payment_type == "cash":
                available = delivery.cash_received
                refund = min(available, remaining)
                delivery.cash_received -= refund

            elif payment_type == "transferred_from_account":
                available = delivery.transferred_from_account
                refund = min(available, remaining)
                delivery.transferred_from_account -= refund

            remaining -= refund

            # Qayta hisoblash
            total_paid = delivery.cash_received + delivery.return_amount + delivery.transferred_from_account
            delivery.remaining_debt = delivery.total_amount - total_paid
            delivery.completed = delivery.remaining_debt <= 0
            delivery.save()
