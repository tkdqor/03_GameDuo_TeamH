from django.urls import path

from .views import UserListAPIView, UserSigninApiView, UserSignupApiView

urlpatterns = [
    path("signin", UserSigninApiView.as_view()),
    path("signup", UserSignupApiView.as_view()),
    path("", UserListAPIView.as_view()),
]
