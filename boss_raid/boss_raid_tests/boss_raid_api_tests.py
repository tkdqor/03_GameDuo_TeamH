import datetime
import time

from rest_framework.test import APITestCase

from boss_raid.models import RaidRecord


class BossRaidStatusAPIViewTestCase(APITestCase):
    """
    Assignee : 상백

    보스레이드 입장 확인 테스트입니다.
    setUp 메서드로 enter_time과 time_limit이 설정된 RaidRecord 객체를 생성합니다.
    enter_time이 현재 시각이 되고, time.sleep()을 이용해 제한 시간인 time_limit 보다 1초 후에 GET 요청을 설정했으므로
    보스레이드 입장이 가능함을 확인합니다.
    """

    url = "/api/v1/bossRaid"

    def setUp(self):
        """RaidRecord 객체 생성 설정"""
        now = datetime.datetime.now()
        self.level = 1
        self.time_limit = 5
        self.enter_time = now
        self.level_clear_score = 20
        self.user_id = 1
        self.raidrecord = RaidRecord(self.level, self.time_limit, self.enter_time, self.level_clear_score, self.user_id)

    def test_bossraid_status_canEnter_False(self):
        """보스레이드 상태 입장 불가능 테스트"""
        time.sleep(1)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()["canEnter"], "False")

    def test_bossraid_status_canEnter_True(self):
        """보스레이드 상태 입장 가능 테스트"""
        time.sleep(7)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()["canEnter"], "True")

    # def test_bossraid_status_canEnter_False(self):
    #     """보스레이드 상태 입장 불가능 테스트"""
    #     response = self.client.get(self.url)
    #     print(timezone.now())
    #     print(self.enter_time)
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(response.json()["canEnter"], "False")

    # def test_bossraid_status_canEnter_True(self):
    #     """보스레이드 상태 입장 가능 테스트"""
    #     time.sleep(self.time_limit + 1)
    #     response = self.client.get(self.url)
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(response.json()["canEnter"], "True")
