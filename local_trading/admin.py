from django.contrib import admin

from local_trading.models import LocalPartnerDelivery, LocalPayment


@admin.register(LocalPartnerDelivery)
class LocalPartnerDeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner', 'product_description', 'total_amount', 'return_amount', 'cash_received',
                    'transferred_from_account', 'remaining_debt', 'comment', 'created_at']
    list_filter = ['partner__full_name', 'partner__director']
    readonly_fields = ['id', 'created_at', 'updated_at', 'remaining_debt']


@admin.register(LocalPayment)
class LocalPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner', 'amount', 'payment_type', 'comment', 'created_at']
    list_filter = ['partner__full_name', 'partner__director']
    readonly_fields = ['id', 'created_at', 'updated_at']
