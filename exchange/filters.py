from django_filters import rest_framework as filters

from exchange.models import Transaction, ProductOrder, Partner

CURRENCY_CHOICES = [
    ('USD', 'USD'),
    ('UZS', 'UZS'),
]


class TransactionFilter(filters.FilterSet):
    partner = filters.NumberFilter(field_name='partner')
    original_currency = filters.ChoiceFilter(
        field_name='original_currency',
        choices=CURRENCY_CHOICES,
        label="Valyuta (USD yoki UZS)"
    )

    class Meta:
        model = Transaction
        fields = ['partner', 'original_currency']


class ProductOrderFilter(filters.FilterSet):
    partner = filters.NumberFilter(field_name='partner')
    original_currency = filters.ChoiceFilter(
        field_name='original_currency',
        choices=CURRENCY_CHOICES,
        label="Valyuta (USD yoki UZS)"
    )

    class Meta:
        model = ProductOrder
        fields = ['partner', 'original_currency']


class PartnerFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter', label='Qidiruv (ismi bo‘yicha)')

    class Meta:
        model = Partner
        fields = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(full_name__icontains=value)
