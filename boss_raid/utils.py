import datetime
import random

from django.utils import timezone

from .models import BossRaid, RaidRecord


def get_score_and_end_time(record):
    """
    Assignee : 민지

    클라이언트가 없는 관계로 생성한 함수입니다.
    유저가 플레이 후, 획득 점수와 종료 시간을 구하는 함수입니다.
    """
    raid_record = RaidRecord.objects.get(id=record)

    enter_time = raid_record.enter_time
    level = raid_record.level

    """
    level_clear_score와 time_limit은
    추후에 Redis에서 데이터를 받아옵니다.
    """
    boss_raid = BossRaid.objects.get(level=level)
    level_clear_score = boss_raid.level_clear_score
    time_limit = boss_raid.time_limit

    random_score = random.randint(0, level_clear_score)

    if random_score <= level_clear_score // 2:
        score = 0
        end_time = enter_time + datetime.timedelta(seconds=time_limit)
        return {"score": score, "end_time": end_time}
    else:
        score = random_score
        play_time = ((time_limit // level_clear_score) * score) - 1
        end_time = enter_time + datetime.timedelta(seconds=play_time)
        return {"score": score, "end_time": end_time}


def get_playing_records():
    """
    Assignee : 민지

    현재 게임을 플레이 하고 있는 레이드 레코드가 있는지 확인하기 위해 필요한 함수 입니다.
    end_time 값이 없는 레코드들을 모두 불러옵니다.
    그중에서 현재 시각을 기준으로 enter_time이 limit_time보다 이전인 아닌 기록들을 return 합니다.

    time_limit은 추후 Redis에서 데이터를 가져오는 코드로 리팩토링 할 예정입니다.
    """
    playing_records = RaidRecord.objects.filter(end_time=None)
    now = timezone.now()
    time_limit = 180
    playing_record = playing_records.filter(enter_time__gte=now - datetime.timedelta(seconds=time_limit))
    return playing_record
