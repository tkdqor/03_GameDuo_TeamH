from rest_framework.serializers import ModelSerializer

from .models import BossRaid, RaidRecord


class RaidRecordModelSeiralizer(ModelSerializer):
    """
    Assignee : 민지

    RaidRecord 모델을 위한 시리얼라이저 입니다.
    """

    class Meta:
        model = RaidRecord
        fields = "__all__"


class BossRaidModelSerializer(ModelSerializer):
    """
    Assignee : 민지

    BossRaid 모델을 위한 시리얼라이저 입니다.
    """

    class Meta:
        model = BossRaid
        fields = "__all__"
