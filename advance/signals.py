from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from advance.models import Advance, Salary
from advance.services import AdvanceSettlementService


@receiver(post_save, sender=Advance)
def user_balans_update_advance(sender, instance, created, **kwargs):
    if created and instance.employee:
        user = instance.employee
        user.balans -= instance.amount
        user.save(update_fields=['balans'])


@receiver(post_save, sender=Salary)
def user_balans_update_salary(sender, instance, created, **kwargs):
    if created and instance.employee:
        AdvanceSettlementService.settle_advances(instance.employee, instance.amount)
        user = instance.employee
        user.balans += instance.amount
        user.save(update_fields=['balans'])
