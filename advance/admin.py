from django.contrib import admin

from advance.models import Advance, Salary


@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'amount', 'comment', 'is_settled', 'settled_amount', 'created_at']
    list_filter = ['employee', 'is_settled', 'employee__director']
    search_fields = ['employee__name', 'employee__phone_number']
    search_help_text = 'Ishchi ismi va telefon nomeri orqali qidirish.'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'is_settled', 'settled_amount']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'amount', 'comment', 'created_at']
    list_filter = ['employee', 'employee__director']
    search_fields = ['employee.name', 'employee.phone_number']
    search_help_text = 'Ishchi ismi va telefon nomeri orqali qidirish.'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
