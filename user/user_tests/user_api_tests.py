import datetime

from rest_framework.test import APIClient, APITestCase

from boss_raid.models import BossRaid, RaidRecord
from user.models import User


class UserSiginUpViewTestCase(APITestCase):
    """
    Assignee : 상백

    회원가입 테스트입니다.
    회원가입시 필요한 nickname과 password를 JSON 형태로 요청할 때 유저가 등록됨을 확인합니다.
    동일한 nickname으로 회원가입 시 400 status code를 확인합니다.
    nickname과 password과 6자리 이상이 되지 않은 경우, 400 status code를 확인합니다.
    """

    url = "/users/signup"

    def test_user_signup(self):
        """유저 등록 테스트"""
        user_data = {
            "nickname": "sangbaek",
            "password": "123456",
        }
        response = self.client.post(self.url, data=user_data, format="json")
        self.assertEqual(200, response.status_code)

    def test_unique_nickname_validation(self):
        """nickname 중복 여부 테스트"""
        user_data_1 = {
            "nickname": "sangbaek2",
            "password": "123456",
        }
        response = self.client.post(self.url, data=user_data_1, format="json")
        self.assertEqual(200, response.status_code)

        user_data_2 = {
            "nickname": "sangbaek2",
            "password": "123456",
        }
        response = self.client.post(self.url, data=user_data_2, format="json")
        self.assertEqual(400, response.status_code)

    def test_length_nickname_validation(self):
        """nickname 길이(6자리 이상) 테스트"""
        user_data = {
            "nickname": "sang",
            "password": "123456",
        }
        response = self.client.post(self.url, data=user_data, format="json")
        self.assertEqual(400, response.status_code)

    def test_length_password_validation(self):
        """password 길이(6자리 이상) 테스트"""
        user_data = {
            "nickname": "sangbaek",
            "password": "1234",
        }
        response = self.client.post(self.url, data=user_data, format="json")
        self.assertEqual(400, response.status_code)


class UserSignInViewTestCase(APITestCase):
    """
    Assignee : 상백

    회원 로그인 및 로그아웃 테스트입니다.
    setUp 메서드로 생성된 유저로 로그인 가능 여부를 확인합니다.
    또한, nickname과 password가 다른 경우를 확인합니다.
    """

    url = "/users/signin"

    def setUp(self):
        """유저 생성 설정"""
        self.nickname = "sangbaek"
        self.password = "123456"
        self.user = User.objects.create_user(self.nickname, self.password)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_authentication(self):
        """로그인 테스트"""
        print(self.user)
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

    def test_logout(self):
        """로그아웃 테스트"""
        response = self.client.delete(self.url)
        self.assertEqual(200, response.status_code)


class UserListTestCase(APITestCase):
    """
    Assignee : 상백

    회원 전체 조회 테스트입니다.
    setUp 메서드로 admin 유저 로그인 상태로 설정 후, 회원 전체 조회 여부를 확인합니다.
    """

    url = "/users/"

    def setUp(self):
        """로그인 상태 설정"""
        payload = {
            "nickname": "sangbaek",
            "password": "123456",
        }
        self.user = User.objects.create(**payload, is_admin=True)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_user_list_api_view_get(self):
        """회원 전체 조회 테스트"""
        response = self.client.get(self.url, format="json")
        self.assertEqual(200, response.status_code)


class UserLookupTestCase(APITestCase):
    """
    Assignee : 상백

    회원 단건 조회 테스트입니다.
    """

    url = "/users/<user_id>"

    def setUp(self):
        """유저 생성 설정"""
        self.user_id = (1,)
        self.nickname = "sangbaek"
        self.password = "123456"
        self.user = User.objects.create(
            id=self.user_id,
            nickname=self.nickname,
            password=self.password,
        )

        self.bossraid = BossRaid.objects.create(level=1, level_clear_score=20, time_limit=180)

        now = datetime.datetime.now()
        # self.id = 1
        self.level = 1
        self.enter_time = now
        self.level_clear_score = 20
        self.time_limit = 5

        self.raidrecord = RaidRecord.objects.create(
            # user_id=self.id,
            level=self.level,
            enter_time=self.enter_time,
            level_clear_score=self.level_clear_score,
            time_limit=self.time_limit,
        )

    def test_user_lookup_api_view_get(self):
        """회원 단건 조회 테스트"""
        response = self.client.get(self.url, format="json")
        self.assertEqual(200, response.status_code)
