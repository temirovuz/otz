from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from advance.models import Advance, Salary
from advance.services import AdvanceSettlementService
from advance.tasks import send_message_simple


@receiver(post_save, sender=Advance)
def user_balans_update_advance(sender, instance, created, **kwargs):
    if created and instance.employee:
        user = instance.employee
        user.balans -= instance.amount
        user.save(update_fields=["balans"])
        text = (
            f"<b>Yangi avans:</b>\n\n💸<b>Miqdori:</b> {instance.amount} so'm\n👤 <b>Ishchi:</b> {user.full_name}\n"
            f"📅 <i>{instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>Izoh:</b> {instance.comment}"
        )
        send_message_simple(user.tg_id, text)


@receiver(post_delete, sender=Advance)
def user_balans_restore_on_advance_delete(sender, instance, **kwargs):
    if instance.employee:
        user = instance.employee
        user.balans += instance.amount
        user.save(update_fields=["balans"])
        text = (
            f"<b>Avans bekor qilindi:</b>\n\n💸<b>Miqdori:</b> {instance.amount} so'm\n👤 <b>Ishchi:</b> {user.full_name}\n"
            f"📅 <i>{instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>Izoh:</b> {instance.comment}"
        )
        send_message_simple(user.tg_id, text)

@receiver(post_save, sender=Salary)
def user_balans_update_salary(sender, instance, created, **kwargs):
    if created and instance.employee:
        AdvanceSettlementService.settle_advances(instance.employee, instance.amount)
        user = instance.employee
        user.balans += instance.amount
        user.save(update_fields=["balans"])
        text = (
            f"<b>Yangi ish haqi:</b>\n\n💸<b>Miqdori:</b> {instance.amount} so'm\n👤 <b>Ishchi:</b> {user.full_name}\n"
            f"📅 {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            f"\n<b>Izoh:</b> {instance.comment}"
        )
        send_message_simple(user.tg_id, text)


@receiver(post_delete, sender=Salary)
def user_balans_restore_on_salary_delete(sender, instance, **kwargs):
    if instance.employee:
        user = instance.employee
        user.balans -= instance.amount
        user.save(update_fields=["balans"])
        text = (
            f"<b>Hisobdan o'chirildi:</b>\n\n💸<b>Miqdori:</b> {instance.amount} so'm\n👤 <b>Ishchi:</b> {user.full_name}\n"
            f"📅 {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            f"\n<b>Izoh:</b> {instance.comment}"
        )
        send_message_simple(user.tg_id, text)
