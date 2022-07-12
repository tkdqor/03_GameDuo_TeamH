# from django.shortcuts import render
import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RaidRecord
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
