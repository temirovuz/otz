from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsAdminUserAndAuthenticated
from exchange.api.v1.serializers import (
    PartnerSerializer,
    TransactionSerializer,
    ProductOrderSerializer,
)
from exchange.filters import TransactionFilter, ProductOrderFilter, PartnerFilter
from exchange.models import Partner, Transaction, ProductOrder


class PartnerListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUserAndAuthenticated]
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Hamkor ismi bo‘yicha izlash (qisman)",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUserAndAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter  # ✅ to‘g‘risi shu, filter_class emas

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            return Transaction.objects.order_by("-created_at")[:100]
        return Transaction.objects.select_related("partner").all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "partner",
                openapi.IN_QUERY,
                description="Hamkor ID (raqam)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "original_currency",
                openapi.IN_QUERY,
                description="To'lov turi (usd yoki uzs)",
                enum=["USD", "UZS"],
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserAndAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "pk"
    http_method_names = ["patch", "delete"]


class ProductOrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUserAndAuthenticated]
    serializer_class = ProductOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductOrderFilter

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            return ProductOrder.objects.order_by("-created_at")[:100]
        return ProductOrder.objects.select_related("partner").all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "partner",
                openapi.IN_QUERY,
                description="Hamkor ID (raqam)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "original_currency",
                openapi.IN_QUERY,
                description="To'lov turi (usd yoki uzs)",
                enum=["USD", "UZS"],
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductOrderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserAndAuthenticated]
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    lookup_field = "pk"
    http_method_names = ["patch", "delete"]
