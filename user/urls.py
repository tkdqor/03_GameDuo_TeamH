from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    GameTokenObtainPairView,
    LoginView,
    LogoutView,
    UserListAPIView,
    UserListDetailAPIView,
    UserSignupApiView,
)

urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/gametoken", GameTokenObtainPairView.as_view(), name="token_gametoken"),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("signup", UserSignupApiView.as_view()),
    path("", UserListAPIView.as_view()),
    path("<user_id>", UserListDetailAPIView.as_view()),
]
