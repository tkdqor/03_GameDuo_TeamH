from django.test import TestCase
from django.urls import resolve

from user.views import LoginView, UserListAPIView, UserSignupApiView


class UserViewTestCase(TestCase):
    """
    Assignee : 상백

    user view와 url 연결에 대한 테스트입니다.
    회원가입 / 로그인 / 로그아웃 / 회원 전체 및 단건 조회 url 연결을 확인합니다.
    """

    def test_url_resolves_to_sign_up_view(self):
        """sign_up url과 view 매칭 테스트"""

        found = resolve("/users/signup")

        self.assertEqual(found.func.__name__, UserSignupApiView.as_view().__name__)

    def test_url_resolves_to_sign_in_view(self):
        """sign_in url과 view 매칭 테스트"""

        found = resolve("/users/signin")

        self.assertEqual(found.func.__name__, LoginView.as_view().__name__)

    def test_url_resolves_to_logout_view(self):
        """로그아웃 url과 view 매칭 테스트"""

        found = resolve("/users/logout")

        self.assertEqual(found.func.__name__, UserListAPIView.as_view().__name__)

    def test_url_resolves_to_users_view(self):
        """회원 전체 조회 url과 view 매칭 테스트"""

        found = resolve("/users/")

        self.assertEqual(found.func.__name__, UserListAPIView.as_view().__name__)

    def test_url_resolves_to_users_user_id_view(self):
        """회원 단건 조회 url과 view 매칭 테스트"""

        found = resolve("/users/1")

        self.assertEqual(found.func.__name__, UserListAPIView.as_view().__name__)
