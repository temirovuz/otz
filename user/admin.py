from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_id', 'phone_number', 'full_name', 'user_type', 'balans', 'director')
    list_filter = ('user_type','director')
    search_fields = ('phone_number', 'full_name')
    search_help_text = 'Tel nomer va Ism orqali qidirish'
    readonly_fields = ['id', 'tg_id']
    ordering = ('full_name',)
