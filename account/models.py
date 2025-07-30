from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from account.manager import CustomUserManager



class CustomUser(AbstractUser):
    CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
        ("user", "User")
    )
    user_type = models.CharField(max_length=10, choices=CHOICES, default="user" )
    username = None
    phone_number = PhoneNumberField(unique=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.phone_number)