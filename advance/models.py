from django.db import models

from user.models import BaseModel, User


class Advance(BaseModel):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                                 related_name='advances', verbose_name="Ishchi")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pul miqdori")
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Izoh')
    is_settled = models.BooleanField(default=False, verbose_name="Hisoblanganmi", db_index=True)
    settled_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Qolgan pul miqdori")

    class Meta:
        verbose_name = "Oldindan olinga maosh"
        verbose_name_plural = "Oldindan olinga maoshlar"
        ordering = ['-id']
        indexes = [models.Index(fields=['is_settled']), models.Index(fields=['employee', 'is_settled'])]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.settled_amount = self.amount

        self.is_settled = self.settled_amount == 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.phone_number} - {self.amount} - {self.created_at}"


class Salary(BaseModel):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                                 related_name='salaries', verbose_name="Ishchi")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pul miqdori")
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Izoh')

    class Meta:
        verbose_name = "Hisoblanga maosh"
        verbose_name_plural = "Hisoblanga maoshlar"
        ordering = ['-id']
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f"{self.employee.phone_number} - {self.amount} - {self.comment}"
