from django.urls import path

from exchange.api.v1.views import PartnerListCreateView, PartnerUpdateView, TransactionDetailView, TransactionListCreateView, \
    ProductOrderListCreateView, ProductOrderDetailView

urlpatterns = [
    path('partners/', PartnerListCreateView.as_view(), name='partner-create-list'),
    path('partber/<int:pk>', PartnerUpdateView.as_view, name='partner-edit'),
    path('transaction/', TransactionListCreateView.as_view(), name='transaction-create-list'),
    path('transaction/<int:pk>', TransactionDetailView.as_view(), name='transaction-create-list'),

    path('product_order/', ProductOrderListCreateView.as_view(), name='transaction-create-list'),
    path('product_order/<int:pk>', ProductOrderDetailView.as_view(), name='transaction-create-list'),
]
