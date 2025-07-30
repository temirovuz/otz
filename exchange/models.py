from django.db import models

from user.models import BaseModel


class Partner(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Hamkor ismi", db_index=True)
    balans = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Toshkent hamkor"
        verbose_name_plural = "Toshkent hamkorlar"
        ordering = ['full_name']
        indexes = [models.Index(fields=['full_name'])]

    def decrease_balance(self, amount):
        self.balans -= amount
        self.save(update_fields=['balans'])

    def increase_balance(self, amount):
        self.balans += amount
        self.save(update_fields=['balans'])

    def __str__(self):
        return self.full_name


class Transaction(BaseModel):
    CURRENCY_CHOICES = [
        ('UZS', 'Uzbek Som'),
        ('USD', 'US Dollar'),
    ]
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="O'tkazilgan pul miqdori")
    original_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS',
                                         verbose_name="Boshlang'ich valyuta")
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valyuta kursi")
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                           verbose_name="Konvertatsiya qilingan miqdor")
    comment = models.TextField(null=True, blank=True)
    uzs_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="O'tkazilgan pul miqdori UZS da")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pul o'tkazmasi"
        verbose_name_plural = "Pul o'tkazmalari"

    def save(self, *args, **kwargs):
        # Converted amount
        if self.original_currency == 'USD':
            self.converted_amount = self.amount * self.exchange_rate
            self.uzs_amount = self.converted_amount
        elif self.original_currency == 'UZS':
            self.converted_amount = self.amount / self.exchange_rate
            self.uzs_amount = self.amount

        # Pul miqdorini yaxlitlash
        if self.converted_amount:
            self.converted_amount = round(self.converted_amount, 2)
        if self.uzs_amount:
            self.uzs_amount = round(self.uzs_amount, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} {self.original_currency} -> {self.converted_amount}"


class ProductOrder(BaseModel):
    CURRENCY_CHOICES = [
        ('UZS', 'Uzbek Som'),
        ('USD', 'US Dollar'),
    ]
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Pul miqdori")
    original_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS',
                                         verbose_name="Boshlang'ich valyuta")
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valyuta kursi")
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                           verbose_name="Konvertatsiya qilingan miqdor")
    comment = models.TextField(null=True, blank=True)
    uzs_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="O'tkazilgan pul miqdori UZS da")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sotib olingan mahsumot"
        verbose_name_plural = "Sotib olingan mahsulotlar"

    def save(self, *args, **kwargs):
        # Converted amount
        if self.original_currency == 'USD':
            self.converted_amount = self.amount * self.exchange_rate
            self.uzs_amount = self.converted_amount
        elif self.original_currency == 'UZS':
            self.converted_amount = self.amount / self.exchange_rate
            self.uzs_amount = self.amount

        # Pul miqdorini yaxlitlash
        if self.converted_amount:
            self.converted_amount = round(self.converted_amount, 2)
        if self.uzs_amount:
            self.uzs_amount = round(self.uzs_amount, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} {self.original_currency} -> {self.converted_amount}"
