from django.urls import path

from advance.api.v1.views import AdvanceCreateListView, AdvanceDetailView, SalaryCreateListView, SalaryDetailView

urlpatterns = [
    path('advances/', AdvanceCreateListView.as_view(), name="create-and-list-advances"),
    path('advance/<int:pk>/', AdvanceDetailView.as_view(), name='advance-detail'),

    path('salaries/', SalaryCreateListView.as_view(), name="create-and-list-salaries"),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name="salary-detail"),
]
