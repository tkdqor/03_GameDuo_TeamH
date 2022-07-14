import datetime
import time

from rest_framework.test import APIClient, APITestCase

from boss_raid.models import BossRaid, RaidRecord
from user.models import User


class BossRaidStatusFalseAPIViewTestCase(APITestCase):
    """
    Assignee : 상백

    보스레이드 입장 확인 테스트입니다.
    setUp 메서드로 enter_time과 time_limit이 설정된 RaidRecord 객체를 생성합니다.
    enter_time이 현재 시각이 되고, time.sleep()을 이용해 제한 시간인 time_limit 보다 7초 후에 GET 요청을 설정했으므로
    보스레이드 입장이 가능함을 확인합니다.
    """

    url = "/api/v1/bossRaid"

    def setUp(self):
        """유저 및 RaidRecord 객체 생성 설정"""
        now = datetime.datetime.now()
        self.level = 1
        self.enter_time = now
        self.level_clear_score = 20
        self.time_limit = 5

        self.user = User.objects.create(nickname="sangbaek", password="123456")

        self.raidrecord = RaidRecord.objects.create(
            user_id=self.user.id,
            level=self.level,
            enter_time=self.enter_time,
            level_clear_score=self.level_clear_score,
            time_limit=self.time_limit,
        )

    def test_bossraid_status_canEnter_True1(self):
        """보스레이드 상태 입장 불가능 테스트"""
        time.sleep(2)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()["canEnter"], "False")

    # def test_bossraid_status_canEnter_True2(self):
    #     """보스레이드 상태 입장 가능 테스트"""
    #     time.sleep(7)
    #     response = self.client.get(self.url)
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(response.json()["canEnter"], "True")


class BossRaidEnterAPIViewTestCase(APITestCase):
    """
    Assignee : 상백

    보스레이드 시작 테스트입니다.
    setUp 메서드로 인증된 유저와 level 1의 BossRaid 객체를 생성합니다.
    userId와 level을 입력했을 때, 새로운 RaidRecord 객체를 생성하는 것을 확인합니다.
    """

    url = "/api/v1/bossRaid/enter"

    def setUp(self):
        """유저 및 BossRaid 객체 생성 설정"""
        self.user_id = 1
        self.nickname = "sangbaek"
        self.password = "123456"
        self.user = User.objects.create(id=self.user_id, nickname=self.nickname, password=self.password)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.bossraid = BossRaid.objects.create(level=1, level_clear_score=20, time_limit=180)

    def test_bossraid_enter(self):
        """보스레이드 시작 테스트"""
        bossraid_data = {"userId": 1, "level": 1}
        response = self.client.post(self.url, data=bossraid_data, format="json")
        self.assertEqual(response.status_code, 201)


class BossRaidEndAPIViewTestCase(APITestCase):
    """
    Assignee : 상백

    보스레이드 종료 확인 테스트입니다.
    setUp 메서드로 인증된 유저와 level 1의 BossRaid 그리고 RaidRecord 객체를 생성합니다.
    recordId를 입력했을 때, 204 status code를 확인합니다.
    """

    url = "/api/v1/bossRaid/end"

    def setUp(self):
        """유저 및 BossRaid, RaidRecord 객체 생성 설정"""
        self.user_id = 1
        self.nickname = "sangbaek"
        self.password = "123456"
        self.user = User.objects.create(id=self.user_id, nickname=self.nickname, password=self.password)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.bossraid = BossRaid.objects.create(level=1, level_clear_score=20, time_limit=180)

        now = datetime.datetime.now()
        self.id = 1
        self.level = 1
        self.enter_time = now
        self.level_clear_score = 20
        self.time_limit = 5

        self.raidrecord = RaidRecord.objects.create(
            id=self.id,
            user_id=self.user.id,
            level=self.level,
            enter_time=self.enter_time,
            level_clear_score=self.level_clear_score,
            time_limit=self.time_limit,
        )

    def test_bossraid_end(self):
        """보스레이드 종료 테스트"""
        bossraid_data = {"recordId": 1}
        response = self.client.patch(self.url, data=bossraid_data, format="json")
        self.assertEqual(response.status_code, 204)
