from django.db.models import Q
from django_filters import FilterSet, CharFilter
from .models import User

class UserFilter(FilterSet):
    user_type = CharFilter(field_name='user_type', lookup_expr='exact')
    query = CharFilter(method='search_filter')

    class Meta:
        model = User
        fields = ['user_type']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) | Q(phone_number__icontains=value)
        )
