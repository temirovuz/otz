from rest_framework import serializers

from user.models import User



class UserCreateSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "balans"]
