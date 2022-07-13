import datetime
import random

from .models import BossRaid, RaidRecord


def get_score_and_endtime(record):
    """
    Assignee : 민지

    클라이언트가 없는 관계로 생성한 함수입니다.
    게임을 플레이한 시간과, 획득 점수를 계산합니다.
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

    random_score = random.randint(0, 20)

    if random_score <= 10:
        score = 0
        end_time = enter_time + datetime.timedelta(seconds=time_limit)
        return {"score": score, "end_time": end_time}
    else:
        score = random_score
        play_time = ((time_limit // level_clear_score) * score) - 1
        end_time = enter_time + datetime.timedelta(seconds=play_time)
        return {"score": score, "end_time": end_time}
