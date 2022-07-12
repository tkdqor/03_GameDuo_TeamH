from django.db import models


class BossRaid(models.Model):
    """
    Assignee : 훈희

    보스 레이드에 대한 정보를 담고 있는 모델입니다.

    """

    id = models.BigAutoField(primary_key=True)
    level = models.IntegerField("레벨", default=0)
    level_clear_score = models.IntegerField("레벨 클리어점수", default=0)
    time_limit = models.IntegerField("제한시간", default=0)
