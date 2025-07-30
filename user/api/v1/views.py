from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsEmployeeUserAndAuthenticated
from user.api.v1.serializers import UserSerializer
from user.filters import UserFilter
from user.models import User


class UserListView(ListAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = User.objects.all().order_by("full_name")
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    ordering = ["full_name"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_type",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Foydalanuvchi turi",
            ),
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Ism yoki telefon bo‘yicha izlash",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    http_method_names = ["patch", "delete"]
