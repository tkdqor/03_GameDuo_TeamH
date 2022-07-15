import os

import django
import requests
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


"""
Assignee : 정석

redis를 이용한 보스레이드 정보 캐싱 로직입니다.
보스레이드의 시간만 리턴해주는 get_raid_time
보스레이드들을 리턴해주는 get_levels 로 구성되어있습니다.

캐싱된 데이터를 필요로하는 이후 로직에서는 2개의 get함수만 사용하게되며,
캐싱데이터가 없을시엔 자체적으로 get 함수 내에서 create함수를 호출해 캐싱데이터를 생성 후 리턴해줍니다.
"""


def initial_data():
    url = "https://dmpilf5svl7rv.cloudfront.net/assignment/backend/bossRaidData.json"
    request = requests.get(url)
    data = request.json()
    return data


def create_raid_time():
    data = initial_data()
    bossraidlimitseconds = data["bossRaids"][0]["bossRaidLimitSeconds"]
    cache.set("limit_time", bossraidlimitseconds, 3600)
    time = cache.get("limit_time")
    return time


def create_levels():
    data = initial_data()
    levels = data["bossRaids"][0]["levels"]
    cache.set("levels", levels, 3600)
    levels = cache.get("levels")
    return levels


def get_raid_time():
    time = cache.get("limit_time")
    if time is None:
        time = create_raid_time()
    return time


def get_levels():
    levels = cache.get("levels")
    if levels is None:
        levels = create_levels()
    return levels
