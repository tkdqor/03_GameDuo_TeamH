from django.contrib.auth import get_user_model
from django.db import models

from boss_raid.models import BossRaid

# Create your models here.
"""장고의 기본 User 모델을 불러옵니다."""
User = get_user_model()


class RaidRecord(models.Model):
    """
    Assignee : 민지

    레이드 레코드에 대한 정보를 담고 있는 모델입니다.
    """

    id = models.BigAutoField(primary_key=True)
    boss_raid = models.ForeignKey(
        to=BossRaid, verbose_name="보스레이드", on_delete=models.CASCADE, related_name="raid_record"
    )
    user = models.ForeignKey(to=User, verbose_name="사용자", on_delete=models.CASCADE, related_name="user")
    score = models.IntegerField("획득점수")
    enter_time = models.DateTimeField("시작시간", auto_now_add=True)
    end_time = models.DateTimeField("종료시간", auto_now=True)
