from django.urls import path

from .views import UserSiginupApiView, UserSigninApiView

urlpatterns = [
    path("signin", UserSigninApiView.as_view()),
    path("signup", UserSiginupApiView.as_view()),
    path("", UserSigninApiView.as_view()),
]
