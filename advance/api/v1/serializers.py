from rest_framework import serializers

from advance.models import Advance, Salary


class AdvanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Advance
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_settled', 'settled_amount']

class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Salary
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_settled', 'settled_amount']