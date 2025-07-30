from django.contrib import admin

from exchange.models import Partner, Transaction, ProductOrder


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'balans']
    search_fields = ['full_name']
    search_help_text = "Hamkor ismi orqali qidirish"
    readonly_fields = ['id', 'balans']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner', 'amount', 'original_currency', 'exchange_rate', 'converted_amount', 'comment',
                    'created_at', 'uzs_amount']
    list_filter = ['partner', 'original_currency']
    readonly_fields = ['id', 'created_at', 'updated_at', 'uzs_amount', 'converted_amount']


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner', 'amount', 'original_currency', 'exchange_rate', 'converted_amount', 'comment',
                    'created_at', 'uzs_amount']
    list_filter = ['partner', 'original_currency']
    readonly_fields = ['id', 'created_at', 'updated_at', 'converted_amount', 'uzs_amount']
