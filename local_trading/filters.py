from random import choices

from django_filters import rest_framework as filters

from local_trading.models import LocalPartnerDelivery, LocalPayment

PAYMENT_TYPES = [
    ("cash", "Naqt"),
    ("transferred_from_account", "Schetdan O'tqazma")
]
DIRECTORS = [('azizbek', 'Azizbek'), ('abdurahmon', 'Abdurahmon')]

class LocalPartnerDeliveryFilter(filters.FilterSet):
    partner = filters.NumberFilter(field_name='partner')
    partner_director = filters.ChoiceFilter(field_name='partner__director', choices=DIRECTORS, lookup_expr='exact')

    class Meta:
        model = LocalPartnerDelivery
        fields = ['partner', 'partner_director']


class LocalPaymentFilter(filters.FilterSet):
    partner = filters.NumberFilter(field_name='partner')
    partner_director = filters.ChoiceFilter(field_name='partner__director', choices=DIRECTORS, lookup_expr='exact')
    payment_type = filters.ChoiceFilter(
        field_name='payment_type',
        choices=PAYMENT_TYPES,
        label="Valyuta (Naqt yoki Schetdan O'tqazma)"
    )

    class Meta:
        model = LocalPayment
        fields = ['partner', 'partner_director', 'payment_type']

