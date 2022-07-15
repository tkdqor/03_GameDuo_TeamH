from django.test import TestCase
from django.urls import resolve

from boss_raid.views import BossRaidEndAPIView, BossRaidEnterAPIView, BossRaidStatusAPIView


class BossRaidViewTestCase(TestCase):
    """
    Assignee : 상백

    bossraid view와 url 연결에 대한 테스트입니다.
    보스레이드 상태 조회 / 시작 / 종료 url 연결을 확인합니다.
    """

    def test_url_resolves_to_boss_raid_status_view(self):
        """보스레이드 상태를 조회 url과 view 매칭 테스트"""

        found = resolve("/api/v1/bossRaid")

        self.assertEqual(found.func.__name__, BossRaidStatusAPIView.as_view().__name__)

    def test_url_resolves_to_boss_raid_enter_view(self):
        """보스레이드 시작 url과 view 매칭 테스트"""

        found = resolve("/api/v1/bossRaid/enter")

        self.assertEqual(found.func.__name__, BossRaidEnterAPIView.as_view().__name__)

    def test_url_resolves_to_boss_raid_end_view(self):
        """보스레이드 종료 url과 view 매칭 테스트"""

        found = resolve("/api/v1/bossRaid/end")

        self.assertEqual(found.func.__name__, BossRaidEndAPIView.as_view().__name__)
