from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Yaratilgan vaqti", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name="Yangilangan vaqti", auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    tg_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Telegram ID")
    phone_number = PhoneNumberField(unique=True, db_index=True, blank=False, null=False, verbose_name="Telefon nomeri")
    full_name = models.CharField(max_length=155, db_index=True, null=True, blank=True, verbose_name='Ism familiya')
    user_type = models.CharField(max_length=155, choices=(("ishchi", "Ishchi"), ("mijoz", "Mijoz"), ("user", "User"),
                                                          ('director', 'Director')), default='user',
                                 verbose_name='Unvoni')
    director = models.CharField(max_length=155, choices=[('azizbek', 'Azizbek'), ('abdurahmon', 'Abdurahmon')],
                                default='azizbek', db_index=True)
    balans = models.DecimalField(max_digits=13, decimal_places=2, default=0, verbose_name='Hisobi')

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-id']
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["full_name"]),
            models.Index(fields=["user_type"]),
            models.Index(fields=["director"]),
        ]

    def __str__(self):
        return f"{self.phone_number} - {self.full_name}"
