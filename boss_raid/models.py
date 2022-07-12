from django.db import models

from user.models import User


class BossRaid(models.Model):
    """
    Assignee : 훈희

    보스 레이드에 대한 정보를 담고 있는 모델입니다.

    """

    id = models.BigAutoField(primary_key=True)
    level = models.IntegerField("레벨", default=0)
    level_clear_score = models.IntegerField("레벨 클리어점수", default=0)
    time_limit = models.IntegerField("제한시간", default=0)


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
    end_time = models.DateTimeField("종료시간", blank=True, null=True)
