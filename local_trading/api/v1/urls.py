from django.urls import path

from local_trading.api.v1.views import LocalPartnerDeliveryDetailView, LocalPartnerDeliveryListCreateView, \
    LocalPaymentListCreateView, LocalPaymentDetailView

urlpatterns = [
    path('local_delivery/', LocalPartnerDeliveryListCreateView.as_view(), name='delivery-list-create'),
    path('local_delivery/<int:pk>/', LocalPartnerDeliveryDetailView.as_view(), name='delivery-detail'),

    path('local_payment/', LocalPaymentListCreateView.as_view(), name='payment-list-create'),
    path('local_delivery/<int:pk>/', LocalPaymentDetailView.as_view(), name='payment-detail'),

]
