from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from account.api.views import LoginAPIView, LogoutAPIView

urlpatterns = [
    # path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
