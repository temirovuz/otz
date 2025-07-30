from rest_framework import serializers

from local_trading.models import LocalPartnerDelivery, LocalPayment


class LocalPartnerDeliverySerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)

    class Meta:
        model = LocalPartnerDelivery
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'remaining_debt']

class LocalPaymentSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)

    class Meta:
        model = LocalPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
