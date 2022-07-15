# import datetime
# import operator
# import os
# import random
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()
#
# import requests
# from django.core.cache import cache
# from django.utils import timezone
#
# from boss_raid.models import BossRaid, RaidRecord
# from user.models import User
#
#
# def total_score(userid):
#     records = RaidRecord.objects.filter(user=userid)
#     score = []
#     for record in records:
#         score.append(record.score)
#     result = sum(score)
#     return result
#
#
# def rank():
#     users = User.objects.all()
#     rank = []
#     for user in users:
#         nickname = user.nickname
#         score = total_score(user.id)
#         if score != 0:
#             rank.append({"nickname": nickname, "score": score})
#         rank_result = sorted(rank, key=(lambda x: x["score"]), reverse=True)
#         rank_result_slice =  rank_result[0:10]
#     return rank_result_slice
#
#
# print(rank())
