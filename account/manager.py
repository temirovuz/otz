from django.contrib.auth.models import BaseUserManager
from user.models import User  # ← import qiling

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        # User modeldan phone_number orqali topamiz
        # try:
        #     linked_user = User.objects.get(phone_number=phone_number)
        # except User.DoesNotExist:
        #     raise ValueError(f"User with phone number {phone_number} does not exist")
        #
        # # ForeignKey ni to‘ldiramiz
        # extra_fields['user'] = linked_user

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)
