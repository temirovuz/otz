from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['tg_id', 'phone_number', 'created_at', 'updated_at', 'balans']
