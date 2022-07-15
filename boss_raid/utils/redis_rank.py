import os

import django
from django.core.cache import cache
from django.db.models import Q

from boss_raid.models import RaidRecord
from user.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

"""
Assignee : 정석

redis를 이용한 랭킹 정보 캐싱 로직입니다.
로직상 레이드 실패시 RaidRecord에 score=0으로 기록됩니다.
랭킹로직에 0점인 데이터가 무의미하여
DB 호출시 0점이상의 레코드만 호출했습니다.
"""


def set_score(userid):
    records = RaidRecord.objects.filter(Q(user=userid) & Q(score__gt=0))
    score = []
    for record in records:
        score.append(record.score)
    score_data = sum(score)
    return score_data


def set_rank():
    users = User.objects.all()
    data = []
    for user in users:
        nickname = user.nickname
        score = set_score(user.id)
        if score != 0:
            data.append({"nickname": nickname, "score": score})
    rank_data = sorted(data, key=(lambda x: x["score"]), reverse=True)
    return rank_data


def create_rank():
    data = set_rank()
    cache.set("rank", data, 600)
    rank = cache.get("rank")
    return rank


def get_rank():
    rank = cache.get("rank")
    if rank is None:
        rank = create_rank()
    return rank
