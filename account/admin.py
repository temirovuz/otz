from django.contrib import admin

from account.models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_type', 'is_active')
    search_fields = ("phone_number", "user_type")
    list_filter = ('user_type', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'phone_number')

