from rest_framework import serializers

from exchange.models import Partner, Transaction, ProductOrder


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
        read_only_fields = ['id','balans']

class TransactionSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','converted_amount','exchange_rate']

class ProductOrderSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)

    class Meta:
        model = ProductOrder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'converted_amount', 'exchange_rate']