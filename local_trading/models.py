from django.db import models

from user.models import User, BaseModel


class LocalPartnerDelivery(BaseModel):
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries', verbose_name="Hamkor")
    product_description = models.TextField(verbose_name="Mahsulot haqida")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="To'lanishi shart bo'lgan summa")
    return_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Vozvrat")
    cash_received = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Naqt to'langan")
    transferred_from_account = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                                   verbose_name="Schyotdan o‘tkazilgan pul")
    remaining_debt = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="Qolgan qarz")
    completed = models.BooleanField(default=False, db_index=True, verbose_name="To'langanmi?")
    comment = models.TextField(null=True, blank=True, verbose_name='Izoh')

    class Meta:
        verbose_name = "Mahaliy chiqarilgan yuk"
        verbose_name_plural = "Mahaliy chiqarilgan yuklar"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['completed'])]

    def __str__(self):
        return f"{self.partner.full_name} - {self.product_description} - {self.total_amount}"


class LocalPayment(BaseModel):
    PAYMENT_TYPES = [
        ("cash", "Naqt"),
        ("transferred_from_account", "Schetdan O'tqazma")
    ]
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='local_payments', verbose_name="Hamkor")
    amount = models.DecimalField(max_digits=13, decimal_places=2, verbose_name="Pul Miqdori", null=False, blank=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPES, default='cash', verbose_name="To'lov turi")
    comment = models.TextField(null=True, blank=True, verbose_name="Izhoh")

    class Meta:
        verbose_name = "Mahaliy hamkor to'lovi"
        verbose_name_plural = "Mahaliy hamkorlar to'lovlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.partner.full_name} - {self.amount} - {self.payment_type}"
