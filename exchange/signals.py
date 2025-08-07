from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from advance.tasks import send_message_group
from core.settings import GROUP_ID
from exchange.models import Transaction, ProductOrder


@receiver(pre_save, sender=Transaction)
def update_balance_on_transaction_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Transaction.objects.get(pk=instance.pk)
    except Transaction.DoesNotExist:
        return

    if not instance.partner:
        return

    old_uzs = old_instance.uzs_amount or 0
    new_uzs = instance.uzs_amount or 0
    delta = new_uzs - old_uzs
    user = instance.partner
    if delta > 0:
        user.decrease_balance(delta)
    elif delta < 0:
        user.increase_balance(abs(delta))


@receiver(post_save, sender=Transaction)
def partner_balans_update(sender, instance, created, **kwargs):
    if created and instance.partner:
        user = instance.partner
        user.decrease_balance(instance.uzs_amount)
        text = (
            f"<b>Yangi tranzaksiya:</b>\n\n"
            f"👤 <b>Hamkor:</b> {user.full_name}\n"
            f"💸 <b>Tolov turi:</b> {instance.original_currency}\n"
            f"💰 <b>Miqdori:</b> {instance.amount} {instance.original_currency}\n"
            f"💸 <b>Konvertatsiya qilingan miqdor:</b> {instance.converted_amount}\n"
            f"💸 <b>UZS da:</b> {instance.uzs_amount} so'm\n"
            f"💲 <b>Valyuta kursi:</b> {instance.exchange_rate}\n"
            f"📅 <i>{instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>💬 Izoh:</b> {instance.comment}"
        )
        send_message_group(text)


@receiver(post_delete, sender=Transaction)
def restore_partner_balance_on_delete(sender, instance, **kwargs):
    if instance.partner:
        user = instance.partner
        user.increase_balance(instance.uzs_amount)


@receiver(post_save, sender=ProductOrder)
def partner_balans_update_(sender, instance, created, **kwargs):
    if created and instance.partner:
        user = instance.partner
        user.balans += instance.uzs_amount
        user.save(update_fields=["balans"])
        text = (
            f"<b>Yangi buyurtma:</b>\n\n"
            f"👤 <b>Hamkor:</b> {user.full_name}\n"
            f"💸 <b>Tolov turi:</b> {instance.original_currency}\n"
            f"💰 <b>Miqdori:</b> {instance.amount} {instance.original_currency}\n"
            f"💸 <b>Konvertatsiya qilingan miqdor:</b> {instance.converted_amount}\n"
            f"💸 <b>UZS da:</b> {instance.uzs_amount} so'm\n"
            f"💲 <b>Valyuta kursi:</b> {instance.exchange_rate}\n"
            f"📅 <i>{instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>💬 Izoh:</b> {instance.comment}"
        )
        send_message_group(text)


@receiver(pre_save, sender=ProductOrder)
def update_balance_on_payment_change(sender, instance, **kwargs):
    if not instance.pk or not instance.partner:
        return

    try:
        old_instance = ProductOrder.objects.get(pk=instance.pk)
    except ProductOrder.DoesNotExist:
        return

    old_uzs = old_instance.uzs_amount or 0
    new_uzs = instance.uzs_amount or 0
    delta = new_uzs - old_uzs

    user = instance.partner

    if delta > 0:
        user.increase_balance(delta)  # to‘lov oshdi → balans oshadi
    elif delta < 0:
        user.decrease_balance(abs(delta))  # to‘lov kamaydi → balans kamayadi


@receiver(post_delete, sender=ProductOrder)
def delete_order_product(sender, instance, **kwargs):
    if instance.partner:
        user = instance.partner
        user.decrease_balance(instance.uzs_amount)
