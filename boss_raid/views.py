# from django.shortcuts import render
import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User

from .models import BossRaid, RaidRecord
from .serializers import RaidRecordModelSeiralizer


# url : GET api/v1/bossRaid
class BossRaidStatusAPIView(APIView):
    """
    Assignee : 민지

    보스레이드 상태를 조회하는 api view 입니다.
    """

    def get(self, request):
        """
        end_time 값이 없는 레코드들을 모두 불러옵니다.
        그중에서 현재 시각을 기준으로 enter_time이 limit_time보다 이전인 기록들은 예외로 처리합니다.

        예외 처리 후에도 남아있는 레코드가 있다면, 누군가가 플레이 중이므로 입장 불가능 상태로 response 합니다.
        예외 처리 후 남아있는 레코드가 없다면, 아무도 플레이를 하고 있지 않음으로 입장 가능 상태로 response 합니다.

        limit_time은 추후 S3에서 변화가 있다면, 변화된 값을 넣는 코드로 리팩토링 할 예정입니다.
        """
        playing_records = RaidRecord.objects.filter(end_time=None)
        now = timezone.now()
        limit_time = 180
        playing_record = playing_records.filter(enter_time__gte=now - datetime.timedelta(seconds=limit_time))
        serializer = RaidRecordModelSeiralizer(playing_record, many=True)

        if playing_record:
            raid_record = serializer.data[0]
            return Response({"canEnter": "False", "enteredUserId": raid_record["user"]}, status=status.HTTP_200_OK)
        else:
            return Response({"canEnter": "True", "enteredUserId": "Nobody"}, status=status.HTTP_200_OK)


# url : POST api/v1/bossRaid/enter
class BossRaidEnterAPIView(APIView):
    """
    Assignee : 민지

    보스레이드 시작 api view 입니다.
    """

    def post(self, request):
        """
        보스레이드 시작 가능한 상태인지 확인하고, 시작 가능하다면 새로운 RaidRecord를 생성합니다.
        보스레이드 상태조회 api view 와 겹치는 코드는 추후에 리팩토링할 예정입니다.
        """
        playing_records = RaidRecord.objects.filter(end_time=None)
        now = timezone.now()
        limit_time = 180
        playing_record = playing_records.filter(enter_time__gte=now - datetime.timedelta(seconds=limit_time))

        if playing_record:
            return Response({"isEntered": "False"}, status=status.HTTP_200_OK)
        else:
            user_id = request.data["userId"]
            level = request.data["level"]

            user = User.objects.get(id=user_id)
            """
            BossRaid에서 level_score_limit과 time_limit을 가져오는 부분은,
            추후에 S3 데이터를 캐싱한 Redis에서 가져오는 코드로 수정될 예정입니다.
            """
            boss_raid = BossRaid.objects.get(level=level)
            level_clear_score = boss_raid.level_clear_score
            time_limit = boss_raid.time_limit

            new_raid_record = RaidRecord.objects.create(
                user=user, level=level, level_clear_score=level_clear_score, time_limit=time_limit
            )
            new_raid_record.save()

            return Response({"isEntered": "True", "raidRecordId": new_raid_record.id}, status=status.HTTP_201_CREATED)
