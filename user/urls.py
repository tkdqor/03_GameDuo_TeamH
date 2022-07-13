from django.urls import path

from .views import UserSigninApiView, UserSignupApiView

urlpatterns = [
    path("signin", UserSigninApiView.as_view()),
    path("signup", UserSignupApiView.as_view()),
    path("", UserSignupApiView.as_view()),
]
