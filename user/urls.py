from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListAPIView, UserSigninApiView, UserSignupApiView

urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("signin", UserSigninApiView.as_view()),
    path("signup", UserSignupApiView.as_view()),
    path("", UserListAPIView.as_view()),
]
