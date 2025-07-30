from django.urls import path

from user.api.v1.views import UserListView,  UserDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
