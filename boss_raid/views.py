import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwner

from .models import RaidRecord
from .serializers import RaidRecordModelSerializer
from .utils.boss_raid_api_utils import get_playing_records, get_score_and_end_time
from .utils.redis_cache import get_levels, get_raid_time
from .utils.redis_queue import RedisQueue

q = RedisQueue("my_queue", host="localhost", port=6379, db=2)
"""배포 서버에서는 host 변경이 필요합니다."""


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

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """보스레이드 시작 가능한 상태인지 확인하고, 시작 가능하다면 새로운 RaidRecord를 생성합니다."""
        playing_record = get_playing_records()

        if playing_record:
            return Response({"isEntered": "False"}, status=status.HTTP_202_ACCEPTED)
        else:
            user = request.user.id
            level = int(request.data["level"])

            """
            동시성 이슈 핸들링을 위해 queue를 사용합니다.
            여러 유저가 동시에 레이드를 시작하려 할때, queue에 가장 먼저 정보를 넣은 유저만 게임을 시작할 수 있습니다.
            """
            element = json.dumps({"whoSetQueueFirst": user})
            q.put(element)
            first_element = q.get()
            first_element_json = json.loads(first_element)

            if user != first_element_json["whoSetQueueFirst"]:
                q.set_empty()
                return Response({"isEntered": "False"}, status=status.HTTP_202_ACCEPTED)
            try:
                level_clear_score = get_levels()[level - 1]["score"]
                time_limit = get_raid_time()

                data = {"user": user, "level": level, "level_clear_score": level_clear_score, "time_limit": time_limit}
                serializer = RaidRecordModelSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    q.set_empty()
                    return Response(
                        {"isEntered": "True", "raidRecordId": serializer.data["id"]}, status=status.HTTP_201_CREATED
                    )
                q.set_empty()
                return Response({"message": "게임을 시작할 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            except IndexError:
                q.set_empty()
                return Response({"message": "해당 레벨의 레이드가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# url : PATCH api/v1/bossRaid/end
class BossRaidEndAPIView(APIView):
    """
    Assignee : 민지

    보스레이드 종료 api view 입니다.
    관리자와 보스레이드를 시작한 본인만 종료 요청을 할 수 있습니다.
    """

    permission_classes = [IsOwner]

    def get_object_and_check_permissions(self, record_id):
        """요청을 한 유저가 해당 레이드에 권한이 있는지 체크합니다."""
        try:
            raid_record = RaidRecord.objects.get(id=record_id)
            self.check_object_permissions(self.request, raid_record)
            return raid_record
        except RaidRecord.DoesNotExist:
            return

    def patch(self, request):
        """
        get_score_and_end_time 함수는 utils.py에 정의되어 있습니다.
        과제 요구사항에 response 값이 없기 때문에 204 status code를 사용합니다.
        """
        record_id = request.data["recordId"]
        raid_record = self.get_object_and_check_permissions(record_id)
        data = get_score_and_end_time(record_id)

        serializer = RaidRecordModelSerializer(raid_record, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
