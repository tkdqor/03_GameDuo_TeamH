from rest_framework.test import APIClient, APITestCase

from user.models import User


class UserSiginUpViewTestCase(APITestCase):
    """
    Assignee : 상백

    회원가입 테스트입니다.
    회원가입시 필요한 nickname과 password를 JSON 형태로 요청할 때 유저가 등록됨을 확인합니다.
    동일한 nickname으로 회원가입 시 400 status code를 확인합니다.
    """

    url = "/user/signup"

    def test_user_signup(self):
        """유저 등록 테스트"""
        user_data = {
            "nickname": "sangbaek",
            "password": "1234",
        }
        response = self.client.post(self.url, data=user_data, format="json")
        self.assertEqual(200, response.status_code)

    def test_unique_nickname_validation(self):
        """nickname 중복 여부 테스트"""
        user_data_1 = {
            "nickname": "sangbaek2",
            "password": "1234",
        }
        response = self.client.post(self.url, data=user_data_1, format="json")
        self.assertEqual(200, response.status_code)

        user_data_2 = {
            "nickname": "sangbaek2",
            "password": "1234",
        }
        response = self.client.post(self.url, data=user_data_2, format="json")
        self.assertEqual(400, response.status_code)


class UserSignInViewTestCase(APITestCase):
    """
    Assignee : 상백

    회원 로그인 테스트입니다.
    setUp 메서드로 생성된 유저로 로그인 가능 여부를 확인합니다.
    또한, nickname과 password가 다른 경우를 확인합니다.
    """

    url = "/user/signin"

    def setUp(self):
        self.nickname = "sangbaek"
        self.password = "1234"
        self.user = User.objects.create_user(self.nickname, self.password)

    def test_authentication(self):
        """로그인 테스트"""
        response = self.client.post(self.url, {"nickname": self.nickname, "password": self.password})
        self.assertEqual(200, response.status_code)

    def test_authentication_with_wrong_nickname(self):
        """nickname이 다를 때 테스트"""
        response = self.client.post(self.url, {"nickname": "wrongwrong", "password": self.password})
        self.assertEqual(401, response.status_code)

    def test_authentication_with_wrong_password(self):
        """패스워드 다를 때 테스트"""
        response = self.client.post(self.url, {"nickname": self.nickname, "password": "wrongwrong"})
        self.assertEqual(401, response.status_code)


class UserLookupTestCase(APITestCase):
    """
    Assignee : 상백

    회원 전체 조회 테스트입니다.
    setUp 메서드로 로그인 상태를 설정 후 회원 전체 조회 여부를 확인합니다.
    """

    def setUp(self):
        """로그인 상태 설정"""
        payload = {
            "nickname": "sangbaek",
            "password": "1234",
        }
        self.user = User.objects.create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_user_api_view_get(self):
        """회원 전체 조회 테스트"""
        url = "/user/"
        response = self.client.get(url, format="json")
        self.assertEqual(200, response.status_code)
