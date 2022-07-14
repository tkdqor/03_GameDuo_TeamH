from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BossRaid, RaidRecord
from .serializers import RaidRecordModelSerializer
from .utils import get_playing_records, get_score_and_end_time


# url : GET api/v1/bossRaid
class BossRaidStatusAPIView(APIView):
    """
    Assignee : 민지

    보스레이드 상태를 조회하는 api view 입니다.
    """

    def get(self, request):
        """
        playing_record가 있다면, 누군가가 플레이 중이므로 입장 불가능 상태로 response 합니다.
        playing_record가 없다면, 아무도 플레이를 하고 있지 않음으로 입장 가능 상태로 response 합니다.
        """
        playing_record = get_playing_records()
        serializer = RaidRecordModelSerializer(playing_record, many=True)

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
    로그인 한 유저만 보스레이드를 시작할 수 있습니다.
    """

    permissions_classes = [IsAuthenticated]

    def post(self, request):
        """
        보스레이드 시작 가능한 상태인지 확인하고, 시작 가능하다면 새로운 RaidRecord를 생성합니다.
        """
        playing_record = get_playing_records()

        if playing_record:
            return Response({"isEntered": "False"}, status=status.HTTP_202_ACCEPTED)
        else:
            user = request.user.id
            level = request.data["level"]
            """
            BossRaid에서 level_score_limit과 time_limit을 가져오는 부분은,
            추후에 S3 데이터를 캐싱한 Redis에서 가져오는 코드로 수정될 예정입니다.
            """
            boss_raid = BossRaid.objects.get(level=level)
            level_clear_score = boss_raid.level_clear_score
            time_limit = boss_raid.time_limit

            data = {"user": user, "level": level, "level_clear_score": level_clear_score, "time_limit": time_limit}

            serializer = RaidRecordModelSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"isEntered": "True", "raidRecordId": serializer.data["id"]}, status=status.HTTP_201_CREATED
                )


# url : PATCH api/v1/bossRaid/end
class BossRaidEndAPIView(APIView):
    """
    Assignee : 민지

    보스레이드 종료 api view 입니다.
    """

    def patch(self, request):
        """
        get_score_and_end_time 함수는 utils.py에 정의되어 있습니다.
        과제 요구사항에 response 값이 없기 때문에 204 status code를 사용합니다.
        """
        record_id = request.data["recordId"]
        raid_record = get_object_or_404(RaidRecord, pk=record_id)
        data = get_score_and_end_time(record_id)

        serializer = RaidRecordModelSerializer(raid_record, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
