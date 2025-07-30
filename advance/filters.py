from django_filters import rest_framework as filters

from advance.models import Advance, Salary


class AdvanceFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee')
    employee_director = filters.CharFilter(field_name='employee__director', lookup_expr='exact')
    is_settled = filters.BooleanFilter(field_name='is_settled')

    class Meta:
        model = Advance
        fields = ['employee', 'employee_director', 'is_settled']


class SalaryModelFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee')
    employee_director = filters.CharFilter(field_name='employee__director', lookup_expr='exact')

    class Meta:
        model = Salary
        fields = ['employee', 'employee_director']
