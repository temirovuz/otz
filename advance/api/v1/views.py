from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from advance.api.v1.serializers import AdvanceSerializer, SalarySerializer
from advance.filters import SalaryModelFilter, AdvanceFilter
from advance.models import Advance, Salary
from core.permissions import IsEmployeeUserAndAuthenticated


class AdvanceCreateListView(ListCreateAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    serializer_class = AdvanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvanceFilter

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            return Advance.objects.filter(is_settled=False).order_by("-created_at")[
                :100
            ]
        return Advance.objects.select_related("employee").all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "employee",
                openapi.IN_QUERY,
                description="Employee ID (raqam)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "employee_director",
                openapi.IN_QUERY,
                description="Employee direktor nomi (faqat azizbek yoki abdurahmon)",
                type=openapi.TYPE_STRING,
                enum=["azizbek", "abdurahmon"],  # 👈 Choice shu yerda berilgan
            ),
            openapi.Parameter(
                "is_settled",
                openapi.IN_QUERY,
                description="Hisoblanganmi: true yoki false",
                type=openapi.TYPE_BOOLEAN,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdvanceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = Advance.objects.all()
    serializer_class = AdvanceSerializer
    lookup_field = "pk"
    http_method_names = ["patch", "delete"]


class SalaryCreateListView(ListCreateAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    serializer_class = SalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryModelFilter

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            return Salary.objects.order_by("-created_at")[:100]
        return Salary.objects.select_related("employee").all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "employee",
                openapi.IN_QUERY,
                description="Employee ID (raqam)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "employee_director",
                openapi.IN_QUERY,
                description="Employee direktor nomi (faqat azizbek yoki abdurahmon)",
                type=openapi.TYPE_STRING,
                enum=["azizbek", "abdurahmon"],
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SalaryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    lookup_field = "pk"
    http_method_names = ["patch", "delete"]
