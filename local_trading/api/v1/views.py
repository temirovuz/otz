from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsEmployeeUserAndAuthenticated
from local_trading.api.v1.serializers import LocalPartnerDeliverySerializer, LocalPaymentSerializer
from local_trading.filters import LocalPartnerDeliveryFilter, LocalPaymentFilter
from local_trading.models import LocalPartnerDelivery, LocalPayment


class LocalPartnerDeliveryListCreateView(ListCreateAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    serializer_class = LocalPartnerDeliverySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LocalPartnerDeliveryFilter

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            return LocalPartnerDelivery.objects.all().order_by('-created_at')[:100]
        return LocalPartnerDelivery.objects.select_related('partner').all()


class LocalPartnerDeliveryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = LocalPartnerDelivery.objects.all()
    serializer_class = LocalPartnerDeliverySerializer
    lookup_field = 'pk'
    http_method_names = ['patch', 'delete']


class LocalPaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    serializer_class = LocalPaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LocalPaymentFilter

    def get_queryset(self):
        query_params = self.request.GET
        is_all_empty = all(not value for key, value in query_params.items())

        if is_all_empty:
            print('Bo‘sh query params — 100 ta obyekt')
            return LocalPayment.objects.all().order_by('-created_at')[:100]

        print('To‘liq query filter ishlasin')
        return LocalPayment.objects.select_related('partner').all()


class LocalPaymentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployeeUserAndAuthenticated]
    queryset = LocalPayment.objects.all()
    serializer_class = LocalPaymentSerializer
    lookup_field = 'pk'
    http_method_names = ['patch', 'delete']
